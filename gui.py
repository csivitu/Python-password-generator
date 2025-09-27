import random
import string
import math
import tkinter as tk
from tkinter import messagebox

# Word bank built into the code
WORDS = [
    "sunrise", "planet", "echo", "quantum", "delta", "fusion", "matrix", "shadow",
    "nebula", "crystal", "titanium", "galaxy", "storm", "velocity", "breeze",
    "cosmos", "signal", "flare", "aurora", "nova", "spark", "horizon", "lunar"
]

def generate_password(num_words=4, include_numbers=True, include_symbols=True, exclude_chars=""):
    chosen = random.sample(WORDS, num_words)
    # Remove excluded chars from words
    cleaned_words = ["".join(c for c in word if c not in exclude_chars) for word in chosen]
    password = "-".join(cleaned_words)
    if include_numbers:
        valid_digits = [d for d in "0123456789" if d not in exclude_chars]
        if valid_digits:
            password += random.choice(valid_digits) + random.choice(valid_digits)
    if include_symbols:
        valid_symbols = [s for s in "!@#$%^&*?" if s not in exclude_chars]
        if valid_symbols:
            password += random.choice(valid_symbols)
    return password


# ---------- Strength calculation ----------
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

def strength_label(entropy_bits: float):
    if entropy_bits < 28:
        return "Very Weak", "red"
    elif entropy_bits < 36:
        return "Weak", "orange"
    elif entropy_bits < 60:
        return "Reasonable", "yellow"
    elif entropy_bits < 128:
        return "Strong", "lightgreen"
    else:
        return "Very Strong", "green"

# ---------- Callbacks ----------
def on_generate():
    try:
        num_words = int(word_entry.get())
        include_numbers = num_var.get()
        include_symbols = sym_var.get()

        password = generate_password(num_words, include_numbers, include_symbols)
        output_var.set(password)

        # Update strength
        entropy = estimate_entropy(password)
        label, color = strength_label(entropy)
        strength_var.set(f"{label} ({entropy} bits)")
        strength_label_widget.config(fg=color)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number of words.")

def on_copy():
    password = output_var.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        root.update()
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("No Password", "Generate a password first.")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("🔐 Password Generator")
root.geometry("480x380")
root.configure(bg="black")

# Common style
FONT = ("Consolas", 12, "bold")
FG_COLOR = "#c084fc"   # light purple
BG_COLOR = "black"
BTN_COLOR = "#9333ea"  # deep purple
ENTRY_COLOR = "#1e1b29"

# Input: number of words
tk.Label(root, text="Enter number of words:", font=FONT, fg=FG_COLOR, bg=BG_COLOR).pack(pady=5)
word_entry = tk.Entry(root, font=FONT, bg=ENTRY_COLOR, fg="white",
                      insertbackground="white", justify="center")
word_entry.insert(0, "4")
word_entry.pack(pady=5)

# Checkboxes
num_var = tk.BooleanVar(value=True)
sym_var = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include numbers", variable=num_var, font=FONT, fg=FG_COLOR,
               bg=BG_COLOR, selectcolor=BG_COLOR, activebackground=BG_COLOR).pack()
tk.Checkbutton(root, text="Include symbols", variable=sym_var, font=FONT, fg=FG_COLOR,
               bg=BG_COLOR, selectcolor=BG_COLOR, activebackground=BG_COLOR).pack()

# Generate button
tk.Button(root, text="Generate Password", font=FONT, fg="white", bg=BTN_COLOR,
          activebackground=FG_COLOR, activeforeground="black", command=on_generate).pack(pady=10)

# Output field
output_var = tk.StringVar()
output_entry = tk.Entry(root, textvariable=output_var, font=FONT, bg=ENTRY_COLOR,
                        fg=FG_COLOR, justify="center", width=40, relief="flat")
output_entry.pack(pady=5)

# Strength label
strength_var = tk.StringVar(value="Password Strength: N/A")
strength_label_widget = tk.Label(root, textvariable=strength_var,
                                 font=("Consolas", 12, "bold"), bg=BG_COLOR, fg="gray")
strength_label_widget.pack(pady=5)

# Copy button
tk.Button(root, text="Copy to Clipboard", font=FONT, fg="white", bg=BTN_COLOR,
          activebackground=FG_COLOR, activeforeground="black", command=on_copy).pack(pady=10)

root.mainloop()