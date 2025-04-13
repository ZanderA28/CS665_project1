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
        select_button = tkinter.Button(self.home_frame, text="Display", command=self.select_frame)
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
        action_menu.bind("<<ComboboxSelected>>", self.handle_action_change)

    def handle_action_change(self, event):
        selected_action = self.action_var.get()
        if selected_action == "Select":
            self.select_frame()
            print("reading database")
        elif selected_action == "Add":
            messagebox.showinfo("Action", NULL)
            print("adding to database")
        elif selected_action == "Update":
            self.update_frame()
            print("updating database")
        elif selected_action == "Delete":
            messagebox.showinfo("Action", NULL)
            print("deleting from database")
    
    def select_frame(self):
        self.home_frame.destroy()
        self.select_frame = tkinter.Frame(self.root)
        self.select_frame.pack(pady = 20)

        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill="both", expand=True)
        tkinter.Label(self.select_frame, text="Select a table to view:").pack()

        self.table_var = tkinter.StringVar()
        self.table_dropdown = ttk.Combobox(self.select_frame, textvariable=self.table_var, state="readonly")
        self.table_dropdown["values"] = ("aircraft", "customer", "employee", "eart")
        self.table_dropdown.pack(pady=5)
        selected_table = self.table_var.get()

        go_button = tkinter.Button(self.select_frame, text="Go", command=self.display_selected)
        go_button.pack(pady=5)

        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill="both", expand=True)

        
    def display_selected(self):
        if hasattr(self, 'tree'):
            self.tree.delete(*self.tree.get_children())
        selected_table = self.table_var.get()
        
        self.cursor.execute(f"SELECT * FROM {selected_table}")
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        self.tree["columns"] = columns
        self.tree["show"] = "headings"

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for row in rows:
            self.tree.insert("", "end", values=row)


    def update_frame(self):
        self.home_frame.destroy()
        self.update_frame = tkinter.Frame(self.root)
        self.update_frame.pack(pady=20)

        tkinter.Label(self.update_frame, text="Select a table to update:").pack()

        self.update_table_var = tkinter.StringVar()
        self.update_table_dropdown = ttk.Combobox(self.update_frame, textvariable=self.update_table_var, state="readonly")
        self.update_table_dropdown["values"] = ("aircraft", "part", "employee", "customer") 
        self.update_table_dropdown.pack(pady=5)

        go_button = tkinter.Button(self.update_frame, text="Go", command=self.load_table_for_update)
        go_button.pack(pady=5)

        self.update_tree = ttk.Treeview(self.root)
        self.update_tree.pack(fill="both", expand=True)


    def load_table_for_update(self):
        for widget in self.update_tree.get_children():
            self.update_tree.delete(widget)

        selected_table = self.update_table_var.get()

        self.cursor.execute(f"SELECT * FROM {selected_table}")
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        self.update_tree["columns"] = columns
        self.update_tree["show"] = "headings"

        for col in columns:
            self.update_tree.heading(col, text=col)
            self.update_tree.column(col, width=100)

        for row in rows:
            self.update_tree.insert("", "end", values=row)

        self.edit_fields = []
        self.selected_row_id = None

        entry_frame = tkinter.Frame(self.root)
        entry_frame.pack(pady=10)

        for i, col in enumerate(columns):
            tkinter.Label(entry_frame, text=col).grid(row=0, column=i)
            entry = tkinter.Entry(entry_frame)
            entry.grid(row=1, column=i)
            self.edit_fields.append(entry)

        self.update_tree.bind("<<TreeviewSelect>>", self.on_update_row_select)

        update_btn = tkinter.Button(self.root, text="Update Selected Row", command=lambda: self.update_row(selected_table, columns))
        update_btn.pack(pady=5)
        

    def on_update_row_select(self, event):
        selected = self.update_tree.selection()
        if selected:
            values = self.update_tree.item(selected[0], "values")
            self.selected_row_id = values[0]
            for i, val in enumerate(values):
                self.edit_fields[i].delete(0, tkinter.END)
                self.edit_fields[i].insert(0, val)

    def update_row(self, table_name, columns):

        updated_values = [entry.get() for entry in self.edit_fields]
        set_clause = ", ".join(f"{col} = %s" for col in columns[1:])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {columns[0]} = %s"

        try:
            self.cursor.execute(query, updated_values[1:] + [self.selected_row_id])
            self.conn.commit()
            messagebox.showinfo("Success", "Record updated.")
            self.load_table_for_update()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))


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

