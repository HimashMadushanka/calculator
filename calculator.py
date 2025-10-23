import tkinter as tk
from tkinter import font as tkfont
import math

button_values = [
    ["AC", "+/-", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="]
]

right_symbols = ["+", "×", "-", "÷", "="]
top_symbols = ["AC", "+/-", "%"]

row_count = len(button_values)
column_count = len(button_values[0])
colour_light_gray = "#D4D4D2"
colour_black = "#1C1C1C"
colour_dark_gray = "#505050"
colour_orange = "#FF9500"
colour_white = "white"

# Window setup
window = tk.Tk()
window.title("Calculator")
window.resizable(True, True)
window.configure(bg="#1a1a1a")

# Main frame with rounded effect
frame = tk.Frame(
    window,
    background="#2C2C2C",
    highlightbackground="#EA7FF8",
    highlightthickness=3,
    relief="flat"
)

# Title with gradient-like effect
title_label = tk.Label(
    window,
    text=" 😊 QuickCalc 😊 ",
    font=("Arial", 20, "bold"),
    background="#040C53",
    foreground="white",
    pady=15,
    padx=10,
    relief="flat"
)
title_label.pack(side="top", fill="x")

# Display label
label_var = tk.StringVar()
label_var.set("0")

label = tk.Label(
    frame,
    textvariable=label_var,
    font=("Arial", 45, "bold"),
    background=colour_black,
    foreground=colour_white,
    anchor="e",
    width=column_count,
    height=2,
    bd=0,
    relief="flat",
    padx=20,
    pady=10
)

label.grid(row=0, column=0, columnspan=column_count, sticky="nsew", pady=(10, 15))

# Store buttons for animations
buttons = []

# A+B, A-B, A*B, A/B
A = "0"
operator = None
B = None


def clear_all():
    global A, B, operator
    A = "0"
    operator = None
    B = None


def remove_zero_decimal(num):
    if num % 1 == 0:
        num = int(num)
    return str(num)


def update_label_text(text):
    length = len(text)
    if length <= 9:
        label.config(font=("Arial", 45, "bold"))
    elif length <= 14:
        label.config(font=("Arial", 35, "bold"))
    else:
        label.config(font=("Arial", 25, "bold"))
    label_var.set(text)


def animate_button_press(button):
    """Smooth button press animation"""
    original_relief = button.cget("relief")
    button.config(relief="sunken")
    window.after(100, lambda: button.config(relief=original_relief))


def on_enter(e, button, color):
    """Hover effect"""
    button.config(background=color, cursor="hand2")


def on_leave(e, button, original_color):
    """Remove hover effect"""
    button.config(background=original_color)


def button_clicked(value):
    global right_symbols, top_symbols, label, A, B, operator

    if value == "√":
        try:
            current_num = float(label_var.get())
            if current_num < 0:
                update_label_text("Error")
            else:
                sqrt_result = math.sqrt(current_num)
                update_label_text(remove_zero_decimal(sqrt_result))
        except ValueError:
            update_label_text("Error")

    elif value in right_symbols:
        if value == "=":
            if A is not None and operator is not None:
                B = label_var.get()
                NumA = float(A)
                NumB = float(B)

                if operator == "+":
                    update_label_text(remove_zero_decimal(NumA + NumB))
                elif operator == "-":
                    update_label_text(remove_zero_decimal(NumA - NumB))
                elif operator == "×":
                    update_label_text(remove_zero_decimal(NumA * NumB))
                elif operator == "÷":
                    if NumB != 0:
                        update_label_text(remove_zero_decimal(NumA / NumB))
                    else:
                        update_label_text("Error")

                clear_all()

        elif value in "+-×÷":
            if operator is None:
                A = label_var.get()
                update_label_text("0")
                B = "0"
                operator = value

    elif value in top_symbols:
        if value == "AC":
            clear_all()
            update_label_text("0")

        elif value == "+/-":
            result = float(label_var.get()) * -1
            update_label_text(remove_zero_decimal(result))

        elif value == "%":
            result = float(label_var.get()) / 100
            update_label_text(remove_zero_decimal(result))

    else:
        if value == ".":
            if "." not in label_var.get():
                update_label_text(label_var.get() + value)

        elif value in "0123456789":
            if label_var.get() == "0":
                update_label_text(value)
            else:
                update_label_text(label_var.get() + value)


# Create buttons with smooth styling
for row in range(row_count):
    for column in range(column_count):
        value = button_values[row][column]
        
        button = tk.Button(
            frame,
            text=value,
            font=("Arial", 24, "bold"),
            width=4,
            height=1,
            bd=0,
            relief="flat",
            command=lambda v=value: [animate_button_press([b for b in buttons if b.cget("text") == v][0]), button_clicked(v)]
        )

        # Button coloring with hover effects
        if value in top_symbols:
            bg_color = colour_light_gray
            hover_color = "#E5E5E5"
            button.config(
                foreground=colour_black,
                background=bg_color,
                activebackground=hover_color,
                highlightthickness=0
            )
            button.bind("<Enter>", lambda e, b=button, c=hover_color: on_enter(e, b, c))
            button.bind("<Leave>", lambda e, b=button, c=bg_color: on_leave(e, b, c))

        elif value in right_symbols:
            bg_color = colour_orange
            hover_color = "#FFB84D"
            button.config(
                foreground=colour_white,
                background=bg_color,
                activebackground=hover_color,
                highlightthickness=0
            )
            button.bind("<Enter>", lambda e, b=button, c=hover_color: on_enter(e, b, c))
            button.bind("<Leave>", lambda e, b=button, c=bg_color: on_leave(e, b, c))

        else:
            bg_color = colour_dark_gray
            hover_color = "#6e6e6e"
            button.config(
                foreground=colour_white,
                background=bg_color,
                activebackground=hover_color,
                highlightthickness=0
            )
            button.bind("<Enter>", lambda e, b=button, c=hover_color: on_enter(e, b, c))
            button.bind("<Leave>", lambda e, b=button, c=bg_color: on_leave(e, b, c))

        button.grid(row=row + 1, column=column, padx=3, pady=3, sticky="nsew")
        buttons.append(button)

# Grid configuration
for r in range(row_count + 1):
    frame.grid_rowconfigure(r, weight=1)
for c in range(column_count):
    frame.grid_columnconfigure(c, weight=1)

frame.pack(expand=True, fill="both", padx=10, pady=10)


# Dynamic font resizing
def resize_fonts(event):
    width = event.width
    height = event.height

    new_label_font_size = max(25, int(width / 15))
    label.config(font=("Arial", new_label_font_size, "bold"))

    new_button_font_size = max(18, int(width / 20))

    for child in frame.winfo_children():
        if isinstance(child, tk.Button):
            child.config(font=("Arial", new_button_font_size, "bold"))

window.bind("<Configure>", resize_fonts)

# Center the window
window.update()
window_width = 400
window_height = 600
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

window.mainloop()