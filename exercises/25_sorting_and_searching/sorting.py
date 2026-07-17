"""Exercise 25: Sorting & Searching.

Hand-rolled bubble/insertion/merge/quicksort for the mechanics, benchmarked
against the standard library's Timsort (sorted()/list.sort()), plus binary
search via the bisect module.
"""

import bisect
import random
import time


def bubble_sort(items: list[int]) -> list[int]:
    result = items.copy()
    n = len(result)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:  # already sorted -- stop early
            break
    return result


def insertion_sort(items: list[int]) -> list[int]:
    result = items.copy()
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


def merge_sort(items: list[int]) -> list[int]:
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])
    return _merge(left, right)


def _merge(left: list[int], right: list[int]) -> list[int]:
    result: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quicksort(items: list[int]) -> list[int]:
    if len(items) <= 1:
        return items
    pivot = items[len(items) // 2]
    less = [x for x in items if x < pivot]
    equal = [x for x in items if x == pivot]
    greater = [x for x in items if x > pivot]
    return quicksort(less) + equal + quicksort(greater)


def benchmark(name: str, func, data: list[int]) -> None:
    start = time.perf_counter()
    func(data)
    elapsed = time.perf_counter() - start
    print(f"  {name:<20} {elapsed * 1000:8.3f}ms")


def main() -> None:
    sample = [5, 2, 9, 1, 5, 6, 3, 8, 4, 7]
    print(f"unsorted: {sample}")
    print(f"bubble_sort: {bubble_sort(sample)}")
    print(f"insertion_sort: {insertion_sort(sample)}")
    print(f"merge_sort: {merge_sort(sample)}")
    print(f"quicksort: {quicksort(sample)}")
    print(f"sorted() (Timsort, stdlib): {sorted(sample)}")

    # --- Benchmark against a larger dataset ---
    random.seed(42)
    data = [random.randint(0, 10_000) for _ in range(1_500)]
    print("\nbenchmarks (1,500 random ints):")
    benchmark("bubble_sort", bubble_sort, data)
    benchmark("insertion_sort", insertion_sort, data)
    benchmark("merge_sort", merge_sort, data)
    benchmark("quicksort", quicksort, data)
    benchmark("sorted() [Timsort]", sorted, data)

    # --- Binary search via bisect: O(log n) on an already-sorted sequence ---
    sorted_data = sorted(data)
    target = sorted_data[len(sorted_data) // 3]
    index = bisect.bisect_left(sorted_data, target)
    print(f"\nbisect_left found {target} at index {index}: {sorted_data[index] == target}")

    # bisect.insort keeps a list sorted as you insert, without a full re-sort
    small = [1, 3, 5, 7, 9]
    bisect.insort(small, 4)
    print(f"insort(4) into {[1, 3, 5, 7, 9]} -> {small}")


if __name__ == "__main__":
    main()
