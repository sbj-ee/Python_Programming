"""Exercise 06: Dicts & Sets.

dict maps keys to values with O(1) average lookup; set stores unique,
unordered elements. Both are hash-based, so keys/elements must be hashable
(immutable).
"""

from collections import Counter, defaultdict


def main() -> None:
    # --- dict basics ---
    person = {"name": "Ada", "age": 36, "field": "mathematics"}
    print(f"person = {person}")
    print(f"person['name'] = {person['name']}")
    print(f"person.get('missing', 'N/A') = {person.get('missing', 'N/A')}")

    person["age"] = 37  # update
    person["country"] = "UK"  # insert
    print(f"after update/insert: {person}")

    for key, value in person.items():
        print(f"  {key}: {value}")

    # --- dict comprehension ---
    squares = {n: n * n for n in range(5)}
    print(f"squares = {squares}")

    # --- merging dicts (3.9+ union operator) ---
    defaults = {"retries": 3, "timeout": 5}
    overrides = {"timeout": 10}
    merged = defaults | overrides
    print(f"merged = {merged}")

    # --- defaultdict: no KeyError, missing keys get a factory default ---
    groups: defaultdict[str, list[str]] = defaultdict(list)
    for word in ["apple", "avocado", "banana", "blueberry", "cherry"]:
        groups[word[0]].append(word)
    print(f"groups = {dict(groups)}")

    # --- Counter: specialized dict for counting hashable items ---
    letters = Counter("mississippi")
    print(f"letters = {letters}")
    print(f"most_common(2) = {letters.most_common(2)}")

    # --- set basics ---
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}
    print(f"union: {a | b}")
    print(f"intersection: {a & b}")
    print(f"difference: {a - b}")
    print(f"symmetric_difference: {a ^ b}")

    # --- set comprehension and deduplication ---
    unique_lengths = {len(w) for w in ["a", "bb", "cc", "ddd"]}
    print(f"unique_lengths = {unique_lengths}")

    dupes = [1, 2, 2, 3, 3, 3]
    print(f"deduplicated (order lost): {set(dupes)}")
    print(f"deduplicated (order kept): {list(dict.fromkeys(dupes))}")


if __name__ == "__main__":
    main()
