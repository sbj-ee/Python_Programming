"""Exercise 33: Regex.

The re module: match/search/findall/sub, capture groups, and compiled
patterns for reuse across many inputs.
"""

import re


def main() -> None:
    text = "Contact: alice@example.com or bob.smith@work.co.uk, phone 555-123-4567"

    # --- match() anchors at the START of the string; search() scans for the first hit ---
    print(f"re.match(r'Contact', text): {bool(re.match(r'Contact', text))}")
    print(f"re.match(r'alice', text): {bool(re.match(r'alice', text))}")  # False: not at start
    print(f"re.search(r'alice', text): {bool(re.search(r'alice', text))}")

    # --- findall(): every non-overlapping match ---
    email_pattern = r"[\w.+-]+@[\w-]+\.[\w.-]+"
    emails = re.findall(email_pattern, text)
    print(f"emails found: {emails}")

    # --- Capture groups: () extracts sub-parts of each match ---
    phone_pattern = r"(\d{3})-(\d{3})-(\d{4})"
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        print(f"phone groups: area={phone_match.group(1)}, "
              f"prefix={phone_match.group(2)}, line={phone_match.group(3)}")
        print(f"full match: {phone_match.group(0)}")

    # --- Named groups: clearer than positional indices for complex patterns ---
    named_pattern = r"(?P<user>[\w.+-]+)@(?P<domain>[\w.-]+)"
    for m in re.finditer(named_pattern, text):
        print(f"user={m.group('user')!r}, domain={m.group('domain')!r}")

    # --- sub(): find-and-replace, with backreferences to captured groups ---
    redacted = re.sub(phone_pattern, "XXX-XXX-XXXX", text)
    print(f"redacted phone: {redacted}")

    redacted_emails = re.sub(email_pattern, "[email]", text)
    print(f"redacted emails: {redacted_emails}")

    # --- Compiled patterns: reuse across many inputs, faster in a hot loop ---
    word_pattern = re.compile(r"\b[A-Za-z]+\b")
    lines = ["The quick 42 fox", "jumps over 7 dogs!", "no numbers here"]
    for line in lines:
        words = word_pattern.findall(line)
        print(f"words in {line!r}: {words}")

    # --- split(): break a string on a pattern instead of a fixed delimiter ---
    messy = "one,  two,three   ,four"
    parts = re.split(r"\s*,\s*", messy)
    print(f"split on ',' with surrounding whitespace: {parts}")

    # --- Common pitfall: greedy vs. non-greedy quantifiers ---
    html = "<b>bold</b> and <i>italic</i>"
    greedy = re.findall(r"<.*>", html)  # one huge match, spans both tags
    lazy = re.findall(r"<.*?>", html)  # each tag matched separately
    print(f"greedy <.*>: {greedy}")
    print(f"lazy <.*?>: {lazy}")


if __name__ == "__main__":
    main()
