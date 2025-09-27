import random
import string
import math

WORDS = [
    "sunrise", "planet", "echo", "quantum", "delta", "fusion", "matrix", "shadow",
    "nebula", "crystal", "titanium", "galaxy", "storm", "velocity", "breeze",
    "cosmos", "signal", "flare", "aurora", "nova", "spark", "horizon", "lunar"
]

def generate_password(num_words=4, include_numbers=True, include_symbols=True):
    chosen = random.sample(WORDS, num_words)
    password = "-".join(chosen)

    if include_numbers:
        password += str(random.randint(10, 99))

    if include_symbols:
        password += random.choice("!@#$%^&*?")

    return password

# ---------- Password Strength ----------
def estimate_entropy(password: str) -> float:
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(c in string.punctuation for c in password): pool += 32
    if "-" in password: pool += 1  # account for the dash separator

    if pool == 0:
        pool = len(set(password)) or 2

    entropy = len(password) * math.log2(pool)
    return round(entropy, 2)

def strength_label(entropy_bits: float) -> str:
    if entropy_bits < 28:
        return "Very Weak"
    elif entropy_bits < 36:
        return "Weak"
    elif entropy_bits < 60:
        return "Reasonable"
    elif entropy_bits < 128:
        return "Strong"
    else:
        return "Very Strong"

# ---------- Main ----------
def main():
    print("Password Generator")

    try:
        num_words = int(input("Enter the number of words: "))
    except ValueError:
        print("Enter a valid number.")
        return

    include_numbers = input("Include numbers? (y/n): ").lower() == "y"
    include_symbols = input("Include symbols? (y/n): ").lower() == "y"
    exclude_chars = input("Characters to exclude (leave blank for none): ")
    password = generate_password(num_words, include_numbers, include_symbols, exclude_chars)

    print("\nGenerated Password:", password)

    # Show strength
    entropy = estimate_entropy(password)
    label = strength_label(entropy)
    print(f"Estimated Entropy: {entropy} bits")
    print(f"Password Strength: {label}")

if __name__ == "__main__":
    main()
