from asyncio.windows_events import NULL
import tkinter
from tkinter import ttk
import mysql.connector
from tkinter import ttk, messagebox




class AircraftApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alex's Aircraft Database")
        self.active_frame = None
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
        self.create_nav_bar()
        self.home_frame()
        
    
    def create_nav_bar(self):
        self.nav_frame = tkinter.Frame(self.root)
        self.nav_frame.pack(pady=10)

        self.action_var = tkinter.StringVar()
        action_menu = ttk.Combobox(self.nav_frame, textvariable=self.action_var, state="readonly")
        action_menu["values"] = ("Home", "Select", "Insert", "Update", "Delete")
        action_menu.current(0)
        action_menu.pack(side="left", padx=10)

        go_button = tkinter.Button(self.nav_frame, text="Go", command=self.handle_action_change)
        go_button.pack(side="left")


    def home_frame(self):
        self.login_frame.destroy()

        if self.active_frame:
            self.active_frame.destroy()

        self.active_frame = tkinter.Frame(self.root)
        self.active_frame.pack(pady=20)


        tkinter.Label(self.active_frame, text="HOME", font=("Helvetica", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=20, sticky="ew")
        

        sql_buttons_frame = tkinter.LabelFrame(self.active_frame, text="Predefined SQL Queries", padx=10, pady=10)
        sql_buttons_frame.grid(row=2, column=1)

        join_customers_button = tkinter.Button(sql_buttons_frame, text="Customers & Aircraft", command=self.query_customers_aircraft)
        join_customers_button.grid(row=1, column=0, pady=5)

        join_employees_parts = tkinter.Button(sql_buttons_frame, text="Employees & Parts", command=self.query_employees_max_parts)
        join_employees_parts.grid(row=1, column=1, pady=5)

        
   

    def handle_action_change(self):
        selected_action = self.action_var.get()
        if selected_action == "Select":
            self.select_frame()
            print("reading database")
        elif selected_action == "Insert":
            self.insert_frame()
            print("adding to database")
        elif selected_action == "Update":
            self.update_frame()
            print("updating database")
        elif selected_action == "Delete":
            self.delete_frame()
            print("deleting from database")
        elif selected_action == "Home":
            self.home_frame()
            print("going home")
    
    def select_frame(self):
        if self.active_frame:
            self.active_frame.destroy()


        self.active_frame = tkinter.Frame(self.root)
        self.active_frame.pack(pady=20)

     
        tkinter.Label(self.active_frame, text="Select a table to view:").pack()

        self.table_var = tkinter.StringVar()
        self.table_dropdown = ttk.Combobox(self.active_frame, textvariable=self.table_var, state="readonly")
        self.table_dropdown["values"] = ("aircraft", "part", "employee", "customer")
        self.table_dropdown.pack(pady=5)
        selected_table = self.table_var.get()

        go_button = tkinter.Button(self.active_frame, text="Go", command=self.display_selected)
        go_button.pack(pady=5)

        self.tree = ttk.Treeview(self.active_frame)
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
        if self.active_frame:
            self.active_frame.destroy()

        if hasattr(self, "entry_frame") and self.entry_frame.winfo_exists():
            self.entry_frame.destroy()

        self.active_frame = tkinter.Frame(self.root)
        self.active_frame.pack(pady=20)

        tkinter.Label(self.active_frame, text="Select a table to update:").pack()

        self.update_table_var = tkinter.StringVar()
        self.update_table_dropdown = ttk.Combobox(self.active_frame, textvariable=self.update_table_var, state="readonly")
        self.update_table_dropdown["values"] = ("aircraft", "part", "employee", "customer") 
        self.update_table_dropdown.pack(pady=5)

        go_button = tkinter.Button(self.active_frame, text="Go", command=self.load_table_for_update)
        go_button.pack(pady=5)

        self.update_tree = ttk.Treeview(self.active_frame)
        self.update_tree.pack(fill="both", expand=True)


    def load_table_for_update(self):
        for widget in self.update_tree.get_children():
            self.update_tree.delete(widget)

        if hasattr(self, "entry_frame") and self.entry_frame.winfo_exists():
            self.entry_frame.destroy()
            self.update_btn.destroy()

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

        self.entry_frame = tkinter.Frame(self.active_frame)
        self.entry_frame.pack(pady=10)

        for i, col in enumerate(columns):
            tkinter.Label(self.entry_frame, text=col).grid(row=0, column=i)
            entry = tkinter.Entry(self.entry_frame)
            entry.grid(row=1, column=i)
            self.edit_fields.append(entry)

        self.update_tree.bind("<<TreeviewSelect>>", self.on_update_row_select)

        self.update_btn = tkinter.Button(self.active_frame, text="Update Selected Row", command=lambda: self.update_row(selected_table, columns))
        self.update_btn.pack(pady=5)
        

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

        self.cursor.execute(query, updated_values[1:] + [self.selected_row_id])
        self.conn.commit()
        messagebox.showinfo("Success", "Record updated.")
        self.load_table_for_update()
        



    def delete_frame(self):
        if self.active_frame:
            self.active_frame.destroy()

        self.active_frame = tkinter.Frame(self.root)
        self.active_frame.pack(pady=20)

        tkinter.Label(self.active_frame, text="Select a table to delete from:").pack()

        self.delete_table_var = tkinter.StringVar()
        self.delete_table_dropdown = ttk.Combobox(self.active_frame, textvariable=self.delete_table_var, state="readonly")
        self.delete_table_dropdown["values"] = ("aircraft", "part", "employee", "customer")
        self.delete_table_dropdown.pack(pady=5)

        go_button = tkinter.Button(self.active_frame, text="Go", command=self.load_table_for_delete)
        go_button.pack(pady=5)

        self.delete_tree = ttk.Treeview(self.active_frame)
        self.delete_tree.pack(fill="both", expand=True)

        delete_button = tkinter.Button(self.active_frame, text="Delete Selected Row", command=self.delete_selected_row)
        delete_button.pack(pady=5)



    def load_table_for_delete(self):
        for widget in self.delete_tree.get_children():
            self.delete_tree.delete(widget)

        selected_table = self.delete_table_var.get()
        self.cursor.execute(f"SELECT * FROM {selected_table}")
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        self.delete_tree["columns"] = columns
        self.delete_tree["show"] = "headings"

        for col in columns:
            self.delete_tree.heading(col, text=col)
            self.delete_tree.column(col, width=100)

        for row in rows:
            self.delete_tree.insert("", "end", values=row)

        self.delete_columns = columns
        self.delete_table_name = selected_table


    def delete_selected_row(self):
        selected_item = self.delete_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No row selected.")
            return

        values = self.delete_tree.item(selected_item[0], "values")
        primary_key_column = self.delete_columns[0]
        primary_key_value = values[0]

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete row with {primary_key_column} = {primary_key_value}?")
        if not confirm:
            return

        query = f"DELETE FROM {self.delete_table_name} WHERE {primary_key_column} = %s"
        self.cursor.execute(query, (primary_key_value,))
        self.conn.commit()
        messagebox.showinfo("Success", "Row deleted successfully.")
        self.load_table_for_delete()
        


    def insert_frame(self):
        if self.active_frame:
            self.active_frame.destroy()

        self.active_frame = tkinter.Frame(self.root)
        self.active_frame.pack(pady=20)

        tkinter.Label(self.active_frame, text="Select a table to insert into:").pack()

        self.insert_table_var = tkinter.StringVar()
        self.insert_table_dropdown = ttk.Combobox(self.active_frame, textvariable=self.insert_table_var, state="readonly")
        self.insert_table_dropdown["values"] = ("aircraft", "part", "employee", "customer") 
        self.insert_table_dropdown.pack(pady=5)

        go_button = tkinter.Button(self.active_frame, text="Go", command=self.load_fields_for_insert)
        go_button.pack(pady=5)


    def load_fields_for_insert(self):
        selected_table = self.insert_table_var.get()

        self.cursor.execute(f"SELECT * FROM {selected_table}")
        columns = [desc[0] for desc in self.cursor.description]
        _ = self.cursor.fetchall()
        
        self.insert_columns = columns
        self.insert_table_name = selected_table

        
        if hasattr(self, 'input_frame'):
            self.input_frame.destroy()

        self.input_frame = tkinter.Frame(self.active_frame)
        self.input_frame.pack(pady=10)

        self.input_entries = []
        for i, col in enumerate(columns):
            tkinter.Label(self.input_frame, text=col).grid(row=0, column=i)
            entry = tkinter.Entry(self.input_frame)
            entry.grid(row=1, column=i, padx=5)
            self.input_entries.append(entry)

        insert_button = tkinter.Button(self.active_frame, text="Insert Row", command=self.insert_row)
        insert_button.pack(pady=5)

    def insert_row(self):
        values = [entry.get() for entry in self.input_entries]

        placeholders = ", ".join(["%s"] * len(values))
        columns_str = ", ".join(self.insert_columns)
        query = f"INSERT INTO {self.insert_table_name} ({columns_str}) VALUES ({placeholders})"

        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "Row added successfully.")
            for entry in self.input_entries:
                entry.delete(0, tkinter.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))




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

