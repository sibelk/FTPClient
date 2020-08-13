# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 17:50:53 2020

@author: sibel
"""

import tkinter as tk
from ftplib import FTP
from tkinter import filedialog
from tkinter.simpledialog import askstring


'''

            SERVER        : localhost
            PORT          : 21
            Kullanici adi : user
            Parola        : 12345


            GEREKLİ MODÜLLER
            -----------------
            +tkinter
            +pyftpdlib 1.5.6    (forserver )
            +ftplib             (for client )


'''
# %%


class Root(tk.Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("FTPApp")
        self.minsize(600, 150)
        
        # login form
        self.server_name = tk.Label(
            self, text="HOST:", font=("Helvetica", 12), justify=tk.LEFT)
        self.server_name.grid(column=0, sticky=tk.W, row=0)

        self.serverName = tk.Entry(self, width=15)
        self.serverName.grid(column=1, row=0)

        self._port = tk.Label(self, text="Port:", font=(
            "Helvetica", 12), justify=tk.LEFT)
        self._port.grid(column=2, sticky=tk.W, row=0)

        self._port_ = tk.Entry(self, width=15)
        self._port_.grid(column=3, row=0)

        self.name = tk.Label(self, text="User Name:", font=(
            "Helvetica", 12), justify=tk.LEFT)
        self.name.grid(column=4, sticky=tk.W, row=0)

        self.nam = tk.Entry(self, width=15)
        self.nam.grid(column=5, row=0)

        self.passwd = tk.Label(self, text="Password:", font=(
            "Helvetica", 12), justify=tk.LEFT)
        self.passwd.grid(column=6, sticky=tk.W, row=0)

        self.password = tk.Entry(self, width=15, show="*")
        self.password.grid(column=7, row=0)

        self.btn = tk.Button(self, text="LOGIN", bg="black",
                             fg="white", command=self.ftp_connection)
        self.btn.grid(column=7, row=2, sticky=tk.E)


# %%  FTP COMMANDS

    def ftp_connection(self):
        self.ftp = FTP(self.serverName.get())
        print(self._port_.get())
        if(self._port_.get()=='' ):
            self._port_.delete(0,'end')
            self._port_.insert(0,"21")
 
        try:
           
            self.ftp.connect(self.serverName.get(),int(self._port_.get()))
            a = self.ftp.login(self.nam.get(), self.password.get())
            if(a):
                self.user_interface()
                self.list_dir()

        except Exception as e:
            tk.messagebox.showerror(title="Connection Error", message=e)

    def delete(self):
        try:
            self.ftp.delete(self.selection())
            self.list_dir()
        except Exception as e:
            tk.messagebox.showerror(title="Delete Error", message=e)

    def list_dir(self):

        data = []
        dirlist = self.ftp.nlst()
        self.ftp.dir(data.append)
        self.liste.delete(0, 'end')
        self.liste.insert(0, "/")

        for index, d in enumerate(dirlist):
            self.liste.insert(index+1, str(d))

    def upload(self):
        try:

            filename = filedialog.askopenfilename(
                initialdir="/", title="Select A File", filetype=())
            filename = filename.split("/")[-1]
            if(filename):
                self.ftp.storbinary('STOR '+str(filename), open(filename, 'rb'))
            else:
                pass
        except Exception as e:
            tk.messagebox.showerror(title="Upload Error", message=e)

        # upload işlemi ve list yenileme
        self.list_dir()

    def download(self):
        try:
            filename = self.selection()
            if(filename):
                localfile = open(filename, 'wb')
                self.ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
            else:
                pass
            localfile.close()
        except Exception as e:
            tk.messagebox.showerror(title="Download Error", message=e)

    def create_dir(self):

        name = askstring('Name', 'Enter Filename')
        try:
            if(name in self.ftp.nlst()):
                tk.messagebox.showwarning(
                    title="Directory Error", message="Directory already exists!")
            else:
                self.ftp.mkd(name)
                self.list_dir()

        except Exception as e:
            tk.messagebox.showerror(title="Directory Error", message=e)

    def change_name(self):
        try:
            new_name = askstring('Name', 'Enter new file name:')
            if(new_name in self.ftp.nlst()):
                tk.messagebox.showwarning(
                    title="File name Error", message="File already exists!")
            else:
                self.ftp.rename(self.selection(), new_name)
                self.list_dir()
        except Exception as e:
            tk.messagebox.showerror(title="Renaming Error", message=e)

    def change_dir(self):

        directory = self.selection()

        try:
            msg = self.ftp.cwd(directory)

        except Exception as e:
            tk.messagebox.showerror(title="Directory Change Error", message=e)
        self.liste.delete(0, 'end')

        self.list_dir()

    # GET SELECTED LISTBOX ITEM NAMES
    def selection(self):
        all_items = self.liste.get(0, tk.END)
        sel_idx = self.liste.curselection()
        sel_list = [all_items[item] for item in sel_idx]
        return sel_list[0]

    def exit(self):

        self.ftp.quit()
        print("Connection closed")
        self.destroy()


# %%  APP INTERFACE AFTER SUCCESSFUL LOGIN


    def user_interface(self):
        self.minsize(450, 450)

        self.files = tk.Label(self, text="FILES:", font=(
            "Helvetica", 12), justify=tk.LEFT)
        self.files.grid(column=0, row=3, sticky=tk.W)
        self.war = tk.Label(self, text="(/ :home directory.)",
                            font=("Helvetica", 8), justify=tk.LEFT)
        self.war.grid(column=1, row=3, sticky=tk.W)

        self.sil = tk.Button(self, text="DELETE", bg="black",
                             fg="white", command=self.delete)
        self.sil.grid(column=0, row=7, sticky=tk.E+tk.W+tk.S+tk.N)

        self.up = tk.Button(self, text="UPLOAD", bg="black",
                            fg="white", command=self.upload)
        self.up.grid(column=1, row=7, sticky=tk.E+tk.W+tk.S+tk.N)

        self.down = tk.Button(self, text="DOWNLOAD",
                              bg="black", fg="white", command=self.download)
        self.down.grid(column=2, row=7, sticky=tk.E+tk.W+tk.S+tk.N)

        self.make_dir = tk.Button(
            self, text="CREATE FOLDER", bg="black", fg="white", command=self.create_dir)
        self.make_dir.grid(column=3, row=7, sticky=tk.E+tk.W+tk.S+tk.N)

        self.change_n = tk.Button(
            self, text="RENAME", bg="black", fg="white", command=self.change_name)
        self.change_n.grid(column=4, row=7, sticky=tk.E+tk.W+tk.S+tk.N)

        self.cikis = tk.Button(self, text="LOGOUT",
                               bg="RED", fg="BLACK", command=self.exit)
        self.cikis.grid(column=5, row=7, sticky=tk.E+tk.W+tk.S+tk.N)

        self.liste = tk.Listbox(self, width=50, height=20)
        self.liste.grid(column=0, row=5, padx=2, pady=2,
                        columnspan=10,  sticky=tk.E+tk.W+tk.S+tk.N)
        self.liste.bind('<Double-1>', lambda x: self.change_dir())


# %% MAIN
root = Root()
root.mainloop()
