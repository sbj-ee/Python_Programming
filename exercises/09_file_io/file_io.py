"""Exercise 09: File I/O.

open() with a context manager, pathlib.Path for filesystem paths, and the
json/csv modules for structured data. All writes go to a temp directory so
this script leaves nothing behind in the repo.
"""

import csv
import json
import tempfile
from pathlib import Path


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)

        # --- Plain text I/O with a context manager ---
        # `with` guarantees the file is closed even if an exception occurs,
        # equivalent to try/finally but far less to get wrong.
        text_path = workdir / "notes.txt"
        with text_path.open("w") as f:
            f.write("line one\n")
            f.write("line two\n")

        with text_path.open("r") as f:
            lines = [line.rstrip("\n") for line in f]
        print(f"lines = {lines}")

        # --- pathlib for path manipulation ---
        print(f"text_path.name = {text_path.name}")
        print(f"text_path.suffix = {text_path.suffix}")
        print(f"text_path.stem = {text_path.stem}")
        print(f"text_path.parent = {text_path.parent}")
        print(f"text_path.exists() = {text_path.exists()}")

        # --- Appending ---
        with text_path.open("a") as f:
            f.write("line three\n")
        print(f"after append: {text_path.read_text().splitlines()}")

        # --- JSON: structured data round-trip ---
        data = {"name": "Ada", "languages": ["Python", "C++"], "active": True}
        json_path = workdir / "data.json"
        json_path.write_text(json.dumps(data, indent=2))

        loaded = json.loads(json_path.read_text())
        print(f"loaded json = {loaded}")
        print(f"loaded['languages'] = {loaded['languages']}")

        # --- CSV: tabular data ---
        csv_path = workdir / "scores.csv"
        with csv_path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "score"])
            writer.writerows([["Ada", 97], ["Linus", 88], ["Grace", 91]])

        with csv_path.open("r", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        print(f"csv rows = {rows}")
        total = sum(int(row["score"]) for row in rows)
        print(f"total score = {total}")

        # --- Listing directory contents ---
        print(f"files in workdir: {sorted(p.name for p in workdir.iterdir())}")

    # tmp directory and everything in it is gone once the `with` block exits
    print(f"tempdir still exists: {workdir.exists()}")


if __name__ == "__main__":
    main()
