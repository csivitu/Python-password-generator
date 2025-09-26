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

def generate_password(num_words=4, include_numbers=True, include_symbols=True):
    chosen = random.sample(WORDS, num_words)
    password = "-".join(chosen)

    if include_numbers:
        password += str(random.randint(10, 99))

    if include_symbols:
        password += random.choice("!@#$%^&*?")

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

    #Labels for colours have alreay been given thus the issue is moot yet here is a lil something for y'all

    # Add after strength_label_widget
strength_canvas = tk.Canvas(root, height=16, width=240, bg=BG_COLOR, highlightthickness=0)
strength_canvas.pack(pady=5)

def update_strength_meter(entropy):
    # Define 4 buckets and their respective colors
    buckets = [
        (28, "red"),
        (36, "orange"),
        (60, "yellow"),
        (128, "lightgreen"),
        (float("inf"), "green")
    ]
    width = 60  # 240px total divided by 4
    for i, (limit, color) in enumerate(buckets):
        # Fill up to the bucket reached
        fill = "black" if entropy < limit and i > 0 else color
        strength_canvas.create_rectangle(i*width, 0, (i+1)*width, 16, fill=fill, outline="")
    strength_canvas.update()

# In on_generate, after updating label color, add:
update_strength_meter(entropy)


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