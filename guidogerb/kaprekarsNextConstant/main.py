import random
import time


def get_digits(num, width):
    return [int(d) for d in f"{num:0{width}d}"]


def from_digits(digits):
    return int("".join(map(str, digits)))


def kaprekar_step(num, width):
    digits = get_digits(num, width)
    # Sort Descending (Max) and Ascending (Min)
    digits_desc = sorted(digits, reverse=True)
    digits_asc = sorted(digits)

    max_val = from_digits(digits_desc)
    min_val = from_digits(digits_asc)

    return max_val - min_val


def find_constants_for_width(width, trials=5000):
    """
    Stochastically searches for constants.
    """
    found_constants = set()

    # We always include specific 'seed' patterns to ensure we don't miss
    # the 6174-derivatives (e.g., 63317664) which have small basins sometimes.
    seeds = [random.randint(0, 10 ** width - 1) for _ in range(trials)]

    for start_num in seeds:
        # Quick filter for repdigits
        if len(set(get_digits(start_num, width))) < 2:
            continue

        current = start_num
        history = set()

        # Run routine (limit steps to avoid infinite loops)
        for _ in range(60):
            if current in history:
                break
            history.add(current)

            next_val = kaprekar_step(current, width)

            if next_val == current and next_val != 0:
                found_constants.add(current)
                break
            current = next_val

    return sorted(list(found_constants))


def analyze_pattern():
    print(f"{'Digits':<8} | {'Count':<6} | {'Status':<15} | {'Hypothesis Check'}")
    print("-" * 75)

    # Trackers for the user's hypothesis
    prev_even_count = 0

    # We will test from 2 up to 20
    test_range = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    for width in test_range:
        constants = find_constants_for_width(width)
        count = len(constants)

        status = "Success" if count > 0 else "No Constant"
        hypothesis_msg = ""

        if width % 2 != 0:
            # ODD DIGITS CHECK
            if count == 1:
                hypothesis_msg = "✅ Fits (1 const)"
            elif count > 1:
                hypothesis_msg = f"❌ Divergent ({count} consts)"
            else:
                hypothesis_msg = "No const"
        else:
            # EVEN DIGITS CHECK
            # For the first even number (2), there is no 'previous' to compare validly
            if width == 2:
                hypothesis_msg = "Base Case"
            else:
                expected = prev_even_count + 1
                if count == expected:
                    hypothesis_msg = f"✅ Fits (+1 pattern: {count})"
                elif count > expected:
                    hypothesis_msg = f"⚠️ BONUS FOUND ({count} > {expected})"
                elif count < expected:
                    hypothesis_msg = f"❌ BROKEN ({count} < {expected})"

            # Update previous even count for next even iteration
            prev_even_count = count

        # Print row
        const_snippet = str(constants[0]) if constants else ""
        if len(constants) > 1:
            const_snippet += f" (+{len(constants) - 1} more)"

        print(f"{width:<8} | {count:<6} | {status:<15} | {hypothesis_msg}")


if __name__ == "__main__":
    print("Running Pattern Analysis on Kaprekar Constants...")
    print("Note: This relies on random sampling. Counts are empirical.\n")
    analyze_pattern()