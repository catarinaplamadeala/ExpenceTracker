import customtkinter as ctk
import csv
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("675x400")
app.title("Expense Tracker")

# Left frame for Add Expense section
add_expense_frame = ctk.CTkFrame(app, width=230, height=300, fg_color="#333333", corner_radius=15)
add_expense_frame.place(x=20, y=20)

# Labels and entry fields for adding new expense
ctk.CTkLabel(add_expense_frame, text="Add New Expense", font=("Century Gothic", 16, 'bold'), text_color="white").place(x=40, y=10)

expense_title_label = ctk.CTkLabel(add_expense_frame, text="Expense Title", font=("Century Gothic", 12), text_color="white")
expense_title_label.place(x=20, y=70)

expense_title = ctk.CTkEntry(add_expense_frame, font=("Century Gothic", 12), width=100, placeholder_text="Title")
expense_title.place(x=110, y=70)
expense_title.focus()

expense_amount_label = ctk.CTkLabel(add_expense_frame, text="Amount (€)", font=("Century Gothic", 12), text_color="white")
expense_amount_label.place(x=20, y=110)

expense_amount = ctk.CTkEntry(add_expense_frame, font=("Century Gothic", 12), width=100, placeholder_text="€")
expense_amount.place(x=110, y=110)

select_category = ctk.CTkLabel(add_expense_frame, text="Category", font=("Century Gothic", 12), text_color="white")
select_category.place(x=20, y=150)

combobox = ctk.CTkComboBox(master=add_expense_frame, values=["Personal", "Entertainment", "Food", "Travel", "Rent", "Utilities"], font=("Century Gothic", 12), width=100)
combobox.place(x=110, y=150)
combobox.set("")  # set initial value

calendar_text = ctk.CTkLabel(add_expense_frame, text='Date', font=("Century Gothic", 12), text_color="white")
calendar_text.place(x=20, y=190)

calendar = ctk.CTkEntry(add_expense_frame, placeholder_text="DD/MM/YYYY", font=("Century Gothic", 12), width=100)
calendar.place(x=110, y=190)

def add_new_expense():
    title = expense_title.get()
    amount = expense_amount.get()
    category = combobox.get()
    date = calendar.get()

    with open('expenses.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([title, amount, category, date])

    expense_title.delete(0, 'end')
    expense_amount.delete(0, 'end')
    combobox.set("")
    calendar.delete(0, 'end')

    update_table()
    update_total()

add_expense_button = ctk.CTkButton(add_expense_frame, text="Add Expense", font=("Century Gothic", 12), command=add_new_expense)
add_expense_button.place(x=45, y=255)

# Right frame for displaying expenses table
table_frame = ctk.CTkFrame(app, width=600, height=350, fg_color="#666666", corner_radius=15)
table_frame.place(x=260, y=20)

# Function to update the expense table
def update_table():
    # Clear existing table content
    for widget in table_frame.winfo_children():
        widget.destroy()

    # Column headers
    columns = ["Title", "Amount(€)", "Category", "Date"]
    for i, column in enumerate(columns):
        header_frame = ctk.CTkFrame(table_frame, width=100, height=30, fg_color="#666666", border_width=1)
        header_frame.grid(row=0, column=i, padx=15, pady=8)
        header_label = ctk.CTkLabel(header_frame, text=column, font=("Century Gothic", 14, 'bold'), text_color="white")
        header_label.pack(fill="both", expand=True)

    # Check if expenses.csv is empty
    if os.path.getsize('expenses.csv') == 0:
        no_expenses_label = ctk.CTkLabel(table_frame, text="No expenses", font=("Century Gothic", 14), text_color="white")
        no_expenses_label.grid(row=1, column=0, columnspan=len(columns), padx=15, pady=8)
        return

    # Read expenses from CSV and display them
    with open('expenses.csv', mode='r') as file:
        reader = csv.reader(file)

        # Display data rows
        for i, expense in enumerate(reader, start=1):
            for j, value in enumerate(expense):
                data_label = ctk.CTkLabel(table_frame, text=value, font=("Century Gothic", 12), text_color="white")
                data_label.grid(row=i, column=j, padx=13, pady=1)

# Function to calculate and update the total amount
def update_total():
    total_sum = 0  # Initialize total_sum variable

    with open('expenses.csv', 'r') as file:
        reader = csv.reader(file)

        # Perform summation operation on the second column
        for row in reader:
            try:
                amount = row[1].strip().replace(',', '.')  # Replace comma with dot for decimal handling
                value = float(amount)  # Convert amount to float
                total_sum += value  # Add the value to the total sum
            except (IndexError, ValueError) as e:
                print(f"Error: {e} - Skipping row: {row}")

    # Update the total label
    total_label.configure(text=f"Total Expenses: € {total_sum:.2f}")

# Welcome message and total amount spent
welcome_frame = ctk.CTkFrame(app, width=700, height=50, fg_color="#4A4D50", corner_radius=15)
welcome_frame.place(x=20, y=330)

total_label = ctk.CTkLabel(welcome_frame, text="Total Expenses: € 0.00", font=("Century Gothic", 16, 'bold'), text_color="white")
total_label.pack(padx=20, pady=5)

# Initial display of the table and total
update_table()
update_total()

app.mainloop()
