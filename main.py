# import packages
import subprocess
import time
import tkinter
from tkinter import *
from invite import return_invite_key
from get_duration import handle_duration
import threading
from config import *

# read and assign config variable
config = ConfigParser()
config.read("user_info.ini")

# try to get username, if error username is the username in username.txt
try:
    # reach USER
    user = config["USER"]
    # get username
    name = user["username"]
    # print(name)
    # print(type(name))

    # if username is default, open a GUI to change it
    if name == "default":
        # define a function to open a tkinter windows
        # that window better to be a local variable not to have an interference
        def get_username():
            # assign tkinter object
            user_w = Tk()
            # define winsize
            user_w.geometry("1200x920")
            # define title
            user_w.title("Pythch Watch")
            # make background green
            user_w.configure(bg="green")
            # block sizing
            user_w.resizable(False, False)

            # define a function of button
            def change_username():
                # get input text
                entry = text.get(1.0, tkinter.END)
                # remove \n
                entry = entry[0:len(entry)-1]
                # print(entry)
                # change username in config
                update_user(config=config, username=entry)
                # close window
                user_w.destroy()

            # define tkinter objects
            text = tkinter.Text(user_w, height=2, width=20)
            text_button = tkinter.Button(user_w, text="get a username", command=change_username)
            # place tkinter objects
            text.pack(anchor=CENTER, pady=280)
            text_button.pack(anchor=CENTER, pady=0)
            # start window
            user_w.mainloop()

        # run function
        get_username()

except:
    print("couldn't get username")
    # write in log file
    # removed

    # exit(0)

# open file for client-server rıke
#file = open("role.txt", "w")
# define tkinter object, as windows
root = Tk()
# give the windows a size
root.geometry('1200x920')
# give it a title
root.title('Pythch Watch')
# make background green
root.configure(background='green')
# limit sizing
root.resizable(False, False)


# function for entering invite key
def enter_click():
    # remove buttons from screen and pack new ones
    button_invite_generate.pack_forget()
    button_invite_entry.pack_forget()
    invitation.pack(pady=100)
    enter_button.pack()


# server code to be worked as thread
def run_server():
    subprocess.Popen(['powershell', 'python.exe server.py'])


# function for creating an invite key
def generate_click():
    button_invite_generate.pack_forget()
    button_invite_entry.pack_forget()
    # invitation area
    print(1)
    invite_area.insert(END, return_invite_key())
    invite_area.pack(pady=80)
    next_button.pack()
    try:
        change_connection_key(config, "host")
    except:
        file = open("role.txt", "w")
        file.write("host")
        file.close()
    # define thread
    server = threading.Thread(target=run_server)
    #subprocess.Popen(['powershell', 'python.exe server.py'])
    # start thread
    server.start()


# get invitation
def enter_invite():
    entry = invitation.get(1.0, tkinter.END)
    print(entry[0:len(entry)-1])
    next_button.pack()
    # write client role and key
    try:
        change_connection_key(config, "client:"+ entry)
    except:
        file = open("role.txt", "w")
        file.write("client:"+ entry)
        file.close()


# remove objects from screen and go messaging part
def go_next():
    invite_area.pack_forget()
    next_button.pack_forget()
    invitation.pack_forget()
    enter_button.pack_forget()
    next_button.pack_forget()

    messaging_area.pack(side=TOP)
    send_message_text.pack(pady=4)
    send_message_button.pack(pady=4)
    option.pack(side=LEFT, padx=10)
    choose_button.pack(side=LEFT, padx=10)
    start_movie_button.pack(side=RIGHT, padx=10)
    # import packages after giving role
    # importing client needs a role client or server
    from client import recieve
    from client import s
    rec = threading.Thread(target=recieve, args=(s, messaging_area))
    rec.start()


# definitions of tkinter screen objects
invite_area = tkinter.Listbox(height=1, width=30)
button_invite_generate = tkinter.Button(command=generate_click, text='Generate Invitation Key', height=10, width=20, bg='blue')
button_invite_entry = tkinter.Button(command=enter_click, text='Enter Invitation', height=10, width=20, bg='blue')
next_button2 = tkinter.Button(text='next')
#button_invite_entry.grid_location(100,100)

button_invite_entry.pack(padx=100, pady=100, side=LEFT)
button_invite_generate.pack(padx=100, pady=100, side=RIGHT)
#button_invite_generate.grid_location(200,500)
invitation = tkinter.Text(height=2, width=30)
enter_button = tkinter.Button(text='Enter Invitation', command=enter_invite)

next_button = tkinter.Button(text='Next', command=go_next)


# messaging part
# sending message to server
def send_message():
    # send message using socket
    message = send_message_text.get(1.0, tkinter.END)
    message = message[0:len(message)-1]
    try:
        from client import s
    except:
        print("Couldn't get socket! ")

    from client import username
    from client import send
    from client import s
    try:
        send(s, username, message)
    except:
        messaging_area.insert(END, "Couldn't connect! There is a problem with invite key! ")
    try:
        for pos in messaging_area.curselection():
            print(pos)
    except:
        pass


# write message to chatting area and go down
def insert_message(message, username):
    send_that = "[" + username + "]" + "> " + message
    messaging_area.insert(END, send_that)
    messaging_area.yview(END)
    messaging_area.update()


# creation of messaging objects
messaging_area = tkinter.Listbox(height=20, width=100)
# bottom
send_message_text = tkinter.Text(height=2, width=75)
send_message_button = tkinter.Button(text='Send Message', command=send_message)

# define of option for pm
stvar = tkinter.StringVar()
# choose someone to send pm
# couldn't have enough time
users = ["user1", "user2"]
option = tkinter.OptionMenu(root, stvar, *users)


def choose_user_pm():
    pass


# close the window and start movie
def start_movie():
    root.destroy()
    from client import s
    open_movie = threading.Thread(target=handle_duration, args=(s,))
    #handle_duration(s)
    open_movie.start()
    time.sleep(90)
    subprocess.Popen(['powershell', 'python.exe app.py'])
    #exit(0)
    #from app import App


# right
choose_button = tkinter.Button(text='Send PM', command=choose_user_pm)
start_movie_button = tkinter.Button(text='Go Watch Movie', command=start_movie)
#from client import *
# start app
root.mainloop()
