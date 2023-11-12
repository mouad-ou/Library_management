from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import mysql.connector as mysql
import hashlib
import tkinter as tk
import tkinter.ttk as ttk

class Database:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "gb"
        self.port = 3306
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
            self.cursor = self.conn.cursor()
            print("connected")
        except mysql.Error as e:
            print(e)
    def getAll(self):
        req=f"select * from Books"
        self.cursor.execute(req)
        books=self.cursor.fetchall()
        return books
    def addbook(self,Book):
        req=f"insert into books(Title,Author,Yearpb) values(%s,%s,%s)"
        values=(Book.title,Book.author,Book.year)
        self.cursor.execute(req,values)
        self.conn.commit()
    def addauthor(self,Author):
        if self.cursor:
            self.cursor.close
        req=f"insert into author(name) values(%s)"
        self.cursor.execute(req,(Author.name,))
        self.conn.commit()
    def updatebook(self,Book,id):
        
        req=f"update books set Title=%s,Author=%s,Yearpb=%s where id=%s"
        values=(Book.title,Book.author,Book.year,id)
        self.cursor.execute(req,values)
        self.conn.commit()
    def delete(self,id):
        req=f"delete from books where id=%s"
        values=(id,)
        self.cursor.execute(req,values)
        self.conn.commit()
database = Database()
database.connect()

class LoginWidget(QDialog):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label_username = QLabel("Username:")
        self.line_edit_username = QLineEdit()
        layout.addWidget(label_username)
        layout.addWidget(self.line_edit_username)

        label_password = QLabel("Password:")
        self.line_edit_password = QLineEdit()
        self.line_edit_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_password)
        layout.addWidget(self.line_edit_password)

        self.btn_login = QPushButton('Login')
        self.btn_login.clicked.connect(self.login)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)
        self.setWindowTitle('Login')

    def login(self):
        username = self.line_edit_username.text()
        password = self.line_edit_password.text()

        sql = "SELECT * FROM user WHERE username=%s"
        val = (username,)
        database.cursor.execute(sql, val)
        result = database.cursor.fetchone()

        if result:
              # Print the result tuple for debugging

            stored_salt = "eee27ffc9bd140c954e4ffedc10a86a5"  # Previous salt value
            stored_hashed_password = result[2] if len(result) > 3 else None

            if stored_hashed_password is not None:
                hashed_password = hashlib.sha256((password + stored_salt).encode()).hexdigest()
                print('hashed_pass')
                print(hashed_password)
                print('stored_hashed_password')
                print(stored_hashed_password)
                if hashed_password == stored_hashed_password:
                    QMessageBox.information(self, 'Success', 'Login successful!')
                    
                    self.close()
                    class Book:
                        def __init__(self, title, author, year):
                            self.title = title
                            self.author = author
                            self.year = year
                    class Author:
                        def __init__(self, name):
                            self.name = name
                            

                    conn= Database()
                    conn.connect()



                    # Insert authors that don't exist in the author table
                    def updateAllAuthors():
                            conn.cursor.execute("SELECT DISTINCT Author FROM books")
                            authors = conn.cursor.fetchall()
                            for author in authors:
                                conn.cursor.execute("SELECT * FROM author WHERE name = %s", (author[0],))
                                result = conn.cursor.fetchone()
                                if result is None:
                                    at1=Author(author[0])
                                    conn.addauthor(at1)
                    def getauth():
                        global authorss
                        conn.cursor.execute("SELECT name FROM author")
                        authorss = [author[0] for author in conn.cursor.fetchall()]
                        return authorss



                    #-------------------------- controller ----------------
                    def addBK():
                        open_form()
                    

                    def selectItem(event):
                        global ID
                        seletedItem=my_tree.selection()[0]
                        ID=my_tree.item(seletedItem)["text"]
                    def deleteBook():
                        conn.delete(ID)
                        show()
                    def search_books():
                            query = S_input.get()
                            sql = "SELECT * FROM books WHERE Title LIKE %s OR Yearpb LIKE %s"
                            values = (f"%{query}%", f"%{query}%")
                            conn.cursor.execute(sql, values)
                            books = conn.cursor.fetchall()
                            return books
                    def search_authors():
                            query = authorchoosen.get()
                            sql = "SELECT * FROM books WHERE Author LIKE %s"
                            values = (f"%{query}%",)
                            conn.cursor.execute(sql, values)
                            books = conn.cursor.fetchall()
                            return books
                    def show_search():
                        my_tree.delete(*my_tree.get_children())

                            # Loop through the rows and insert each book into the treeview
                        for row in search_books():
                                my_tree.insert('', 'end', text=row[0], values=(row[1], row[2], row[3]))
                    def show_search_auth():
                        my_tree.delete(*my_tree.get_children())

                            # Loop through the rows and insert each book into the treeview
                        for row in search_authors():
                                my_tree.insert('', 'end', text=row[0], values=(row[1], row[2], row[3]))

                    def show():
                        
                            updateAllAuthors()

                            my_tree.delete(*my_tree.get_children())

                            # Loop through the rows and insert each book into the treeview
                            for row in conn.getAll():
                                my_tree.insert('', 'end', text=row[0], values=(row[1], row[2], row[3]))
                            updateauth()
                    def CheckToAdd(Author):
                            conn.cursor.execute("SELECT id FROM author WHERE name = %s", (Author.name,))
                            author_id = conn.cursor.fetchone()
                            if author_id:
                                author_id = author_id[0]
                            else:
                        
                                conn.addauthor(Author)
                                author_id = conn.cursor.lastrowid
                        

                    def UpdateBook():
                        open_form2()
                    #----------------------------------------------------------------------------------------------------------
                    def open_form2():
                        def getvalues2():
                            ktab = Book(title_entry.get(),author_entry.get(),year_entry.get())
                            global ID
                            if ID != None:
                                conn.updatebook(ktab,ID)
                            show()       
                            at = Author(ktab.author)
                            CheckToAdd(at)
                            show()
                            form_window.destroy()
                        form_window = tk.Toplevel()
                        title_label = tk.Label(form_window, text="Title")
                        title_entry = tk.Entry(form_window)
                        author_label = tk.Label(form_window, text="Author")
                        author_entry = tk.Entry(form_window)
                        year_label = tk.Label(form_window, text="Year")
                        year_entry = tk.Entry(form_window)
                        add_button = tk.Button(form_window, text="Done", command=getvalues2)
                        back_button = tk.Button(form_window, text="Cancel", command=form_window.destroy)
                        title_label.pack(padx=5, pady=5)
                        title_entry.pack(padx=5, pady=5)
                        author_label.pack(padx=5, pady=5)
                        author_entry.pack(padx=5, pady=5)
                        year_label.pack(padx=5, pady=5)
                        year_entry.pack(padx=5, pady=5)
                        add_button.pack(padx=5, pady=5)
                        back_button.pack(padx=5, pady=5)
                        getauth()
                        updateAllAuthors()
                    #----------------------------------------------------------------------------------------------------------------------------------
                    def updateauth():
                         authorchoosen.config(values=getauth())
                    def open_form():
                        def getvalues():
                            ktab = Book(title_entry.get(),author_entry.get(),year_entry.get())
                            conn.addbook(ktab)
                            at = Author(ktab.author)
                            CheckToAdd(at)
                            show()
                            getauth()
                            form_window.destroy()
                        form_window = tk.Toplevel()
                        title_label = tk.Label(form_window, text="Title")
                        title_entry = tk.Entry(form_window)

                        author_label = tk.Label(form_window, text="Author")
                        author_entry = tk.Entry(form_window)

                        year_label = tk.Label(form_window, text="Year")
                        year_entry = tk.Entry(form_window)

                    
                        add_button = tk.Button(form_window, text="Done", command=getvalues)
                        back_button = tk.Button(form_window, text="Cancel", command=form_window.destroy)

                        title_label.pack(padx=5, pady=5)
                        title_entry.pack(padx=5, pady=5)
                        author_label.pack(padx=5, pady=5)
                        author_entry.pack(padx=5, pady=5)
                        year_label.pack(padx=5, pady=5)
                        year_entry.pack(padx=5, pady=5)
                        add_button.pack(padx=5, pady=5)
                        back_button.pack(padx=5, pady=5)
                    #-------------------------------------------------------------------------------------------------
                    frame=tk.Tk()
                    frame.geometry("1600x500")
                    frame.title("task manager")

                    my_tree=ttk.Treeview(frame,columns=("Titre","Auteur","Date de Pub"))
                    my_tree.heading("#0",text="ID")
                    my_tree.heading("Titre",text="Title")
                    my_tree.heading("Auteur",text="Author")
                    my_tree.heading("Date de Pub",text="Publication Date")

                    my_tree.column("#0",width=50)
                    my_tree.column("Titre",width=300)
                    my_tree.column("Auteur",width=300)
                    my_tree.column("Date de Pub",width=300)
                    my_tree.pack(side=tk.LEFT,fill=tk.BOTH)

                    desc_label=tk.Label(frame,text=" Commandes :")
                    desc_label.pack(side=tk.TOP,padx=10,pady=10)

                    add_button=tk.Button(frame,text="Add Book",command=addBK,width=18,height=2)
                    add_button.pack(side=tk.TOP,padx=1,pady=0)


                    update_button=tk.Button(frame,text="Update Book",command=UpdateBook,width=18,height=2)
                    update_button.pack(side=tk.TOP, padx=5, pady=30)
                    delete_button=tk.Button(frame,text="Delete Book",command=deleteBook,width=18,height=2)
                    delete_button.pack(side=tk.TOP, padx=5, pady=1)
                    desc_label=tk.Label(frame,text=" Search By author :")
                    desc_label.pack(side=tk.TOP,padx=10,pady=10)
                    n = tk.StringVar()
                    authorchoosen = ttk.Combobox(frame,values=[], width = 27, textvariable = n)
                    conn.cursor.execute("SELECT name FROM author")
                    authorsss = [author[0] for author in conn.cursor.fetchall()]
                    authorchoosen.config(values=getauth())
                    authorchoosen.pack()
                    Search1_button=tk.Button(frame,text="Search",command=show_search_auth,width=18,height=1)
                    Search1_button.pack( padx=5, pady=5)
                    Reset_button=tk.Button(frame,text="Reset",command=show,width=18,height=1)
                    Reset_button.pack(side=tk.BOTTOM, padx=5, pady=5)
                    Search_button=tk.Button(frame,text="Search",command=show_search,width=18,height=1)
                    Search_button.pack(side=tk.BOTTOM, padx=5, pady=5)
                    S_input=tk.Entry(frame)
                    S_input.pack(side=tk.BOTTOM)

                    my_tree.bind('<ButtonRelease-1>',selectItem)
                    show()



                    frame.mainloop()
                    
                else:
                    QMessageBox.warning(self, 'Error', 'Incorrect username or password 1.')
            else:
                QMessageBox.warning(self, 'Error', 'Incorrect username or password 2.')
        else:
            QMessageBox.warning(self, 'Error', 'Incorrect username or password 3.')

        database.conn.close()
