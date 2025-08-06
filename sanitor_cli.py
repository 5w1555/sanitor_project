# cli.py
from pathlib import Path

import click
from sanitor.engine import run_checks
from sanitor.config import load_config

SKIP_DIRS = {"env", "venv", "site-packages"}

def discover_py_files(root: Path):
    for path in root.rglob("*.py"):
        # skip virtual-env and 3rd-party code
        if SKIP_DIRS.intersection(path.parts):
            continue
        yield path

@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--config", type=click.Path(), help="sanitor JSON config")
@click.option("--json-output", is_flag=True)
def main(path, config, json_output):
    cfg = load_config(Path(config) if config else None)
    p = Path(path)

    # if given a file, just check that one; otherwise walk with our filter
    if p.is_file():
        sources = [p]
    else:
        sources = list(discover_py_files(p))

    all_issues = []
    for src in sources:
        all_issues.extend(run_checks(src, cfg))

    if json_output:
        import json
        def issue_to_dict(issue):
            d = issue.__dict__.copy()
            if isinstance(d.get("file"), Path):
                d["file"] = str(d["file"])
            return d
        print(json.dumps([issue_to_dict(i) for i in all_issues], indent=2))
    else:
        by_file = {}
        for i in all_issues:
            by_file.setdefault(i.file, []).append(i)
        for file, issues in by_file.items():
            print(f"\n📁 {file}")
            for i in sorted(issues, key=lambda x: x.line):
                print(f"  [{i.severity[:1]}] Line {i.line}: {i.message}")
    if not all_issues:
        print("✅ No issues found.")

if __name__ == "__main__":
    main()
