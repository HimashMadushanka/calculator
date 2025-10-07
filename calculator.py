import tkinter
import math

button_values =[
    ["AC" , "+/-" , "%" , "÷"],
    ["7" , "8" , "9" , "×"],
    ["4" , "5" , "6" , "-"],
    ["1" , "2" , "3" , "+"],
    ["0" , "." , "√" , "="]
]

right_symbols = ["+" , "×" , "-" , "÷" , "="]
top_symbols=["AC" , "+/-" , "%"]

row_count = len(button_values) 
column_count = len(button_values[0]) 
colour_light_gray = "#D4D4D2"
colour_black = "#1C1C1C"
colour_dark_gray ="#505050"
colour_orange = "#FF9500"
colour_white = "white"



#window setup

window = tkinter.Tk() 
window.title("Calculator")
window.resizable(True , True)

frame = tkinter.Frame(
    window,background="#2C2C2C",
    highlightbackground="#EA7FF8",
    highlightthickness=60
    )



#title

title_label = tkinter.Label(
    window,  
    text=" 😊 QuickCalc 😊 ",        
    font=("Arial", 20, "bold"),
    background="#040C53",         
    foreground="white",
    pady=10,
    padx=10 
    )

title_label.pack(side="top", fill="x")

label_var = tkinter.StringVar()
label_var.set("0")

label = tkinter.Label(
    frame,
    textvariable=label_var,
    font=("Arial", 45),
    background=colour_black,
    foreground=colour_white,
    anchor="e",
    width=column_count,
    height=2,
    bd=4,
    relief="sunken" 
    )


label.grid(row=0 , column=0, columnspan=column_count, sticky="nsew", pady=10)
for row in range(row_count):
    for column in range(column_count):
        value = button_values[row][column]
        button =tkinter.Button(  frame,
            text=value,
            font=("Arial", 20),     
            width=4,                
            height=1,               
            bd=2,                   
            relief="groove",          
            command=lambda value=value: button_clicked(value))
        


# Button coloring

        if value in top_symbols:
            button.config(
                foreground=colour_black,
                background=colour_light_gray,
                activebackground="#E5E5E5",
                highlightthickness=0
            )
        elif value in right_symbols:
            button.config(
                foreground=colour_white,
                background=colour_orange,
                activebackground="#FFB84D",
                highlightthickness=0
            )


# Numbers and others

        else:  
            button.config(
                foreground=colour_white,
                background=colour_dark_gray,
                activebackground="#6e6e6e",
                highlightthickness=0
            )

        button.grid(row=row+1, column=column, padx=2, pady=2 ,)
        
        if value in top_symbols:
            button.config(foreground=colour_black,background=colour_light_gray)
        elif value in right_symbols:
            button.config(foreground=colour_white,background=colour_orange)
        else:
            button.config(foreground=colour_white,background=colour_dark_gray)
            
        button.grid(row=row+1, column=column, padx=2, pady=2, sticky="nsew")

        
for r in range(row_count + 1):  # +1 for label row
    frame.grid_rowconfigure(r, weight=1)
for c in range(column_count):
    frame.grid_columnconfigure(c, weight=1)

frame.pack(expand=True, fill="both")


# A+B , A-B , A*B , A/B

A = "0" 
operator = None
B = None

def clear_all():
    global A,B, operator
    A = "0" 
    operator = None
    B = None

def remove_zero_decimal(num):
    if num % 1==0:
        num = int(num)
    return str(num)
 
def update_label_text(text):
    length = len(text)
    if length <= 9:
        label.config(font=("Arial", 20))
    elif length <= 14:
        label.config(font=("Arial", 20))
    else:
        label.config(font=("Arial", 20))
    label_var.set(text)


def button_clicked(value):
    global right_symbols, top_symbols,label, A, B, operator 


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
                   update_label_text(remove_zero_decimal(NumA / NumB))
               
               clear_all()
               

       elif value in "+-×÷":
         if operator is None:
                A = label_var.get()
                update_label_text("0") 
                B="0"
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



# dinamic mode 

def resize_fonts(event):
    width = event.width
    height = event.height

    
    new_label_font_size = max(20, int(width / 20))  # min size 20
    label.config(font=("Arial", new_label_font_size))

    new_button_font_size = max(20, int(width / 20))
    
    
    for child in frame.winfo_children():
        if isinstance(child, tkinter.Button):
            child.config(font=("Arial", new_button_font_size))

window.bind("<Configure>", resize_fonts)



# center the window

window.update() 
window_width= window.winfo_width()
window_height= window.winfo_height()
screen_width= window.winfo_screenwidth()
screen_height= window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")


window.mainloop()