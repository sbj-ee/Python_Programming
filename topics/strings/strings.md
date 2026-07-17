# Strings

`str` is an immutable sequence of Unicode code points. Every method that
looks like it modifies a string actually returns a new one.

## Core methods

```python
s = "  Hello, World!  "
s.strip()          # "Hello, World!"  -- removes leading/trailing whitespace
s.lower()           # "  hello, world!  "
s.replace("l", "L") # replaces ALL occurrences
s.split(",")        # ["  Hello", " World!  "]
"-".join(["a", "b", "c"])   # "a-b-c"
s.startswith("  He")
s.find("World")     # index, or -1 if not found
s.index("World")    # index, or raises ValueError if not found
```

## f-strings: the idiomatic way to format

```python
name, score = "Ada", 97.456
f"{name} scored {score:.1f}%"     # "Ada scored 97.5%"
f"{score=:.2f}"                    # "score=97.46" -- self-documenting debug output
f"{name:>10}"                       # right-aligned in a 10-char field
f"{name!r}"                         # uses repr() instead of str()

# f-strings evaluate arbitrary expressions
f"{2 + 2}"          # "4"
f"{[x*x for x in range(3)]}"  # "[0, 1, 4]"
```

## str vs bytes: the Python 3 distinction

```python
text = "café"                 # str: Unicode code points, no inherent encoding
data = text.encode("utf-8")    # bytes: b'caf\xc3\xa9' -- 5 bytes for 4 characters
data.decode("utf-8")            # back to "café"

# Mixing str and bytes raises TypeError -- this is deliberate, unlike Python 2
"a" + b"b"    # TypeError: can only concatenate str (not "bytes") to str
```

This str/bytes split — text is Unicode, bytes are raw octets, and the two
never implicitly mix — is the single biggest change from Python 2 and the
main reason old Python 2 code needs porting.

## Immutability and building strings efficiently

```python
s = "immutable"
s.upper()      # returns a NEW string; s itself is untouched

# Building a string in a loop with += is O(n²) for n pieces:
result = ""
for word in many_words:
    result += word + " "     # avoid this in a hot loop

# The idiomatic, O(n) alternative:
result = " ".join(many_words)
```

## Slicing works the same as on lists

```python
s = "abcdefgh"
s[2:5]    # "cde"
s[::-1]   # "hgfedcba" -- reverse a string
s[::2]    # "aceg"
```

## Multiline and raw strings

```python
raw = r"C:\Users\name"          # backslashes are literal, not escapes
multi = """line one
line two"""

template = f"""
Name: {name}
Score: {score:.1f}
"""
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| `result += piece` in a loop | O(n²) time for n concatenations | `"".join(pieces)` |
| Mixing `str` and `bytes` | `TypeError` at the point of concatenation | Decode/encode explicitly at I/O boundaries |
| `"a" == "a "` assumed equal | Trailing whitespace makes them unequal | `.strip()` before comparing user input |
| Slicing past the end (`s[100:200]`) | Returns `""`, no `IndexError` | Usually fine, but can hide bugs -- validate lengths if it matters |
| `len(s)` on non-ASCII text expecting byte count | Counts code points, not bytes | `len(s.encode("utf-8"))` for byte length |
