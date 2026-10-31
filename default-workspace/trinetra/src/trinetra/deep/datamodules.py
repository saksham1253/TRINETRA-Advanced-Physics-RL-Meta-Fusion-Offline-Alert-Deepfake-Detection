"""trinetra.deep.datamodules — torch Datasets + Kaggle paths + spatial-block assignment.

Each dataset yields exactly the dict its model's step expects. Paths default to /kaggle/input/<slug>; point
them at your downloaded datasets. `spatial_block` turns lat/lon into a coarse grid cell so training uses the
SAME spatial-block CV as eval/ (no spatial leakage between train and test — gate G6).
"""
from __future__ import annotations

import os
from dataclasses import dataclass

import numpy as np
import torch
from torch.utils.data import Dataset

KAGGLE_INPUT = os.environ.get("KAGGLE_INPUT", "/kaggle/input")


def spatial_block(lat: float, lon: float, cell_deg: float = 0.25) -> str:
    """Coarse lat/lon grid id for spatial-block CV (shared with eval.spatial_block_kfold)."""
    return f"{int(np.floor(lat / cell_deg))}_{int(np.floor(lon / cell_deg))}"


@dataclass
class KagglePaths:
    geo: str = f"{KAGGLE_INPUT}/trinetra-geo"
    fire: str = f"{KAGGLE_INPUT}/trinetra-fire"
    eo: str = f"{KAGGLE_INPUT}/trinetra-eo"
    anomaly: str = f"{KAGGLE_INPUT}/trinetra-telemetry"
    deepfake: str = f"{KAGGLE_INPUT}/trinetra-media"
    rl: str = f"{KAGGLE_INPUT}/trinetra-rl-logs"


class GeoSeriesDataset(Dataset):
    """Rows: Z, t, rain, static[6], optional label, lat, lon. Expects a .npz with these arrays."""

    def __init__(self, npz_path: str):
        d = np.load(npz_path, allow_pickle=True)
        self.Z = d["Z"].astype("float32"); self.t = d["t"].astype("float32")
        self.rain = d["rain"].astype("float32"); self.static = d["static"].astype("float32")
        self.label = d["label"].astype("float32") if "label" in d else None
        self.block = np.array([spatial_block(a, b) for a, b in zip(d["lat"], d["lon"])]) \
            if "lat" in d else np.array(["0_0"] * len(self.Z))

    def __len__(self):
        return len(self.Z)

    def __getitem__(self, i):
        item = {
            "Z": torch.tensor([self.Z[i]]), "t": torch.tensor([self.t[i]]),
            "rain": torch.tensor([self.rain[i]]), "static": torch.tensor(self.static[i]),
            "block": self.block[i],
        }
        # Only emit a label key when labels exist. A None value here would crash DataLoader's default
        # collate (it cannot batch NoneType) in physics-only pretraining runs.
        if self.label is not None:
            item["label"] = torch.tensor(self.label[i])
        return item


class WindowNPZDataset(Dataset):
    """Generic windowed-tensor dataset: X (N,C,T) + optional y + optional block. For anomaly / telemetry."""

    def __init__(self, npz_path: str, x_key: str = "X", y_key: str = "y"):
        d = np.load(npz_path, allow_pickle=True)
        self.X = d[x_key].astype("float32")
        self.y = d[y_key].astype("float32") if y_key in d else None
        self.block = d["block"].astype(str) if "block" in d else np.array(["0_0"] * len(self.X))

    def __len__(self):
        return len(self.X)

    def __getitem__(self, i):
        out = {"x": torch.tensor(self.X[i]), "block": self.block[i]}
        if self.y is not None:
            out["y"] = torch.tensor(self.y[i])
        return out


class ImageFolderNPZ(Dataset):
    """Image/clip tensors from .npz: images (N,...) + labels (N, n_classes) [+ block]. For fire/EO/deepfake."""

    def __init__(self, npz_path: str, x_key: str = "images", y_key: str = "labels"):
        d = np.load(npz_path, allow_pickle=True)
        self.X = d[x_key].astype("float32")
        self.y = d[y_key].astype("float32") if y_key in d else None
        self.block = d["block"].astype(str) if "block" in d else np.array(["0_0"] * len(self.X))

    def __len__(self):
        return len(self.X)

    def __getitem__(self, i):
        out = {"x": torch.tensor(self.X[i]), "block": self.block[i]}
        if self.y is not None:
            out["y"] = torch.tensor(self.y[i])
        return out


class RLTransitionDataset(Dataset):
    """Logged (s, a, r, s', done, behavior_prob) tuples for offline RL + OPE. .npz with these keys."""

    def __init__(self, npz_path: str):
        d = np.load(npz_path, allow_pickle=True)
        self.s = d["s"].astype("float32"); self.a = d["a"].astype("int64")
        self.r = d["r"].astype("float32"); self.s_next = d["s_next"].astype("float32")
        self.done = d["done"].astype("float32")
        self.bprob = d["behavior_prob"].astype("float32") if "behavior_prob" in d else None

    def __len__(self):
        return len(self.s)

    def __getitem__(self, i):
        out = {"s": torch.tensor(self.s[i]), "a": torch.tensor(self.a[i]),
               "r": torch.tensor(self.r[i]), "s_next": torch.tensor(self.s_next[i]),
               "done": torch.tensor(self.done[i])}
        if self.bprob is not None:
            out["behavior_prob"] = torch.tensor(self.bprob[i])
        return out
