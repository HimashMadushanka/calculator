import tkinter as tk
from tkinter import ttk
import math

# Button layout
button_values = [
    ["MC", "MR", "M+", "M-", "MS", "M▾"],
    ["%", "CE", "C", "⌫", "1/x", "x²", "√", "÷"],
    ["7", "8", "9", "×", "sin", "cos", "tan", "π"],
    ["4", "5", "6", "-", "log", "ln", "e", "xʸ"],
    ["1", "2", "3", "+", "(", ")", "!", "±"],
    ["0", ".", "=", "±", "Undo", "Redo", "Copy", "Paste"]
]

# Enhanced color scheme with gradients simulation
COLOURS = {
    "dark": {
        "bg": "#0D1117",
        "bg_secondary": "#161B22",
        "display": "#1C2128",
        "display_text": "#F0F6FC",
        "display_glow": "#58A6FF",
        "button_num": "#21262D",
        "button_num_hover": "#30363D",
        "button_op": "#FF6B35",
        "button_op_hover": "#FF8555",
        "button_func": "#238636",
        "button_func_hover": "#2EA043",
        "button_sci": "#8B5CF6",
        "button_sci_hover": "#A78BFA",
        "button_text": "#F0F6FC",
        "button_func_text": "#F0F6FC",
        "history": "#161B22",
        "history_text": "#8B949E",
        "accent": "#58A6FF",
        "border": "#30363D"
    },
    "light": {
        "bg": "#FFFFFF",
        "bg_secondary": "#F6F8FA",
        "display": "#FFFFFF",
        "display_text": "#1F2328",
        "display_glow": "#0969DA",
        "button_num": "#F6F8FA",
        "button_num_hover": "#E8EAED",
        "button_op": "#FF6B35",
        "button_op_hover": "#FF8555",
        "button_func": "#2DA44E",
        "button_func_hover": "#46A763",
        "button_sci": "#8B5CF6",
        "button_sci_hover": "#A78BFA",
        "button_text": "#1F2328",
        "button_func_text": "#FFFFFF",
        "history": "#F6F8FA",
        "history_text": "#656D76",
        "accent": "#0969DA",
        "border": "#D0D7DE"
    }
}

class StyledButton(tk.Button):
    """Custom button with hover effects"""
    def __init__(self, parent, **kwargs):
        self.default_bg = kwargs.get('bg', '#CCCCCC')
        self.hover_bg = kwargs.pop('hover_bg', self.default_bg)
        super().__init__(parent, **kwargs)
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        # Add subtle shadow effect with border
        self.config(
            relief="flat",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=kwargs.get('highlightbackground', '#000000'),
            highlightcolor=kwargs.get('highlightcolor', '#000000')
        )
    
    def on_enter(self, e):
        self.config(bg=self.hover_bg)
    
    def on_leave(self, e):
        self.config(bg=self.default_bg)

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("QuickCalc Pro")
        self.window.geometry("480x750")
        self.window.resizable(True, True)
        
        # Calculator state
        self.current_input = "0"
        self.previous_input = ""
        self.operator = None
        self.waiting_for_operand = False
        self.memory = 0
        self.history = []
        self.theme_mode = "dark"
        self.decimal_places = 6
        self.undo_stack = []
        self.redo_stack = []
        self.button_widgets = []
        
        # Animation state
        self.animation_running = False
        
        # Setup UI
        self.setup_ui()
        
        # Bind keyboard events
        self.bind_keys()
        
        # Center window
        self.center_window()
        
    def setup_ui(self):
        # Configure window background
        self.window.config(bg=self.get_colour("bg"))
        
        # Main frame with padding
        self.main_frame = tk.Frame(
            self.window, 
            bg=self.get_colour("bg"),
            padx=15,
            pady=15
        )
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title with emoji and gradient-like effect
        title_frame = tk.Frame(self.main_frame, bg=self.get_colour("bg"))
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.title_label = tk.Label(
            title_frame,
            text="✨ QuickCalc Pro ✨",
            font=("Segoe UI", 20, "bold"),
            bg=self.get_colour("bg"),
            fg=self.get_colour("accent"),
            pady=5
        )
        self.title_label.pack()
        
        # Display container with shadow effect
        display_container = tk.Frame(
            self.main_frame,
            bg=self.get_colour("border"),
            padx=2,
            pady=2
        )
        display_container.pack(fill=tk.X, pady=(0, 5))
        
        display_inner = tk.Frame(
            display_container,
            bg=self.get_colour("display"),
            padx=15,
            pady=10
        )
        display_inner.pack(fill=tk.BOTH, expand=True)
        
        # History display
        self.history_var = tk.StringVar()
        self.history_label = tk.Label(
            display_inner,
            textvariable=self.history_var,
            font=("Consolas", 10),
            bg=self.get_colour("display"),
            fg=self.get_colour("history_text"),
            anchor="e",
            height=1
        )
        self.history_label.pack(fill=tk.X)
        
        # Main display with glow effect
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        self.display_label = tk.Label(
            display_inner,
            textvariable=self.display_var,
            font=("Segoe UI", 40, "bold"),
            bg=self.get_colour("display"),
            fg=self.get_colour("display_text"),
            anchor="e",
            height=2
        )
        self.display_label.pack(fill=tk.X)
        
        # Memory indicator with icon
        memory_frame = tk.Frame(self.main_frame, bg=self.get_colour("bg"))
        memory_frame.pack(fill=tk.X, pady=(5, 10))
        
        self.memory_var = tk.StringVar()
        self.memory_label = tk.Label(
            memory_frame,
            textvariable=self.memory_var,
            font=("Segoe UI", 9, "bold"),
            bg=self.get_colour("bg"),
            fg=self.get_colour("accent"),
            anchor="w"
        )
        self.memory_label.pack(side=tk.LEFT)
        
        # Theme toggle button
        self.theme_btn = tk.Button(
            memory_frame,
            text="🌓",
            font=("Segoe UI", 12),
            bg=self.get_colour("button_num"),
            fg=self.get_colour("button_text"),
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=2,
            command=self.toggle_theme,
            cursor="hand2"
        )
        self.theme_btn.pack(side=tk.RIGHT)
        
        # Button frame
        self.button_frame = tk.Frame(self.main_frame, bg=self.get_colour("bg"))
        self.button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create buttons
        self.create_buttons()
        
        # Status bar with modern look
        status_frame = tk.Frame(
            self.window,
            bg=self.get_colour("bg_secondary"),
            height=30
        )
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready | F1: Help | F2: Theme")
        self.status_bar = tk.Label(
            status_frame,
            textvariable=self.status_var,
            bg=self.get_colour("bg_secondary"),
            fg=self.get_colour("history_text"),
            anchor="w",
            font=("Segoe UI", 9),
            padx=10
        )
        self.status_bar.pack(fill=tk.BOTH, expand=True)
        
    def get_colour(self, key):
        return COLOURS[self.theme_mode][key]
    
    def create_buttons(self):
        # Configure grid with weights
        for i in range(8):
            self.button_frame.grid_columnconfigure(i, weight=1, minsize=50)
        for i in range(6):
            self.button_frame.grid_rowconfigure(i, weight=1, minsize=50)
        
        self.button_widgets = []
        
        # Create buttons with enhanced styling
        for row_idx, row in enumerate(button_values):
            for col_idx, value in enumerate(row):
                if value:
                    bg_color = self.get_button_bg(value)
                    hover_color = self.get_button_hover_bg(value)
                    
                    btn = StyledButton(
                        self.button_frame,
                        text=value,
                        font=("Segoe UI", 13, "bold"),
                        bg=bg_color,
                        fg=self.get_button_fg(value),
                        hover_bg=hover_color,
                        activebackground=hover_color,
                        activeforeground=self.get_button_fg(value),
                        highlightbackground=self.get_colour("border"),
                        highlightcolor=self.get_colour("border"),
                        cursor="hand2",
                        command=lambda v=value: self.button_click(v)
                    )
                    
                    # Special styling for equals button
                    if value == "=":
                        btn.config(font=("Segoe UI", 16, "bold"))
                    
                    btn.grid(
                        row=row_idx,
                        column=col_idx,
                        padx=3,
                        pady=3,
                        sticky="nsew",
                        columnspan=self.get_colspan(value)
                    )
                    
                    self.button_widgets.append((btn, value))
    
    def get_button_bg(self, value):
        if value in ["+", "-", "×", "÷", "=", "xʸ"]:
            return self.get_colour("button_op")
        elif value in ["MC", "MR", "M+", "M-", "MS", "M▾", "CE", "C", "Undo", "Redo", "Copy", "Paste"]:
            return self.get_colour("button_func")
        elif value in ["sin", "cos", "tan", "log", "ln", "π", "e", "!", "(", ")", "1/x", "x²", "√"]:
            return self.get_colour("button_sci")
        else:
            return self.get_colour("button_num")
    
    def get_button_hover_bg(self, value):
        if value in ["+", "-", "×", "÷", "=", "xʸ"]:
            return self.get_colour("button_op_hover")
        elif value in ["MC", "MR", "M+", "M-", "MS", "M▾", "CE", "C", "Undo", "Redo", "Copy", "Paste"]:
            return self.get_colour("button_func_hover")
        elif value in ["sin", "cos", "tan", "log", "ln", "π", "e", "!", "(", ")", "1/x", "x²", "√"]:
            return self.get_colour("button_sci_hover")
        else:
            return self.get_colour("button_num_hover")
    
    def get_button_fg(self, value):
        if value in ["MC", "MR", "M+", "M-", "MS", "M▾", "CE", "C", "Undo", "Redo", "Copy", "Paste"]:
            return self.get_colour("button_func_text")
        else:
            return self.get_colour("button_text")
    
    def get_colspan(self, value):
        if value == "0":
            return 2
        return 1
    
    def animate_display(self):
        """Subtle flash animation on calculation"""
        if self.animation_running:
            return
        
        self.animation_running = True
        original_bg = self.display_label.cget("bg")
        glow_color = self.get_colour("display_glow")
        
        def flash(count=0):
            if count < 2:
                current = glow_color if count % 2 == 0 else original_bg
                self.display_label.config(bg=current)
                self.window.after(100, lambda: flash(count + 1))
            else:
                self.display_label.config(bg=original_bg)
                self.animation_running = False
        
        flash()
    
    def save_state(self):
        """Save current state to undo stack"""
        self.undo_stack.append({
            'current_input': self.current_input,
            'previous_input': self.previous_input,
            'operator': self.operator,
            'memory': self.memory
        })
        if len(self.undo_stack) > 50:
            self.undo_stack.pop(0)
        self.redo_stack.clear()
    
    def button_click(self, value):
        self.save_state()
        
        if value in "0123456789":
            self.input_digit(value)
        elif value == ".":
            self.input_decimal()
        elif value in ["+", "-", "×", "÷", "xʸ"]:
            self.input_operator(value)
        elif value == "=":
            self.calculate_result()
            self.animate_display()
        elif value == "C":
            self.clear_all()
        elif value == "CE":
            self.clear_entry()
        elif value == "⌫":
            self.backspace()
        elif value == "±":
            self.toggle_sign()
        elif value == "%":
            self.percentage()
        elif value in ["1/x", "x²", "√", "sin", "cos", "tan", "log", "ln", "!", "π", "e"]:
            self.scientific_operation(value)
        elif value in ["MC", "MR", "M+", "M-", "MS"]:
            self.memory_operation(value)
        elif value == "M▾":
            self.show_memory_menu()
        elif value == "(":
            self.input_parenthesis("(")
        elif value == ")":
            self.input_parenthesis(")")
        elif value == "Undo":
            self.undo()
        elif value == "Redo":
            self.redo()
        elif value == "Copy":
            self.copy_to_clipboard()
        elif value == "Paste":
            self.paste_from_clipboard()
        
        self.update_display()
        self.update_status(f"✓ {value}")
    
    def input_digit(self, digit):
        if self.waiting_for_operand or self.current_input == "0":
            self.current_input = digit
            self.waiting_for_operand = False
        else:
            self.current_input += digit
    
    def input_decimal(self):
        if "." not in self.current_input:
            self.current_input += "."
    
    def input_operator(self, op):
        if self.operator and not self.waiting_for_operand:
            self.calculate_result()
        
        self.previous_input = self.current_input
        self.operator = op
        self.waiting_for_operand = True
        self.add_history(f"{self.previous_input} {op}")
    
    def input_parenthesis(self, paren):
        if paren == "(":
            if self.current_input == "0" or self.waiting_for_operand:
                self.current_input = "("
            else:
                self.current_input += "×("
        else:
            self.current_input += ")"
    
    def calculate_result(self):
        if not self.operator or self.waiting_for_operand:
            return
        
        try:
            expression = f"{self.previous_input} {self.operator} {self.current_input}"
            expression = expression.replace("×", "*").replace("÷", "/").replace("xʸ", "**")
            
            if "(" in expression or ")" in expression:
                result = eval(expression, {"__builtins__": None}, 
                            {"sin": math.sin, "cos": math.cos, "tan": math.tan,
                             "log": math.log10, "ln": math.log, "pi": math.pi, 
                             "e": math.e, "sqrt": math.sqrt})
            else:
                result = eval(expression)
            
            self.current_input = self.format_number(result)
            self.add_history(f"{expression} = {self.current_input}")
            
            self.previous_input = ""
            self.operator = None
            self.waiting_for_operand = True
            
        except ZeroDivisionError:
            self.current_input = "Cannot divide by zero"
            self.previous_input = ""
            self.operator = None
        except Exception as e:
            self.current_input = "Error"
            self.previous_input = ""
            self.operator = None
    
    def scientific_operation(self, op):
        try:
            value = float(self.current_input)
            if op == "1/x":
                result = 1 / value
            elif op == "x²":
                result = value ** 2
            elif op == "√":
                result = math.sqrt(value)
            elif op == "sin":
                result = math.sin(math.radians(value))
            elif op == "cos":
                result = math.cos(math.radians(value))
            elif op == "tan":
                result = math.tan(math.radians(value))
            elif op == "log":
                result = math.log10(value)
            elif op == "ln":
                result = math.log(value)
            elif op == "!":
                result = math.factorial(int(value))
            elif op == "π":
                result = math.pi
            elif op == "e":
                result = math.e
            
            if op not in ["π", "e"]:
                self.add_history(f"{op}({value}) = {result}")
            self.current_input = self.format_number(result)
            
        except ValueError:
            self.current_input = "Error"
        except OverflowError:
            self.current_input = "Overflow"
    
    def memory_operation(self, op):
        try:
            current = float(self.current_input)
            if op == "MC":
                self.memory = 0
                self.update_memory_indicator()
            elif op == "MR":
                self.current_input = self.format_number(self.memory)
            elif op == "M+":
                self.memory += current
            elif op == "M-":
                self.memory -= current
            elif op == "MS":
                self.memory = current
            
            self.update_memory_indicator()
            self.add_history(f"Memory {op}: {self.memory}")
            
        except ValueError:
            pass
    
    def show_memory_menu(self):
        menu = tk.Menu(self.window, tearoff=0, 
                      bg=self.get_colour("bg_secondary"),
                      fg=self.get_colour("display_text"))
        menu.add_command(label=f"📌 Memory: {self.memory}", state="disabled")
        menu.add_separator()
        menu.add_command(label="Clear Memory", command=lambda: self.memory_operation("MC"))
        menu.add_command(label="View History", command=self.show_memory_history)
        
        x = self.window.winfo_pointerx()
        y = self.window.winfo_pointery()
        menu.post(x, y)
    
    def show_memory_history(self):
        history_window = tk.Toplevel(self.window)
        history_window.title("📜 Memory History")
        history_window.geometry("350x450")
        history_window.config(bg=self.get_colour("bg"))
        
        text = tk.Text(
            history_window, 
            wrap=tk.WORD,
            bg=self.get_colour("display"),
            fg=self.get_colour("display_text"),
            font=("Consolas", 10),
            padx=10,
            pady=10
        )
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text.insert(tk.END, "📊 Memory History\n\n")
        text.insert(tk.END, f"Current: {self.memory}\n")
        text.insert(tk.END, "─" * 40 + "\n\n")
        
        for i, entry in enumerate(reversed(self.history[-20:]), 1):
            text.insert(tk.END, f"{i}. {entry}\n")
        
        text.config(state="disabled")
    
    def clear_all(self):
        self.current_input = "0"
        self.previous_input = ""
        self.operator = None
        self.waiting_for_operand = False
    
    def clear_entry(self):
        self.current_input = "0"
    
    def backspace(self):
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
    
    def toggle_sign(self):
        if self.current_input != "0":
            if self.current_input[0] == "-":
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
    
    def percentage(self):
        try:
            value = float(self.current_input) / 100
            self.current_input = self.format_number(value)
            self.add_history(f"{self.current_input}%")
        except ValueError:
            pass
    
    def undo(self):
        if self.undo_stack:
            state = self.undo_stack.pop()
            self.redo_stack.append({
                'current_input': self.current_input,
                'previous_input': self.previous_input,
                'operator': self.operator,
                'memory': self.memory
            })
            
            self.current_input = state['current_input']
            self.previous_input = state['previous_input']
            self.operator = state['operator']
            self.memory = state['memory']
            
            self.update_display()
            self.update_memory_indicator()
            self.update_status("↩ Undo")
    
    def redo(self):
        if self.redo_stack:
            state = self.redo_stack.pop()
            self.undo_stack.append({
                'current_input': self.current_input,
                'previous_input': self.previous_input,
                'operator': self.operator,
                'memory': self.memory
            })
            
            self.current_input = state['current_input']
            self.previous_input = state['previous_input']
            self.operator = state['operator']
            self.memory = state['memory']
            
            self.update_display()
            self.update_memory_indicator()
            self.update_status("↪ Redo")
    
    def copy_to_clipboard(self):
        try:
            self.window.clipboard_clear()
            self.window.clipboard_append(self.current_input)
            self.update_status("📋 Copied!")
        except:
            self.update_status("❌ Clipboard error")
    
    def paste_from_clipboard(self):
        try:
            clipboard = self.window.clipboard_get()
            value = float(clipboard)
            self.current_input = self.format_number(value)
            self.update_status("📋 Pasted")
        except:
            self.update_status("❌ Invalid clipboard content")
    
    def format_number(self, num):
        try:
            if isinstance(num, str):
                return num
            
            if num == int(num):
                return str(int(num))
            
            formatted = f"{num:.{self.decimal_places}f}"
            formatted = formatted.rstrip('0').rstrip('.') if '.' in formatted else formatted
            
            return formatted
        except:
            return str(num)
    
    def add_history(self, entry):
        self.history.append(entry)
        if len(self.history) > 100:
            self.history.pop(0)
        
        display_history = self.history[-2:]
        self.history_var.set(" │ ".join(display_history))
    
    def update_display(self):
        self.display_var.set(self.current_input)
        
        # Dynamic font sizing
        length = len(self.current_input)
        if length <= 10:
            font_size = 40
        elif length <= 15:
            font_size = 32
        elif length <= 20:
            font_size = 24
        else:
            font_size = 18
        
        self.display_label.config(font=("Segoe UI", font_size, "bold"))
    
    def update_memory_indicator(self):
        if self.memory != 0:
            self.memory_var.set(f"💾 M: {self.format_number(self.memory)}")
        else:
            self.memory_var.set("")
    
    def update_status(self, message):
        self.status_var.set(message)
        self.window.after(3000, lambda: self.status_var.set("Ready | F1: Help | F2: Theme"))
    
    def bind_keys(self):
        # Number keys (both regular and numpad)
        for i in range(10):
            self.window.bind(str(i), lambda e, digit=str(i): self.button_click(digit))
            self.window.bind(f"<KP_{i}>", lambda e, digit=str(i): self.button_click(digit))
        
        # Basic operators (multiple bindings for convenience)
        self.window.bind("+", lambda e: self.button_click("+"))
        self.window.bind("<KP_Add>", lambda e: self.button_click("+"))
        self.window.bind("<Shift-equal>", lambda e: self.button_click("+"))  # Shift + =
        
        self.window.bind("-", lambda e: self.button_click("-"))
        self.window.bind("<KP_Subtract>", lambda e: self.button_click("-"))
        
        self.window.bind("*", lambda e: self.button_click("×"))
        self.window.bind("<KP_Multiply>", lambda e: self.button_click("×"))
        self.window.bind("<Shift-8>", lambda e: self.button_click("×"))  # Shift + 8
        
        self.window.bind("/", lambda e: self.button_click("÷"))
        self.window.bind("<KP_Divide>", lambda e: self.button_click("÷"))
        
        # Equals/Enter
        self.window.bind("<Return>", lambda e: self.button_click("="))
        self.window.bind("<KP_Enter>", lambda e: self.button_click("="))
        self.window.bind("=", lambda e: self.button_click("="))
        
        # Decimal point
        self.window.bind(".", lambda e: self.button_click("."))
        self.window.bind("<KP_Decimal>", lambda e: self.button_click("."))
        self.window.bind(",", lambda e: self.button_click("."))  # Alternative decimal
        
        # Backspace and delete
        self.window.bind("<BackSpace>", lambda e: self.button_click("⌫"))
        self.window.bind("<Delete>", lambda e: self.button_click("CE"))
        
        # Clear operations
        self.window.bind("<Escape>", lambda e: self.button_click("C"))
        self.window.bind("c", lambda e: self.button_click("C"))
        self.window.bind("C", lambda e: self.button_click("C"))
        
        # Percentage
        self.window.bind("%", lambda e: self.button_click("%"))
        self.window.bind("<Shift-5>", lambda e: self.button_click("%"))
        
        # Parentheses
        self.window.bind("(", lambda e: self.button_click("("))
        self.window.bind(")", lambda e: self.button_click(")"))
        self.window.bind("<Shift-9>", lambda e: self.button_click("("))
        self.window.bind("<Shift-0>", lambda e: self.button_click(")"))
        
        # Sign toggle
        self.window.bind("_", lambda e: self.button_click("±"))
        
        # Scientific functions (case insensitive)
        self.window.bind("s", lambda e: self.button_click("sin"))
        self.window.bind("S", lambda e: self.button_click("sin"))
        
        # Power functions
        self.window.bind("^", lambda e: self.button_click("xʸ"))
        self.window.bind("<Shift-6>", lambda e: self.button_click("xʸ"))
        
        self.window.bind("q", lambda e: self.button_click("x²"))
        self.window.bind("Q", lambda e: self.button_click("x²"))
        
        self.window.bind("r", lambda e: self.button_click("√"))
        self.window.bind("R", lambda e: self.button_click("√"))
        
        # Constants
        self.window.bind("p", lambda e: self.button_click("π"))
        self.window.bind("P", lambda e: self.button_click("π"))
        
        self.window.bind("e", lambda e: self.button_click("e"))
        self.window.bind("E", lambda e: self.button_click("e"))
        
        # Factorial
        self.window.bind("!", lambda e: self.button_click("!"))
        self.window.bind("<Shift-1>", lambda e: self.button_click("!"))
        
        # Control shortcuts (clipboard and undo/redo)
        self.window.bind("<Control-z>", lambda e: self.button_click("Undo"))
        self.window.bind("<Control-Z>", lambda e: self.button_click("Undo"))
        
        self.window.bind("<Control-y>", lambda e: self.button_click("Redo"))
        self.window.bind("<Control-Y>", lambda e: self.button_click("Redo"))
        self.window.bind("<Control-Shift-z>", lambda e: self.button_click("Redo"))
        self.window.bind("<Control-Shift-Z>", lambda e: self.button_click("Redo"))
        
        self.window.bind("<Control-c>", lambda e: self.button_click("Copy"))
        self.window.bind("<Control-C>", lambda e: self.button_click("Copy"))
        
        self.window.bind("<Control-v>", lambda e: self.button_click("Paste"))
        self.window.bind("<Control-V>", lambda e: self.button_click("Paste"))
        
        # Select all (copy)
        self.window.bind("<Control-a>", lambda e: self.button_click("Copy"))
        self.window.bind("<Control-A>", lambda e: self.button_click("Copy"))
        
        # Memory shortcuts
        self.window.bind("<Control-m>", lambda e: self.button_click("MS"))  # Memory Store
        self.window.bind("<Control-M>", lambda e: self.button_click("MS"))
        
        self.window.bind("<Control-r>", lambda e: self.button_click("MR"))  # Memory Recall
        self.window.bind("<Control-R>", lambda e: self.button_click("MR"))
        
        self.window.bind("<Control-p>", lambda e: self.button_click("M+"))  # Memory Plus
        self.window.bind("<Control-P>", lambda e: self.button_click("M+"))
        
        self.window.bind("<Control-l>", lambda e: self.button_click("MC"))  # Memory Clear
        self.window.bind("<Control-L>", lambda e: self.button_click("MC"))
        
        # Function keys
        self.window.bind("<F1>", lambda e: self.show_help())
        self.window.bind("<F2>", lambda e: self.toggle_theme())
        self.window.bind("<F9>", lambda e: self.button_click("C"))  # Quick clear
        
        # Alt shortcuts for advanced functions
        self.window.bind("<Alt-s>", lambda e: self.button_click("sin"))
        self.window.bind("<Alt-S>", lambda e: self.button_click("sin"))
        
        self.window.bind("<Alt-c>", lambda e: self.button_click("cos"))
        self.window.bind("<Alt-C>", lambda e: self.button_click("cos"))
        
        self.window.bind("<Alt-t>", lambda e: self.button_click("tan"))
        self.window.bind("<Alt-T>", lambda e: self.button_click("tan"))
        
        self.window.bind("<Alt-l>", lambda e: self.button_click("log"))
        self.window.bind("<Alt-L>", lambda e: self.button_click("log"))
        
        self.window.bind("<Alt-n>", lambda e: self.button_click("ln"))
        self.window.bind("<Alt-N>", lambda e: self.button_click("ln"))
        
        # Quick reciprocal
        self.window.bind("i", lambda e: self.button_click("1/x"))
        self.window.bind("I", lambda e: self.button_click("1/x"))
    
    def toggle_theme(self):
        self.theme_mode = "light" if self.theme_mode == "dark" else "dark"
        self.refresh_ui()
        self.update_status(f"🎨 Theme: {self.theme_mode.title()}")
    
    def refresh_ui(self):
        # Update all colors
        self.window.config(bg=self.get_colour("bg"))
        self.main_frame.config(bg=self.get_colour("bg"))
        self.title_label.config(bg=self.get_colour("bg"), fg=self.get_colour("accent"))
        self.history_label.config(bg=self.get_colour("display"), fg=self.get_colour("history_text"))
        self.display_label.config(bg=self.get_colour("display"), fg=self.get_colour("display_text"))
        self.memory_label.config(bg=self.get_colour("bg"), fg=self.get_colour("accent"))
        self.theme_btn.config(bg=self.get_colour("button_num"), fg=self.get_colour("button_text"))
        self.button_frame.config(bg=self.get_colour("bg"))
        self.status_bar.config(bg=self.get_colour("bg_secondary"), fg=self.get_colour("history_text"))
        
        # Update all buttons
        for btn, value in self.button_widgets:
            bg_color = self.get_button_bg(value)
            hover_color = self.get_button_hover_bg(value)
            btn.default_bg = bg_color
            btn.hover_bg = hover_color
            btn.config(
                bg=bg_color,
                fg=self.get_button_fg(value),
                activebackground=hover_color,
                highlightbackground=self.get_colour("border")
            )
    
    def show_help(self):
        help_window = tk.Toplevel(self.window)
        help_window.title("📚 QuickCalc Pro - Help")
        help_window.geometry("550x500")
        help_window.config(bg=self.get_colour("bg"))
        
        # Create scrollable text widget
        text_frame = tk.Frame(help_window, bg=self.get_colour("bg"))
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            bg=self.get_colour("display"),
            fg=self.get_colour("display_text"),
            font=("Segoe UI", 10),
            padx=15,
            pady=15,
            relief="flat",
            borderwidth=0
        )
        
        scrollbar = tk.Scrollbar(text_frame, command=text.yview)
        text.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        help_text = """✨ QUICKCALC PRO - HELP GUIDE ✨

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⌨️ KEYBOARD SHORTCUTS

Numbers & Operators:
  • 0-9 or Numpad 0-9: Number input
  • +, -, *, /: Basic operators
  • Numpad +, -, *, /: Alternative operators
  • = or Enter or Numpad Enter: Calculate
  • . or , or Numpad .: Decimal point
  • %: Percentage

Math Operations:
  • ^ or Shift+6: Power (xʸ)
  • Q: Square (x²)
  • R: Square root (√)
  • I: Reciprocal (1/x)
  • P: Pi (π)
  • E: Euler's number (e)
  • ! or Shift+1: Factorial
  • ( ) or Shift+9/0: Parentheses

Scientific Functions (Alt+Key):
  • Alt+S: Sine
  • Alt+C: Cosine
  • Alt+T: Tangent
  • Alt+L: Logarithm (log)
  • Alt+N: Natural log (ln)

Editing:
  • Backspace: Delete last digit (⌫)
  • Delete: Clear entry (CE)
  • Escape or C: Clear all (C)

Clipboard & Undo:
  • Ctrl+Z: Undo last action
  • Ctrl+Y or Ctrl+Shift+Z: Redo
  • Ctrl+C or Ctrl+A: Copy result
  • Ctrl+V: Paste number

Memory Shortcuts:
  • Ctrl+M: Memory Store (MS)
  • Ctrl+R: Memory Recall (MR)
  • Ctrl+P: Memory Plus (M+)
  • Ctrl+L: Memory Clear (MC)

Function Keys:
  • F1: Show this help window
  • F2: Toggle dark/light theme
  • F9: Quick clear all

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💾 MEMORY FUNCTIONS

  • MC or Ctrl+L: Clear memory
  • MR or Ctrl+R: Recall memory value
  • M+ or Ctrl+P: Add to memory
  • M-: Subtract from memory
  • MS or Ctrl+M: Store in memory
  • M▾: Open memory menu with history

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔬 SCIENTIFIC FUNCTIONS

Trigonometry (in degrees):
  • sin: Sine function
  • cos: Cosine function
  • tan: Tangent function

Logarithms:
  • log: Base-10 logarithm
  • ln: Natural logarithm (base-e)

Power & Roots:
  • x²: Square
  • √: Square root
  • xʸ: Power (x to the power of y)
  • 1/x: Reciprocal

Constants & Other:
  • π: Pi (3.14159...)
  • e: Euler's number (2.71828...)
  • !: Factorial (integers only)
  • ( ): Parentheses for grouping

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 TIPS & TRICKS

  1. The display automatically adjusts font size
     based on the length of your result
  
  2. History shows your last 2 calculations
     at the top of the display
  
  3. Use parentheses for complex expressions
     Example: (5 + 3) × (10 - 2)
  
  4. The equals button (=) is larger for
     easy access
  
  5. Hover over buttons to see the smooth
     color transition effect
  
  6. Memory indicator shows 💾 when memory
     contains a non-zero value
  
  7. Status messages appear at the bottom
     and auto-clear after 3 seconds

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 THEMES

QuickCalc Pro includes two beautiful themes:
  • Dark Mode (default): Easy on the eyes
  • Light Mode: Classic bright interface

Toggle anytime with F2 or the 🌓 button!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Created with ❤️ by QuickCalc Pro Team
Version 2.0 - Enhanced Edition
"""
        
        text.insert("1.0", help_text)
        text.config(state="disabled")
        
        # Close button
        btn_frame = tk.Frame(help_window, bg=self.get_colour("bg"))
        btn_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        close_btn = StyledButton(
            btn_frame,
            text="✓ Got it!",
            font=("Segoe UI", 11, "bold"),
            bg=self.get_colour("button_func"),
            fg=self.get_colour("button_func_text"),
            hover_bg=self.get_colour("button_func_hover"),
            padx=30,
            pady=10,
            cursor="hand2",
            command=help_window.destroy
        )
        close_btn.pack()
    
    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = Calculator()
    app.run()