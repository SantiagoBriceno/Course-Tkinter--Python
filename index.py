from tkinter import ttk
from tkinter import *

import sqlite3

class Product:

    dbname = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title("Products Aplication")

        # Creating a Frame Container

        frame = LabelFrame(self.wind, text = 'Register a new Product')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        #name Input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        #Price Input
        Label(frame, text = 'Price: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        # Button add Product 
        ttk.Button(frame, text = 'Save Product', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W+E)

        # Mensajes de aviso
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan=2, sticky = W + E)

        #Table
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading("#0", text='Name', anchor = CENTER)
        self.tree.heading("#1", text='Price', anchor = CENTER)

        self.get_products()


    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.dbname) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):

        #Cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        #quering data
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
        if self.validation():
            print(self.name.get())
            print(self.price.get())

            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            productName = self.name.get()
            productPrice = self.price.get()
            parameters = (productName, productPrice)
            self.run_query(query, parameters)
            self.message['text'] = 'El producto {} ha sido agregado'.format(productName)

            #Borramos los campos de textos
            self.name.delete(0, END)
            self.price.delete(0, END)

        else:
            self.message['text'] = 'El nombre y el precio son requeridos'
        self.get_products()
        


if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
