from tkinter import *
import sqlite3

# NEXT STEPS
# Load database entry - modify / delete
# Display current transaction id


root = Tk()
root.title('Transaction manager')

conn = sqlite3.connect("transactions.db")
c = conn.cursor()
c.execute("""SELECT * FROM transactions""")
a = c.fetchall()
print(a)


# Create Submit Function for Database

def submit():
    # Create a database or connect to one
    conn = sqlite3.connect('transactions.db')

    # Create Cursor
    c = conn.cursor()

    c.execute(
        """INSERT INTO transactions (date, val_num, voucher, qty, price, currency, rate) 
        VALUES (:date, :val_num, :voucher, :qty, :price, :currency, :rate)""",
        {
            'date': date.get(),
            'val_num': val_num.get(),
            'voucher': voucher.get(),
            'qty': qty.get(),
            'price': price.get(),
            'currency': currency.get(),
            'rate': rate.get()
        })
    # Commit Changes
    conn.commit()

    # Close Database

    conn.close()

    # Clear the Text Boxes
    date.delete(0, END)
    voucher.delete(0, END)
    val_num.delete(0, END)
    qty.delete(0, END)
    price.delete(0, END)
    currency.delete(0, END)
    rate.delete(0, END)


# Create Query Function

def query():
    global query
    query = Tk()
    query.title('Abfrage ausführen')
    query.geometry('500x500')
    voucher_num_label = Label(query, text='Beleg-Nr.')
    voucher_num_label.grid(row=0, column=0)
    global voucher_num
    voucher_num = Entry(query, width=20)
    voucher_num.grid(row=0, column=1)
    query_voucher = Button(query, text="Beleg anzeigen", command=show_voucher)
    query_voucher.grid(row=1, column=0)
    modify_voucher = Button(query, text="Beleg bearbeiten", command=modify)
    modify_voucher.grid(row=1, column=1)
    # conn = sqlite3.connect('transactions.db')
    # c = conn.cursor()
    # c.execute("SELECT * FROM transactions")
    # records = c.fetchall()
    # print(records)
    query.mainloop()
    return


def show_voucher():
    conn = sqlite3.connect('transactions.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    voucherqry = voucher_num.get()
    c.execute("SELECT * FROM transactions WHERE voucher = ? ", (voucherqry,))

    result = c.fetchall()
    memb_total = 0
    for member in result:  # Loop through Row Object
        for key in member:  # Loop through Dictionary
            column_descr = Label(query, text=str(member.keys()[memb_total]))
            column_descr.grid(column=memb_total, row=3)
            memb_total += 1

    output_total = 0
    for j in range(0, len(result)):
        for i in result[j]:
            results_label = Label(query, text=str(i))
            results_label.grid(column=output_total, row=4)
            output_total += 1
            print(dict(result[j]), i, "\n")
    return


# Function to modify current voucher

def modify():
    modify = Tk()
    modify.title("Beleg bearbeiten")
    modify.geometry('500x200')

    conn = sqlite3.connect("transactions.db")
    # c = conn.cursor()
    # c.execute("""UPDATE transactions
    #              Set
    #                 date = :date
    #                 val_num = :val_num
    #                 voucher = :voucher
    #                 qty = :qty
    #                 price = :price
    #                 currency = :currency
    #                 rate = :rate)
    #              WHERE
    #                 voucher = :voucher_num
    #                 """,
    #           {
    #               'date': date.get(),
    #               'val_num': val_num.get(),
    #               'voucher': voucher.get(),
    #               'qty': qty.get(),
    #               'price': price.get(),
    #               'currency': currency.get(),
    #               'rate': rate.get(),
    #               'voucher_num': voucher_num.get()
    #           })
    modify.mainloop()
    conn.close()


# Introduction Label

title_label = Label(root, text="Database transactions", font='Arial 14 bold')
title_label.grid(row=0, column=0, padx=20, ipady=10, columnspan=2)

# Create Text Entry Boxes

textbox_row = 4

date = Entry(root, width=15)
date.grid(row=2, column=1, padx=20, sticky=S)

voucher = Entry(root, width=15)
voucher.grid(row=2, column=2, padx=20, sticky=S)

val_num = Entry(root, width=15)
val_num.grid(row=textbox_row, column=0, padx=20, sticky=W)

qty = Entry(root, width=15)
qty.grid(row=textbox_row, column=1, padx=20)

price = Entry(root, width=15)
price.grid(row=textbox_row, column=2, padx=20)

currency = Entry(root, width=15)
currency.grid(row=textbox_row, column=3, padx=20)

rate = Entry(root, width=20)
rate.grid(row=textbox_row, column=4, padx=20)

# Create Text Box Labels

labels_row = 3

transactionid_label = Label(root, text="Transaktions ID:")
transactionid_label.grid(row=1, column=0, padx=20, sticky=NW)

number = StringVar()

conn = sqlite3.connect("transactions.db")
c = conn.cursor()
c.execute("""SELECT Max(transactionid) FROM transactions""")
max_trans_id = c.fetchone()
number.set(max_trans_id)

transactionid = Label(root, textvar=number)
transactionid.grid(row=2, column=0, padx=20, sticky=SW)

date_label = Label(root, text="Transaktionsdatum")
date_label.grid(row=1, column=1, padx=20, sticky=NW)

voucher_label = Label(root, text="Beleg")
voucher_label.grid(row=1, column=2, padx=20, sticky=NW)

val_num_label = Label(root, text="Valorennummer")
val_num_label.grid(row=labels_row, column=0, padx=20, sticky=W)

qty_label = Label(root, text="Anzahl")
qty_label.grid(row=labels_row, column=1, padx=20, sticky=W)

price_label = Label(root, text="Preis")
price_label.grid(row=labels_row, column=2, padx=20, sticky=W)

currency_label = Label(root, text="Währung")
currency_label.grid(row=labels_row, column=3, padx=20, sticky=W)

rate_label = Label(root, text="FW-Kurs")
rate_label.grid(row=labels_row, column=4, padx=20, sticky=W)

# Create Submit Button

submit_btn = Button(root, text="Add Record to Database", command=submit)
submit_btn.grid(row=6, column=0, columnspan=5, pady=10, padx=10, ipadx=100)

# Create a Query Button
query_btn = Button(root, text="Abfrage", command=query)
query_btn.grid(row=0, column=4)
root.mainloop()

# conn = sqlite3.connect('transactions.db')

# Create Cursor
# c = conn.cursor()

# c.execute("""
#        CREATE TABLE transactions (
#        transactionid INTEGER PRIMARY KEY AUTOINCREMENT,
#        date text NOT NULL,
#        voucher integer NOT NULL UNIQUE,
#        val_num integer NOT NULL,
#        qty real NOT NULL,
#        price real NOT NULL,
#        currency text,
#        rate real        )""")
