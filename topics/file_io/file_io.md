# File I/O

`open()` plus a `with` block is the idiomatic way to touch the filesystem;
`pathlib.Path` is the idiomatic way to manipulate paths.

## Opening files

```python
with open("notes.txt", "w") as f:
    f.write("line one\n")

with open("notes.txt") as f:        # mode defaults to "r" (read, text)
    contents = f.read()              # whole file as one string
    # or:
    for line in f:                    # memory-efficient line-by-line iteration
        process(line.rstrip("\n"))

with open("notes.txt", "a") as f:    # append
    f.write("more\n")

with open("data.bin", "rb") as f:     # binary mode -- no text decoding
    raw = f.read()
```

## pathlib: paths as objects, not strings

```python
from pathlib import Path

p = Path("data") / "2024" / "report.csv"   # / composes paths portably
p.name, p.stem, p.suffix, p.parent

p.exists(), p.is_file(), p.is_dir()
p.mkdir(parents=True, exist_ok=True)

p.write_text("hello")        # open + write + close in one call
p.read_text()                 # open + read + close in one call

for child in Path(".").iterdir():
    print(child)

for py_file in Path(".").rglob("*.py"):   # recursive glob
    print(py_file)
```

`pathlib` replaces most of the older `os.path` string-manipulation API with
methods on a `Path` object, and works identically across POSIX and Windows.

## json: structured data

```python
import json

data = {"name": "Ada", "tags": ["python", "math"]}
json.dumps(data, indent=2)          # to a string
Path("data.json").write_text(json.dumps(data))

loaded = json.loads(Path("data.json").read_text())
with open("data.json") as f:
    loaded = json.load(f)            # directly from a file object
```

## csv: tabular data

```python
import csv

with open("scores.csv", "w", newline="") as f:   # newline="" avoids extra \r\n on Windows
    writer = csv.writer(f)
    writer.writerow(["name", "score"])
    writer.writerows([["Ada", 97], ["Linus", 88]])

with open("scores.csv", newline="") as f:
    reader = csv.DictReader(f)        # each row as a dict, keyed by header
    rows = list(reader)
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| `open()` without `with` | File handle leaks if an exception occurs before `close()` | Always use `with open(...) as f:` |
| `f.read()` on a huge file | Loads the entire file into memory at once | Iterate line-by-line (`for line in f`), or read in chunks |
| Omitting `newline=""` when writing CSV on Windows | Extra blank lines between rows | Always pass `newline=""` to `open()` for CSV |
| Mixing text and binary mode | `TypeError` (str vs bytes) at the write/read call | Match the mode ("r"/"rb") to the data you're handling |
| String path concatenation (`dir + "/" + name`) | Breaks on Windows, fragile with trailing slashes | Use `pathlib.Path` and the `/` operator |
