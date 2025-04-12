from asyncio.windows_events import NULL
import tkinter
from tkinter import ttk
import mysql.connector
from tkinter import ttk, messagebox




class AircraftApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alex's Aircraft Database")

        self.create_login_frame()

    def create_login_frame(self):
        self.login_frame = tkinter.Frame(self.root)
        self.login_frame.pack(pady=20)

        tkinter.Label(self.login_frame, text="ALEX'S AIRCRAFT DATA ACCESS").grid(row=0, column=1, sticky="e")

        tkinter.Label(self.login_frame, text="Username:").grid(row=1, column=0, sticky="e")
        self.username_entry = tkinter.Entry(self.login_frame)
        self.username_entry.grid(row=1, column=1)

        tkinter.Label(self.login_frame, text="Password:").grid(row=2, column=0, sticky="e")
        self.password_entry = tkinter.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=2, column=1)

        login_button = tkinter.Button(self.login_frame, text="Connect", command=self.connect_to_db)
        login_button.grid(row=4, column=1)


    def connect_to_db(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.conn = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password,
            database="alexsaircraft"
        )
        self.cursor = self.conn.cursor()
        print("connected to database")
        self.home_frame()
        
        

    def home_frame(self):
        self.login_frame.destroy()
        self.home_frame = tkinter.Frame(self.root)
        dropdown_frame = tkinter.Frame(self.root)
        self.home_frame.pack(pady = 20)
        dropdown_frame.pack(pady=10)

        tkinter.Label(self.home_frame, text="HOME").grid(row=0, column=1, sticky="e")
        tkinter.Label(dropdown_frame, text="Choose Action:").pack(side="left")
        select_button = tkinter.Button(self.home_frame, text="Display", command=self.show_aircraft)
        select_button.grid(row=1, column=1)

        sql_buttons_frame = tkinter.LabelFrame(self.root, text="Predefined SQL Queries", padx=10, pady=10)
        sql_buttons_frame.pack(pady=10)

        join_customers_button = tkinter.Button(sql_buttons_frame, text="Customers & Aircraft", command=self.query_customers_aircraft)
        join_customers_button.grid(row=1, column=0, pady=5)

        join_employees_parts = tkinter.Button(sql_buttons_frame, text="Employees & Parts", command=self.query_employees_max_parts)
        join_employees_parts.grid(row=1, column=1, pady=5)

        self.action_var = tkinter.StringVar()
        action_menu = ttk.Combobox(dropdown_frame, textvariable=self.action_var, state="readonly")
        action_menu["values"] = ("Select", "Add", "Update", "Delete")
        action_menu.pack(side="left", padx=10)
        action_menu.bind("<<ComboboxSelected>>", NULL)
    
    def show_aircraft(self):
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill="both", expand=True)

        self.cursor.execute("SELECT * FROM aircraft")
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        self.tree["columns"] = columns
        self.tree["show"] = "headings"

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for row in rows:
            self.tree.insert("", "end", values=row)

    def query_customers_aircraft(self):
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill="both", expand=True)

        query = """
        SELECT c.Customer_ID, c.Name AS Customer_Name, a.Model_Name, a.Type
        FROM Customer c
        JOIN Aircraft a ON c.Purchased_Model = a.Model_ID
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        self.tree["columns"] = columns
        self.tree["show"] = "headings"

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for row in rows:
            self.tree.insert("", "end", values=row)

    def query_employees_max_parts(self):
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill="both", expand=True)
        query = """
        SELECT e.Employee_ID, e.Name, e.Role, p.Part_Name, p.Quantity
        FROM Employee e
        JOIN Part p ON e.Part_Station_ID = p.Part_ID
        ORDER BY p.Quantity desc
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        self.tree["columns"] = columns
        self.tree["show"] = "headings"

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for row in rows:
            self.tree.insert("", "end", values=row)

        
if __name__ == "__main__":
    root = tkinter.Tk()
    app = AircraftApp(root)
    root.mainloop()

