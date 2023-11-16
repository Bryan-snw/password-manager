from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    password_letters = [choice(letters) for _ in range(nr_letters)]
    password_symbols = [choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password_input.delete(0, END)
    password = ''.join(password_list)
    pyperclip.copy(password)
    password_input.insert(END, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data(data):
    with open("data.json", mode='w') as data_file:
        json.dump(data, data_file, indent=4)


def save_password():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) <= 0 or len(password) <= 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any empty field")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                # Reading Old Data
                data = json.load(data_file)
        except FileNotFoundError:
            save_data(new_data)
        else:
            # Update Data
            data.update(new_data)
            save_data(data)
        finally:
            # Reset
            website_input.delete(0, END)
            password_input.delete(0, END)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def find_password():
    website = website_input.get()
    if len(website) <= 0 :
        messagebox.showinfo(title="Oops", message="Website field is empty")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                # Reading Old Data
                data = json.load(data_file)

        except FileNotFoundError:
            messagebox.showerror(title="Error", message="File Not Found")
        else:
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
            else:
                messagebox.showerror(title="Error", message="No Details for the website exist")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(pady=40, padx=40)

logo = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Label
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entry
website_input = Entry(width=25)
website_input.focus()
website_input.grid(column=1, row=1, sticky='W', padx=(9, 0))

email_input = Entry(width=50)
email_input.insert(END, "bryansie29@gmail.com")
email_input.grid(column=1, row=2, columnspan=2)

password_input = Entry(width=25)
password_input.grid(column=1, row=3, sticky='W', padx=(9, 0))

# Button
generate_password_btn = Button(text="Generate Password", command=generate_password)
generate_password_btn.grid(column=2, row=3, sticky="W", padx=(0, 10))

add_password_btn = Button(text="Add", width=43, command=save_password)
add_password_btn.grid(column=1, row=4, columnspan=2)

search_btn = Button(text="Search", width=15, command=find_password)
search_btn.grid(column=2, row=1, sticky="W", padx=(0, 10))

window.mainloop()
