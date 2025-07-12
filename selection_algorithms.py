import random
import time
import statistics
from typing import List, Any


def _partition(a: List[Any], low: int, high: int, pivot_index: int) -> int:
    """
    Lomuto partition around a[pivot_index].

    Moves the pivot to the end, walks j from low..high‑1,
    keeping an i‑pointer for “< pivot” elements.
    Returns the final resting place of the pivot, which is now
    at index i – the classic Quick‑sort / Quick‑select partition.

    O(high‑low) time, O(1) space.
    """

    # stash pivot at end
    a[pivot_index], a[high] = a[high], a[pivot_index]
    pivot = a[high]
    i = low
    for j in range(low, high):
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    # drop pivot in slot i
    a[i], a[high] = a[high], a[i]

    # i == pivot’s index
    return i


def _median_of_medians(a: List[Any], low: int, high: int) -> int:
    """
    Return index of a “good” pivot (≥30% smaller, ≥30% larger).

    Implements the 5‑element group trick *iteratively*.
        1. Gather indices [low..high].
        2. Repeatedly compress them by replacing each 5‑block with its median.
        3. When ≤5 indices remain, return the true median index.

    The math in textbooks shows this guarantees the split quality
    necessary for worst‑case O(n) select.
    """
    indices = list(range(low, high + 1))

    # Keep shrinking until we’re down to ≤5 representatives
    while len(indices) > 5:
        new_indices = []
        for i in range(0, len(indices), 5):
            group = indices[i:i + 5]
            group.sort(key=a.__getitem__)

            # middle index in group
            median = group[len(group) // 2]
            new_indices.append(median)
        indices = new_indices

    # choose its true median element as pivot
    indices.sort(key=a.__getitem__)
    return indices[len(indices) // 2]


def select_deterministic(a: List[Any], k: int) -> Any:
    """
    Deterministic linear‑time selection.

    Uses the iterative median‑of‑medians for pivot choice.
    """
    low, high = 0, len(a) - 1
    while True:
        # find kth element
        if low == high:
            return a[low]
        pivot_idx = _median_of_medians(a, low, high)
        pivot_idx = _partition(a, low, high, pivot_idx)

        if k == pivot_idx:
            return a[k]
        # recurse left half
        elif k < pivot_idx:
            high = pivot_idx - 1
        # recurse right half
        else:
            low = pivot_idx + 1

def randomized_quickselect(a: List[Any], k: int) -> Any:
    """
    Expected O(n) selection via random pivots.

    Usually faster in practice; worst‑case is still O(n²),
    but probability of hitting that is 2⁻ⁿ-ish.
    """
    low, high = 0, len(a) - 1
    while True:
        if low == high:
            return a[low]
        # pick a random pivot
        pivot_idx = random.randint(low, high)
        pivot_idx = _partition(a, low, high, pivot_idx)

        if k == pivot_idx:
            return a[k]
        elif k < pivot_idx:
            high = pivot_idx - 1
        else:
            low = pivot_idx + 1

if __name__ == "__main__":
    trials = 100
    # repetitions per case, 10², 10³, 10⁴
    sizes = [10 ** e for e in range(2, 5)]
    distributions = {
        "random":     lambda n: [random.randint(0, n) for _ in range(n)],
        "sorted":     lambda n: list(range(n)),
        "rev_sorted": lambda n: list(range(n, 0, -1)),
    }

    for n in sizes:
        for name, gen in distributions.items():
            det_times, rnd_times = [], []
            for _ in range(trials):
                k = random.randint(0, n - 1)

                # deterministic
                arr = gen(n)
                t0 = time.perf_counter_ns()
                select_deterministic(arr, k)
                det_times.append(time.perf_counter_ns() - t0)

                # randomized
                arr = gen(n)
                t0 = time.perf_counter_ns()
                randomized_quickselect(arr, k)
                rnd_times.append(time.perf_counter_ns() - t0)

            det_mu_ms = statistics.fmean(det_times) / 1e6
            rnd_mu_ms = statistics.fmean(rnd_times) / 1e6
            print(f"{n:>6} | {name:<10} | mean runtime of deterministic median of medians ={det_mu_ms:6.2f} ms"
                  f" | mean runtime of randomized Quickselect={rnd_mu_ms:6.2f} ms")
