"""Write src/console/data/build.json (version, commit, build date) for the footer stamp. Run before a demo build."""
import json, subprocess, datetime
c = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip() or "unknown"
json.dump({"version": "0.1.0", "commit": c, "date": datetime.date.today().isoformat()}, open("src/console/data/build.json", "w"))
print(c)
