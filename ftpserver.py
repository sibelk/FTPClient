# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 17:34:03 2020

@author: sibel
"""


from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os
import tkinter as tk

#%% SERVER İCİN CALİSİLAN DİZİNDE Server ADLİ DOSYA OLUSTURMA

path = os.getcwd()
folder= "\\Server"


try:
    # Create target Directory
    os.mkdir(path+folder)
    print("Directory " , path+folder ,  " Created ") 
except FileExistsError:
    print("Directory " , path+folder ,  " already exists") 


#%% FTP SERVER
authorizer = DummyAuthorizer()
authorizer.add_user("user", "12345", path+folder, perm="elradfmwMT")
authorizer.add_anonymous(path+folder)

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("localhost", 21), handler)
try:
    server.serve_forever()
except Exception as e:
    server.s
    tk.messagebox.showerror(title="Server Error", message=e)
