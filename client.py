import socket
import time
import tkinter
# from tkinter import *
from invite import return_invite_key
import threading
from config import *

try:
    username = get_uname()
    username = str(username)
    print(username)
except:
    # open the username file and read it
    file = open('username.txt', 'r')
    # read username
    username = file.read()
    # close the file
    file.close()
    # username = user

# open the roling file and read it
file = open('role.txt', 'r')


# get invite and just return back host and port
# not totally encrypted for now
def decrypt_invite(invite:str):
    host_name_n_port = invite.split('&')
    return host_name_n_port[0], host_name_n_port[1]


inside = file.read()
file.close()
print(inside)
# if host get itself's host and port created by ngrok
if inside == "host":
    host, port = decrypt_invite(return_invite_key())
else: # get the invite
    # split the role and the key
    all = inside.split(':')
    print(all)
    # split host and port in the key
    all = all[1].split('&')
    # assign host and port
    host = all[0]
    port = all[1]

# create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# start streaming
s.connect((host, int(port)))


# get data from server and used by to gui
def recieve(s:socket.socket, listbox: tkinter.Listbox):
    while True:
        try:
            # how big of data is determined, buffer size
            msg = s.recv(1024)
            print(msg.decode("utf-8"))
            time.sleep(1)
            listbox.insert(tkinter.END, msg)

            if msg == 'q':
                break
        except:
            time.sleep(1)

    s.close()


# get data from server and use it in movie messaging part
def recieve_movie(s:socket.socket, listbox: tkinter.Listbox):
    while True:
        try:
            # how big of data is determined, buffer size
            msg = s.recv(1024)
            print(msg.decode("utf-8"))
            if msg.decode("utf-8")[0] == '!':
                pass
            else:
                listbox.insert(tkinter.END, msg)
            time.sleep(1)
            if msg == 'q':
                break
        except:
            time.sleep(1)

    s.close()


# send data to server
def send(s:socket.socket, username:str, msg:str):
    all = username + "&" + msg
    s.send(all.encode())


# rec = threading.Thread(target=recieve, args=(s,))
sen = threading.Thread(target=send, args=(s,username))
