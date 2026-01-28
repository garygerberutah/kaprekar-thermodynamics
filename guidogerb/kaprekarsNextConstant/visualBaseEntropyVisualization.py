import random


def to_base_5_digits(num, width):
    """Converts integer to base 5 digit list."""
    digits = []
    for _ in range(width):
        digits.append(num % 5)
        num //= 5
    return digits[::-1]


def from_base_5_digits(digits):
    """Converts base 5 digit list to integer."""
    val = 0
    for d in digits:
        val = val * 5 + d
    return val


def kaprekar_step_base5(num, width):
    digits = to_base_5_digits(num, width)
    desc = sorted(digits, reverse=True)
    asc = sorted(digits)
    return from_base_5_digits(desc) - from_base_5_digits(asc)


def analyze_base5_curve():
    print(f"{'Digits':<8} | {'Status':<15} | {'Note'}")
    print("-" * 50)

    # We test digit widths 2 to 20 to see where the curve "crashes"
    for width in range(2, 21):
        # 1. Search for Fixed Points (Candidates)
        fixed_points = set()
        loops_found = 0

        # Stochastic check: test 1000 random numbers
        for _ in range(1000):
            num = random.randint(0, 5 ** width - 1)
            history = set()

            # Run routine
            for _ in range(50):
                if num in history:
                    loops_found += 1
                    break
                history.add(num)

                next_val = kaprekar_step_base5(num, width)
                if next_val == num and next_val != 0:
                    fixed_points.add(num)
                    break
                num = next_val

        # 2. Analyze Results
        if len(fixed_points) == 1 and loops_found < 10:
            # (Rough heuristic: if almost everything hits one fixed point)
            # Note: A true proof requires testing ALL numbers, but this shows the trend.
            status = "CONSTANT"
            note = f"Found {list(fixed_points)[0]} (Base 10 val)"
        elif len(fixed_points) > 1:
            status = "SPLIT"
            note = f"Curve Fractured: {len(fixed_points)} distinct points"
        elif len(fixed_points) == 0:
            status = "CHAOS"
            note = "Only loops (no constants)"
        else:
            status = "HYBRID"
            note = f"1 Fixed Point + Loops"

        print(f"{width:<8} | {status:<15} | {note}")


if __name__ == "__main__":
    analyze_base5_curve()