"""Safely extract Kaggle archives and auto-detect TRINETRA dataset roots."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import tarfile
import time
import zipfile
from pathlib import Path


ARCHIVE_SUFFIXES = (".zip", ".tar", ".tar.gz", ".tgz")


def _safe_target(root: Path, name: str) -> Path:
    target = (root / name).resolve()
    if os.path.commonpath((root.resolve(), target)) != str(root.resolve()):
        raise ValueError(f"unsafe archive path: {name}")
    return target


def extract_archive(source: Path, target: Path, max_bytes: int, max_files: int) -> dict:
    target.mkdir(parents=True, exist_ok=True)
    count = total = 0
    if zipfile.is_zipfile(source):
        with zipfile.ZipFile(source) as archive:
            members = archive.infolist()
            count, total = len(members), sum(item.file_size for item in members)
            if count > max_files or total > max_bytes:
                raise ValueError(f"archive cap exceeded: files={count}, bytes={total}")
            for item in members:
                _safe_target(target, item.filename)
            archive.extractall(target)
    elif tarfile.is_tarfile(source):
        with tarfile.open(source) as archive:
            members = archive.getmembers()
            count, total = len(members), sum(item.size for item in members if item.isfile())
            if count > max_files or total > max_bytes:
                raise ValueError(f"archive cap exceeded: files={count}, bytes={total}")
            for item in members:
                _safe_target(target, item.name)
                if item.issym() or item.islnk():
                    raise ValueError(f"archive links are not allowed: {item.name}")
                if not (item.isfile() or item.isdir()):
                    raise ValueError(f"archive special file is not allowed: {item.name}")
            archive.extractall(target)
    else:
        raise ValueError("unsupported or invalid archive")
    return {"files": count, "uncompressed_bytes": total}


def _walk(roots: list[Path]):
    for root in roots:
        if not root.exists():
            continue
        for current, dirs, files in os.walk(root):
            yield Path(current), set(dirs), set(files)


def detect(roots: list[Path]) -> tuple[dict, dict]:
    found: dict[str, list[Path]] = {}

    def add(key: str, path: Path):
        found.setdefault(key, []).append(path.resolve())

    for current, dirs, files in _walk(roots):
        lower_dirs = {name.lower() for name in dirs}
        lower_files = {name.lower() for name in files}
        path_lower = current.as_posix().lower()
        if "data.yaml" in lower_files:
            add("DFIRE", current)
        if current.name.lower() == "training" and {"fire", "nofire"} <= lower_dirs:
            add("DEEPFIRE", current.parent)
        if {"fire_images", "non_fire_images"} <= lower_dirs:
            add("FIREDS", current)
        if {"fogsmog", "sandstorm", "lightning", "rain"} <= lower_dirs:
            add("WEATHER", current)
        if current.name.lower() == "train" and "images" in lower_dirs and "flame" in path_lower:
            add("CANDLE", current.parent.parent)
        if {"street", "buildings", "forest", "mountain"} <= lower_dirs:
            add("SCENES", current)
        if {"fire", "smoke"} <= lower_dirs:
            if all((current / hazard / kind).is_dir() for hazard in ("fire", "smoke") for kind in ("pos", "neg")):
                add("FIRESENSE", current)
        if {"real", "fake"} <= lower_dirs:
            face_like = any(token in path_lower for token in ("final dataset", "face", "stylegan"))
            add("FACES" if face_like else "CIFAKE", current)
        if {"aiartdata", "realart"} <= lower_dirs:
            add("AIART", current)
        if {"images", "labels"} <= lower_dirs and "home" in path_lower:
            add("HOMEFIRE", current.parent if current.name.lower() in {"train", "test"} else current)
        # inventory-only sources (no training contract yet): reported so the team sees them
        if {"annotations", "data_image"} <= lower_dirs:
            add("CRISISMMD", current)
        if {"training_videos", "testing_videos"} <= lower_dirs:
            add("AVENUE", current)
        if {"annualcrop", "forest", "river"} <= lower_dirs:
            add("EUROSAT", current)
        if any(name.startswith("image_") and name.endswith(".h5") for name in lower_files):
            add("L4S", current.parent.parent if current.name.lower() == "img" else current)
        if any("s1hand" in name and name.endswith((".tif", ".tiff")) for name in lower_files):
            add("S1F", current)
        if any(name.endswith(".json") for name in lower_files) and "hephaestus" in path_lower:
            add("HEPH_ANN", current)
        if any(name.endswith((".png", ".jpg", ".tif", ".tiff")) for name in lower_files) and "hephaestus" in path_lower:
            add("HEPH", current)
        for name in files:
            low = name.lower()
            if low.endswith(".csv") and "landslide" in low:
                add("GLC_CSV", current / name)
            if low.endswith(".csv") and ("hmaglof" in low or "glof" in low):
                add("GLOF_CSV", current / name)
            if low.endswith(".csv") and ("imerg" in low or "cloudburst" in low):
                add("IMERG_CSV", current / name)
        if any(name.endswith((".tif", ".tiff")) for name in lower_files) and any(
            token in path_lower for token in ("worldcover", "landcover", "land_cover", "lulc")
        ):
            add("LULC_ROOT", current)

    selected, detail = {}, {}
    for key, paths in sorted(found.items()):
        unique = sorted(set(paths), key=lambda path: (len(path.parts), path.as_posix()))
        choice = unique[0] if key.endswith("_CSV") else Path(os.path.commonpath([str(path) for path in unique]))
        selected[key] = str(choice)
        detail[key] = {"selected": str(choice), "candidates": [str(path) for path in unique]}
    return selected, detail


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="/kaggle/input")
    parser.add_argument("--work", default="/kaggle/working/trinetra_stage")
    parser.add_argument("--env-out", default="/kaggle/working/trinetra_dataset_env.sh")
    parser.add_argument("--report", default="/kaggle/working/trinetra_dataset_inventory.json")
    parser.add_argument("--max-archive-gb", type=float, default=12.0)
    parser.add_argument("--max-total-gb", type=float, default=40.0)
    parser.add_argument("--max-files", type=int, default=250_000)
    parser.add_argument("--no-extract", action="store_true")
    parser.add_argument("--skip-regex", default=os.environ.get("STAGE_SKIP_REGEX", ""),
                        help="case-insensitive regex; archives whose path matches are not extracted (e.g. datasets another account uses)")
    args = parser.parse_args(argv)
    input_root, work = Path(args.input), Path(args.work)
    extracted, archive_reports = work / "extracted", []
    scan_roots = [input_root]
    if not args.no_extract:
        archives = sorted(
            path for path in input_root.rglob("*")
            if path.is_file() and path.name.lower().endswith(ARCHIVE_SUFFIXES)
        )
        queue = [(path, 0) for path in archives]
        seen = set()
        total_bytes = 0
        skip = re.compile(args.skip_regex, re.I) if args.skip_regex else None
        t_start = time.time()
        while queue:
            source, depth = queue.pop(0)
            source_key = str(source.resolve())
            if source_key in seen:
                continue
            seen.add(source_key)
            if skip and skip.search(str(source)):
                archive_reports.append({"archive": str(source), "status": "skipped (skip-regex)"})
                print(f"[stage] skip {source.name}", flush=True)
                continue
            identity = hashlib.sha256(f"{source}:{source.stat().st_size}".encode()).hexdigest()[:10]
            name = source.name
            for suffix in (".tar.gz", ".tgz", ".zip", ".tar"):
                if name.lower().endswith(suffix):
                    name = name[: -len(suffix)]
                    break
            target = extracted / f"{name}-{identity}"
            marker = target / ".trinetra_extracted.json"
            try:
                if marker.exists():
                    info = json.loads(marker.read_text())
                    status = "cached"
                else:
                    remaining = int(args.max_total_gb * 1024**3) - total_bytes
                    if remaining <= 0:
                        raise ValueError("aggregate extraction cap reached")
                    info = extract_archive(
                        source, target, min(int(args.max_archive_gb * 1024**3), remaining), args.max_files
                    )
                    marker.write_text(json.dumps({"source": str(source), **info}, indent=2) + "\n")
                    status = "extracted"
                    print(f"[stage] extracted {source.name}: {info['uncompressed_bytes'] / 1024**3:.2f} GB · "
                          f"{(time.time() - t_start) / 60:.1f} min elapsed", flush=True)
                total_bytes += int(info["uncompressed_bytes"])
                scan_roots.append(target)
                archive_reports.append({"archive": str(source), "target": str(target), "status": status, **info})
                if depth < 2:
                    queue.extend(
                        (path, depth + 1) for path in sorted(target.rglob("*"))
                        if path.is_file() and path.name.lower().endswith(ARCHIVE_SUFFIXES)
                    )
            except Exception as error:
                archive_reports.append({"archive": str(source), "status": "failed", "error": str(error)})
    selected, detected = detect(scan_roots)
    env_path = Path(args.env_out)
    env_path.parent.mkdir(parents=True, exist_ok=True)
    env_path.write_text(
        "# generated by stage_kaggle_archives.py\n"
        + "\n".join(f"export {key}={shlex.quote(value)}" for key, value in sorted(selected.items()))
        + "\n"
    )
    report = {
        "input": str(input_root),
        "work": str(work),
        "archives": archive_reports,
        "datasets": detected,
        "missing_core": [key for key in ("DFIRE", "DEEPFIRE", "WEATHER", "CIFAKE") if key not in selected],
        "note": "Detection chooses a common root when train/test subfolders both match. Review candidates before training.",
    }
    Path(args.report).write_text(json.dumps(report, indent=2) + "\n")
    print(f"[stage] archives={len(archive_reports)} detected={len(selected)} env={env_path}")
    if report["missing_core"]:
        print("[stage] missing core vision roots:", ", ".join(report["missing_core"]))
    for key, value in sorted(selected.items()):
        print(f"  {key}={value}")


if __name__ == "__main__":
    main()
