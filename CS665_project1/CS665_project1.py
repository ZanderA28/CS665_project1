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
        self.home_frame.pack(pady = 20)

        tkinter.Label(self.home_frame, text="HOME").grid(row=0, column=1, sticky="e")
        select_button = tkinter.Button(self.home_frame, text="Display", command=self.show_aircraft)
        select_button.grid(row=1, column=1)

    def show_aircraft(self):
        print("show aircraft clicked")
        
if __name__ == "__main__":
    root = tkinter.Tk()
    app = AircraftApp(root)
    root.mainloop()

