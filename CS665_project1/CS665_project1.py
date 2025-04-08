from asyncio.windows_events import NULL
import tkinter
import mysql.connector




class AircraftApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alex's Aircraft Database")

        self.create_login_frame()

    def create_login_frame(self):
        self.login_frame = tkinter.Frame(self.root)
        self.login_frame.pack(pady=20)

        tkinter.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky="e")
        self.username_entry = tkinter.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        tkinter.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky="e")
        self.password_entry = tkinter.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        login_button = tkinter.Button(self.login_frame, text="Connect", command=NULL)
        login_button.grid(row=3, column=1)





if __name__ == "__main__":
    root = tkinter.Tk()
    app = AircraftApp(root)
    root.mainloop()

conn = mysql.connector.connect(
host="localhost",     # or your DB host
user=input("Username: "),
password=input("Password: "),
database="alexsaircraft" 
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM aircraft")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()