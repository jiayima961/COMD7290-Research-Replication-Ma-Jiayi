"""Ask the installed Codex app-server to discover the three project skills."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import queue
import subprocess
import threading
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    command = ["rtk", "proxy", "codex", "app-server", "--stdio"]
    process = subprocess.Popen(command, cwd=root, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace",
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    messages = queue.Queue()

    def read():
        for line in process.stdout:
            try:
                messages.put(json.loads(line))
            except ValueError:
                continue
        messages.put({"transport_closed": True})

    threading.Thread(target=read, daemon=True).start()

    def send(value):
        process.stdin.write(json.dumps(value) + "\n")
        process.stdin.flush()

    def receive(identifier):
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            item = messages.get(timeout=max(0.1, deadline - time.monotonic()))
            if item.get("transport_closed"):
                raise RuntimeError("Codex app-server closed before returning the discovery response.")
            if item.get("id") == identifier:
                if "error" in item:
                    raise RuntimeError(json.dumps(item["error"]))
                return item["result"]
        raise TimeoutError("Codex app-server discovery timeout.")

    try:
        send({"id": 1, "method": "initialize", "params": {
            "clientInfo": {"name": "comd7290-skill-check", "version": "1.0"},
            "capabilities": {"experimentalApi": True}}})
        initialized = receive(1)
        send({"method": "initialized", "params": {}})
        send({"id": 2, "method": "skills/list", "params": {"cwds": [str(root)], "forceReload": True}})
        response = receive(2)
        names = {"specify-empirical-study", "reproduce-and-diagnose", "verify-and-package"}
        entries = []
        for entry in response.get("data", []):
            for skill in entry.get("skills", []):
                if skill.get("name") in names and Path(skill["path"]).is_relative_to(root):
                    item = {key: skill.get(key) for key in ("name", "description", "enabled", "scope", "path")}
                    item["sha256"] = sha256(Path(skill["path"]).read_bytes()).hexdigest()
                    entries.append(item)
        result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(), "method": "skills/list",
                  "cwd": str(root), "command": command, "initialize_user_agent": initialized.get("userAgent"),
                  "skills": entries, "project_errors": [error for e in response.get("data", [])
                                                          for error in e.get("errors", [])
                                                          if str(root) in error.get("path", "")],
                  "inference_or_skill_execution_performed": False}
        result["status"] = "passed" if {s["name"] for s in entries if s["enabled"]} == names and not result["project_errors"] else "failed"
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "passed" else 1
    finally:
        process.stdin.close()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


if __name__ == "__main__":
    raise SystemExit(main())
