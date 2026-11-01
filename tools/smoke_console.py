"""Headless smoke test of the TRINETRA Command Console demo path (Playwright, SwiftShader WebGL).

Loads the running app, records console errors and page errors, walks the key screens and saves screenshots.
Run: python3 tools/smoke_console.py --url http://localhost:3000/ --out /tmp/shots
Exit code 1 if any page error or console error occurred.
"""
import argparse, json, os, sys, time
from playwright.sync_api import sync_playwright


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--url", default="http://localhost:3000/#console?safe=1"); ap.add_argument("--out", default="/tmp/shots")
    ap.add_argument("--width", type=int, default=1920); ap.add_argument("--height", type=int, default=1080)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    errors, logs = [], []
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
        pg = b.new_page(viewport={"width": a.width, "height": a.height})
        pg.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        pg.on("console", lambda m: (errors if m.type == "error" else logs).append(f"{m.type}: {m.text}"))
        shot = lambda n: pg.screenshot(path=f"{a.out}/{n}.png", timeout=120000)  # noqa: E731
        pg.goto(a.url, wait_until="load", timeout=90000); time.sleep(12); shot("01_national")
        info = pg.evaluate("""() => ({ title: document.title, mode: !!document.body.innerText.match(/Mode/),
            outcome: !!document.body.innerText.match(/Outcome on this simulated scenario/), canvas: !!document.querySelector('canvas.maplibregl-canvas'),
            alerts: document.querySelectorAll('[aria-label="Alerts and evidence"] li').length })""")
        print("national:", json.dumps(info))
        # physics lab: lower the deployment base rate to 1 percent
        pg.get_by_role("button", name="Fusion").first.click() if pg.get_by_role("button", name="Fusion").count() else None
        pg.get_by_placeholder("Filter").fill("base rate"); time.sleep(0.5)
        sl = pg.get_by_role("slider", name="Deployment base rate (prior-shift correction, PROPOSED)")
        if sl.count():
            sl.first.focus(); sl.first.fill("0") if False else pg.evaluate("""() => { const s=[...document.querySelectorAll('input[type=range]')].find(x=>x.getAttribute('aria-label')?.startsWith('Deployment base rate'));
              const set=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set; set.call(s,'150'); s.dispatchEvent(new Event('input',{bubbles:true})); }""")
        time.sleep(2.5); shot("02_lab_prior")
        print("toast:", pg.locator('[role=status]').all_inner_texts()[:1])
        print("outcome:", pg.locator("text=False alarms").first.locator("xpath=..").inner_text().replace("\n", " ") if pg.locator("text=False alarms").count() else "n/a")
        # evidence: first alert card
        cards = pg.locator('[aria-label="Alerts and evidence"] ul li button')
        if cards.count():
            cards.first.click(); time.sleep(1.5); shot("03_evidence")
            pg.get_by_role("button", name="Dive").first.click(); time.sleep(5); shot("04_dive")
        # LoRa outage
        pg.get_by_role("tab", name="LoRa").click(); time.sleep(4)
        pg.get_by_role("button", name="Simulate internet and cellular outage").click(); time.sleep(6); shot("05_lora_outage")
        print("lora:", pg.locator('[aria-label="Alerts and evidence"]').inner_text()[:300].replace("\n", " | "))
        # light theme + about
        pg.get_by_role("button", name="Light theme (projector)").click(); time.sleep(4); shot("06_light")
        pg.get_by_role("button", name="About, methods and data sources").click(); time.sleep(1); shot("07_about")
        pg.keyboard.press("Escape")
        pg.set_viewport_size({"width": 1366, "height": 768}); time.sleep(3); shot("08_1366")
        b.close()
    print("errors:", len(errors)); [print("  ", e[:300]) for e in errors[:20]]
    print("warnings:", [l[:200] for l in logs if l.startswith("warning")][:8])
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
