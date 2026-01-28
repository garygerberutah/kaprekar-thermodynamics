import random


# --- Helper Functions for Base Conversion ---
def int_to_base_string(n, base):
    """Converts an integer to a string representation in the given base."""
    if n == 0: return "0"
    digits = []
    while n:
        digits.append(int(n % base))
        n //= base

    # Map integers 10-15 to A-F
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "".join(chars[d] for d in reversed(digits))


def get_digits_in_base(num, width, base):
    """Returns a list of digits for a number in a given base, padded with zeros."""
    digits = []
    for _ in range(width):
        digits.append(num % base)
        num //= base
    return digits[::-1]  # Reverse to get correct order


def from_digits_in_base(digits, base):
    """Converts a list of digits in a given base back to an integer."""
    val = 0
    for d in digits:
        val = val * base + d
    return val


# --- The Universal Kaprekar Logic ---
def kaprekar_step_base(num, width, base):
    """Performs the routine in any number base."""
    digits = get_digits_in_base(num, width, base)

    # 1. Sort Descending (Max) and Ascending (Min)
    desc = sorted(digits, reverse=True)
    asc = sorted(digits)

    # 2. Reconstruct integers from those sorted digits
    max_val = from_digits_in_base(desc, base)
    min_val = from_digits_in_base(asc, base)

    # 3. Subtract
    return max_val - min_val


def find_constants_universal(base, width, trials=500):
    """Searches for constants in a specific base and width."""
    found = set()

    # Optimization: For small bases/widths, we can be exhaustive,
    # but for safety/speed we stick to random sampling (Monte Carlo).
    for _ in range(trials):
        # Generate random start number for this base
        max_limit = base ** width
        start_num = random.randint(0, max_limit - 1)

        # Repdigit check (in that base)
        digits = get_digits_in_base(start_num, width, base)
        if len(set(digits)) < 2:
            continue

        current = start_num
        history = set()

        # Iterate routine
        for _ in range(50):
            if current in history:
                break
            history.add(current)

            next_val = kaprekar_step_base(current, width, base)

            # Check for Fixed Point
            if next_val == current and next_val != 0:
                found.add(current)
                break
            current = next_val

    return sorted(list(found))


def main():
    print(f"{'Base':<5} | {'Digits':<7} | {'Status':<12} | {'Found Constants (Base Representation)'}")
    print("-" * 80)

    # We test bases from 2 (Binary) to 16 (Hexadecimal)
    # You can change this range to test higher bases
    bases_to_test = range(2, 17)

    for base in bases_to_test:
        print(f"--- Processing Base {base} ---")

        # We test digit widths 2 to 20
        for width in range(2, 21):
            # Increase trials for higher bases/widths to improve accuracy
            trials = 300 if width < 10 else 800

            constants = find_constants_universal(base, width, trials)

            if constants:
                status = "Success"
                # Convert finding to string representation (e.g. 10 -> A)
                const_strs = [int_to_base_string(c, base) for c in constants]
                # Truncate if too many constants found
                if len(const_strs) > 3:
                    output = f"{', '.join(const_strs[:3])} (+{len(const_strs) - 3} more)"
                else:
                    output = ", ".join(const_strs)
            else:
                status = "Loops"
                output = "-"

            # Print row
            print(f"{base:<5} | {width:<7} | {status:<12} | {output}")


if __name__ == "__main__":
    main()