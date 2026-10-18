"""Recreate local raw inputs for an archived skill-1 case without overwriting outputs."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-root", type=Path, required=True)
    args = parser.parse_args()
    case = args.case_root.resolve()
    if not case.is_relative_to(ROOT / "records/skill_tests"):
        raise ValueError("Case root must be inside this project's records/skill_tests/ directory.")
    manifest_path = case / "input_manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError("Use an archived case with its recorded input_manifest.json.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    restored, verified = 0, 0
    for item in manifest["inputs"]:
        source = (ROOT / item["path"]).resolve()
        target = (case / item["path"]).resolve()
        if not source.is_relative_to(ROOT) or not target.is_relative_to(case):
            raise ValueError("Input path escapes its source/case root.")
        if not source.is_file():
            raise FileNotFoundError(f"Obtain the registered original first: {item['path']}")
        if sha256(source.read_bytes()).hexdigest() != item["sha256"]:
            raise ValueError(f"Source version changed: {item['path']}")
        if target.exists():
            if sha256(target.read_bytes()).hexdigest() != item["sha256"]:
                raise ValueError(f"Existing case input differs; refusing overwrite: {item['path']}")
            verified += 1
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            restored += 1
    print(f"Case inputs ready: {restored} restored, {verified} already matched. Authored outputs were not overwritten.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
