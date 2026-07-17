# Regex

The `re` module provides Perl-style regular expressions for pattern
matching, extraction, and substitution over text.

## match, search, findall, finditer

```python
import re

re.match(r"Hello", "Hello, World")     # matches only at the START of the string
re.search(r"World", "Hello, World")     # scans anywhere in the string
re.findall(r"\d+", "a1 b22 c333")       # ['1', '22', '333'] -- all matches, as strings
re.finditer(r"\d+", "a1 b22 c333")       # same, but as an iterator of Match objects (lazy)
```

`match()` anchors implicitly at position 0; a common source of confusion is
expecting it to behave like `search()`. Use `re.fullmatch()` if the ENTIRE
string must match, not just a prefix.

## Capture groups

```python
m = re.search(r"(\d{3})-(\d{3})-(\d{4})", "call 555-123-4567")
m.group(0)     # "555-123-4567" -- the whole match
m.group(1)     # "555"           -- first parenthesized group
m.groups()     # ("555", "123", "4567")

# Named groups -- clearer than positional indices for complex patterns
m = re.search(r"(?P<user>[\w.]+)@(?P<domain>[\w.]+)", "ada@example.com")
m.group("user")     # "ada"
m.group("domain")    # "example.com"
```

## sub: find and replace

```python
re.sub(r"\d{3}-\d{3}-\d{4}", "REDACTED", "call 555-123-4567")
# "call REDACTED"

# Backreferences in the replacement string reuse captured groups
re.sub(r"(\w+)@(\w+)", r"\1 [at] \2", "ada@example")
# "ada [at] example"
```

## Compiled patterns: reuse across many inputs

```python
word_pattern = re.compile(r"\b[A-Za-z]+\b")
for line in many_lines:
    words = word_pattern.findall(line)     # avoids re-parsing the pattern each time
```

Compiling is mainly a readability/reuse win; the `re` module caches
recently-used uncompiled patterns internally too, so raw performance
differences are usually small unless the pattern is used in a tight loop.

## Greedy vs. non-greedy (lazy) quantifiers

```python
html = "<b>bold</b> and <i>italic</i>"
re.findall(r"<.*>", html)      # ['<b>bold</b> and <i>italic</i>'] -- greedy: one huge match
re.findall(r"<.*?>", html)     # ['<b>', '</b>', '<i>', '</i>']     -- lazy: smallest possible matches
```

`*`, `+`, `?`, `{m,n}` are greedy by default (match as much as possible);
appending `?` makes them lazy (match as little as possible).

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Using `match()` expecting `search()` semantics | Misses matches not at the start of the string | Use `re.search()`, or anchor deliberately with `^` |
| Greedy `.*` where a lazy `.*?` was intended | Matches far more than expected (e.g. across multiple HTML tags) | Use `.*?` or a more specific character class instead of `.` |
| Forgetting to escape regex metacharacters in literal text | `.` matches any character, `(` breaks grouping, etc. | `re.escape(literal_text)` before embedding it in a pattern |
| Parsing HTML/nested structures with regex | Regex can't correctly handle arbitrary nesting | Use an HTML parser (`html.parser`, `BeautifulSoup`) for real markup |
| Recompiling the same pattern in a hot loop | Minor but avoidable overhead | `re.compile()` once outside the loop, reuse the compiled pattern |
