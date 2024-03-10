import tkinter as tk

def on_select(option):
    selected_option.set(option)

# Function to handle button clicks
def button_click(option):
    on_select(option)
    root.destroy()  # Close the window after selection

def create_options():
    global root, selected_option  # Declare as global
    # Create the main window
    root = tk.Tk()
    root.title("Box Selection Menu")

    # Options
    options = ["Avant", "Droite", "Gauche", "Retour"]

    # Variable to store the selected option
    selected_option = tk.StringVar()

    # Create and place buttons for each option
    for option in options:
        button = tk.Button(root, text=option, command=lambda o=option: button_click(o))
        button.pack(pady=5)

    # Label to display the selected option
    result_label = tk.Label(root, textvariable=selected_option)
    result_label.pack(pady=10)

    # Start the main loop
    root.mainloop()

    # Access the selected option after the main loop
    print("Selected option:", selected_option.get())
    
    return selected_option.get()