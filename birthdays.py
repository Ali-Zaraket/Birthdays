import sqlite3 as sq
import tkinter as tk
import tkinter.messagebox as msg
import time as t
import re
import os
import smtplib

# CONSTANTS 
title = "Friends"
geometry = "450x420"
font = ("Times", 15)


""" DATABASE BUILT WITH 3 COLUMNS (NAME , DOB, EMAIL)"""


class Friend:
    """ FRIEND CLASS CONTROLLING ALL FRIENDS' FUNCTIONS """

    birthday = False

    # FRIEND CLASS CHARACTERISTICS 
    def __init__(self, name='', dob='', email=''):
        self.name = name
        self.dob = dob
        self.email = email
        self.conn = sq.connect("birthday.db")
        self.cursor = self.conn.cursor()

    # CHECK FOR BIRTHDAYS 
    def checkBirthday(self):
        today = str(t.localtime().tm_mon) + "-" + str(t.localtime().tm_mday)
        pattern = r"....." + today
        self.birthday = bool(re.match(pattern, self.dob))

    # ADDING A FRIEND TO YOUR DATABASE 
    def addFriend(self):
        lst = [self.name, self.dob, self.email]
        self.cursor.executemany("INSERT INTO friends VALUES (?,?,?)", (lst,))
        self.conn.commit()

    # DELETING A FRIEND FROM THE DATABASE
    def deleteFriend(self):
        self.cursor.execute("DELETE FROM friends WHERE name = (?)", (self.name, ))
        self.conn.commit()

    def getAll(self):
        self.cursor.execute("SELECT name FROM friends")
        allFriends = self.cursor.fetchall()
        self.conn.commit()
        return allFriends

    # FRIENDS' INFO
    def getAll_info(self):
        self.cursor.execute("SELECT * FROM friends")
        allFriends = self.cursor.fetchall()
        self.conn.commit()
        return allFriends

    # EMAIL SENDER , PUT YOUR OWN EMAIL ADDRESS AND PASSWORD IN THE VARIABLES WHEN USING 
    @staticmethod
    def sendEmail(friendName, friendEmail):
        # ENVIRONMENT VARIABLES 
        email = os.environ.get('EMAIL')
        password = os.environ.get('EMAIL_PASSWORDS')
        
        with smtplib.SMTP('smtp.gmail.com', 587) as sm:
            sm.ehlo()
            sm.starttls()
            sm.ehlo()
            sm.login(email, password)
            message = f"Subject: BirthDay!\n\n\n Happy BirthDay {friendName} !! \nWish you all Luck..."
            sm.sendmail(email, friendEmail, message)

    # EDITING EMAILS IF CHANGED 
    def update_email(self):
        lst = [self.email, self.name]
        self.cursor.executemany("UPDATE friends SET email = (?) WHERE name = (?)", (lst, ))
        self.conn.commit()


class Windows:

    """ WINDOWS CLASS , SEVERAL WINDOWS OF THE PROGRAM AND THE GUI STRUCTURE"""

    def __init__(self):
        pass

    @staticmethod
    def adding_friend_window():
        global adding_friend, friend_info
        adding_friend = tk.Tk()
        adding_friend.geometry("680x400")
        adding_friend.title(title)
        adding_friend.resizable(False, False)

        friend_info = FriendInfo(adding_friend)
        friend_info.structure()

        adding_friend.mainloop()

    @staticmethod
    def deleting_friend_window():
        deleting_friend = tk.Tk()
        deleting_friend.title(title)
        deleting_friend.geometry("450x450")
        deleting_friend.resizable(False, False)

        header = tk.Label(deleting_friend, text="Select One to Remove.", font=font, bg="Red")
        listbox = tk.Listbox(deleting_friend, font=font, bd=5)

        def delete():
            if listbox.get(tk.END) == "":
                msg.showwarning(title, "No Friends to Delete..")
                deleting_friend.destroy()

            else:
                message = msg.askokcancel(title, "Delete Friend? ")
                if message == 1:
                    friend = Friend(listbox.get(tk.ANCHOR))
                    friend.deleteFriend()

                    listbox.delete(tk.ANCHOR)   

        backButton = tk.Button(deleting_friend, text="Back", font=font, bd=4, bg="LightBlue",
                               command=deleting_friend.destroy)
        delButton = tk.Button(deleting_friend, text="Delete", bd=4, bg="LightBlue", font=font, command=delete)
        for name in Friend().getAll():
            listbox.insert(tk.END, name[0])

        header.grid(row=0, column=0, columnspan=2, padx=130, pady=25)
        listbox.grid(row=1, column=0, columnspan=2, pady=15)
        backButton.grid(row=2, column=0, pady=20)
        delButton.grid(row=2, column=1, pady=20)

        deleting_friend.mainloop()

    def birthDays_window(self):
        b_window = tk.Tk()
        b_window.title(title)
        b_window.geometry(geometry)
        b_window.resizable(False, False)

        header = tk.Label(b_window, text="Search For BirthDays", font=font, bg="Red", padx=20)
        entry = tk.Entry(b_window, width=35, font=font, bd=5)

        # SEARCHING FOR AVAILABLE BIRTHDAYS IN THE DAY 
        def search():
            t.sleep(1)
            for i in range(len(Friend().getAll())):
                friend = list(Friend().getAll_info()[i])
                friend_information = Friend(friend[0], str(friend[1]), friend[2])
                friend_information.checkBirthday()

                if friend_information.birthday:
                    entry.delete(0, tk.END)
                    entry.insert(0, f"Today is {friend[0]}'s BirthDay!!")
                    s_button['text'] = 'Send Mail'
                    s_button.configure(command=lambda: Friend.sendEmail(friend[0], friend[2]))

                    break
            else:
                entry.delete(0, tk.END)
                entry.insert(0, "No BirthDays Today !")
                s_button['state'] = 'disabled'

        frame = tk.Frame(b_window)
        backButton = tk.Button(frame, text="Back", font=font, bd=4, width=8, command=b_window.destroy)
        s_button = tk.Button(frame, text="Start Search", bd=4, font=font, width=8, command=search)
        entry.insert(0, "Click To Start Searching...")

        header.pack(pady=20)
        entry.pack(pady=20)
        frame.pack(pady=25)
        backButton.grid(row=0, column=0, padx=10, pady=20)
        s_button.grid(row=0, column=1, padx=10, pady=20)

        b_window.mainloop()

    # MAIN WINDOW OF THE PROGRAM
    def main(self):
        main = tk.Tk()
        main.geometry(geometry)
        main.title(title)
        main.resizable(False, False)

        button1 = tk.Button(main, text="ADD Friend", font=font, bd=4, width=12, command=self.adding_friend_window)
        button2 = tk.Button(main, text="DEL Friend", font=font, bd=4, width=12, command=self.deleting_friend_window)
        button3 = tk.Button(main, text="BirthDays", font=font, bd=4, width=12, command=self.birthDays_window)
        button4 = tk.Button(main, text="Update Email", font=font, bd=4, width=12, command=Windows.update_email_window)
        button5 = tk.Button(main, text="QUIT", font=font, bd=4, width=12, command=main.destroy)

        button1.pack(pady=20)
        button2.pack(pady=20)
        button3.pack(pady=20)
        button4.pack(pady=20)
        button5.pack(pady=20)

        main.mainloop()

    @staticmethod
    def update_email_window():
        global up
        up = tk.Tk()
        up.title(title)
        up.geometry("500x450")
        up.resizable(False, False)

        window = UpdateWindow(up)
        window.structure()


class FriendInfo:
    """ 
    FRIEND INFO CLASS , WHEN ADDING A NEW FRIEND , 
    ALL INFO IS CONTROLLED HERE BEFORE INSERTING TO DATABASE
    """

    YEARS = [i for i in range(1990, int(t.localtime().tm_year)+1)]
    MONTHS = [i for i in range(1, 13)]
    DAYS = [i for i in range(1, 32)]

    def __init__(self, master):
        self.master = master
        self.nameEntry = tk.Entry(self.master, font=font, width=30, bd=4)
        self.emailEntry = tk.Entry(self.master, font=font, width=30, bd=4)

        self.var1 = tk.StringVar(self.master)
        self.var2 = tk.StringVar(self.master)
        self.var3 = tk.StringVar(self.master)
        self.menu1 = tk.OptionMenu(self.master, self.var1, *self.YEARS)
        self.menu2 = tk.OptionMenu(self.master, self.var2, *self.MONTHS)
        self.menu3 = tk.OptionMenu(self.master, self.var3, *self.DAYS)

    def structure(self):
        header = tk.Label(self.master, text="Fill the info:", font=font, bg="Red")
        nameLabel = tk.Label(self.master, text="Name:", font=font)
        label = tk.Label(self.master, text=" DOB :", font=font)
        label1 = tk.Label(self.master, text="Year", font=font)
        label2 = tk.Label(self.master, text="Month", font=font)
        label3 = tk.Label(self.master, text="Day", font=font)

        emailLabel = tk.Label(self.master, text="Email:", font=font)
        self.var1.set(2000)
        self.var2.set(1)
        self.var3.set(1)

        def add():
            if self.var1.get() == "" or self.var2.get() == "" or self.var3.get() == "" or self.nameEntry.get() == "" or self.emailEntry.get() == "":
                msg.showwarning(title, "Please fill All blanks..")

            else:
                dob = f'{self.var1.get()}-{self.var2.get()}-{self.var3.get()}'
                friend = Friend(self.nameEntry.get(), dob, self.emailEntry.get())
                friend.addFriend()
                msg.showinfo(title, "Friend Successfully Added !")       
                self.master.destroy()

        backButton = tk.Button(self.master, text="Back", font=font, bd=4, bg="LightBlue", width=8,
                               command=adding_friend.destroy)

        addButton = tk.Button(self.master, text="Add", font=font, bd=4, bg="LightBlue", width=8,
                              command=add)

        header.grid(row=0, column=0, columnspan=2, pady=20, padx=30)
        nameLabel.grid(row=1, column=0, columnspan=2, pady=15)
        self.nameEntry.grid(row=1, column=2, columnspan=4)
        emailLabel.grid(row=2, column=0, columnspan=2, pady=15)
        self.emailEntry.grid(row=2, column=2, columnspan=4)
        label.grid(row=3, column=0, columnspan=2, pady=15)
        label1.grid(row=4, column=0)
        self.menu1.grid(row=4, column=1)
        label2.grid(row=4, column=2, padx=40)
        self.menu2.grid(row=4, column=3)
        label3.grid(row=4, column=4, padx=50)
        self.menu3.grid(row=4, column=5)
        backButton.grid(row=5, column=2, columnspan=2, pady=40)
        addButton.grid(row=5, column=3, columnspan=2)


class UpdateWindow:

    """ UPDATING THE EMAILS """

    def __init__(self, master):
        self.master = master
        self.entry = tk.Entry(self.master, bd=4, font=font, width=25)

    def structure(self):
        header = tk.Label(self.master, text="Update Email", font=font)
        listbox = tk.Listbox(self.master, font=font, width=20)
        label = tk.Label(self.master, text="Enter New Email: ", font=font)
        for name in Friend().getAll():
            listbox.insert(tk.END, name[0])

        def update():
            friend = Friend(listbox.get(tk.ANCHOR), email=self.entry.get())
            friend.update_email()
            upButton['text'] = 'Updated'
            upButton['state'] = 'disabled'

        backButton = tk.Button(self.master, text="Back", font=font, bd=4, width=6, command=up.destroy)
        upButton = tk.Button(self.master, text="Update", font=font, bd=4, width=6, command=update)

        header.grid(row=0, column=0, columnspan=2, padx=40, pady=10)
        listbox.grid(row=1, column=0, pady=30, rowspan=2, padx=15)
        label.grid(row=1, column=1)
        self.entry.grid(row=2, column=1)
        backButton.grid(row=3, column=0)
        upButton.grid(row=3, column=1, pady=10)


# RUNNING THE MAIN WINDOW OF CLASS Windows ..
Windows().main()
