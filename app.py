import time
import tkinter
from tkinter import *  # all
# GUI
import pyautogui
import threading
from client import *
from get_duration import stop_continue_movie


# define App class
class App:
    def __init__(self):
        # define objects
        self.root = Tk()
        # make gui full screen
        self.root.attributes('-fullscreen', True)
        # give gui a title
        self.root.title('Pytch Watch')
        # make gui transparent
        self.root.wm_attributes("-transparentcolor", '#ab23ff')
        Text(self.root, bg='#ab23ff', borderwidth=0).pack(fill=BOTH, side=LEFT, expand=1)
        # define objects
        self.send_msg2 = Text(self.root, width=21, height=3, fg='black', bg='green', borderwidth=0)
        self.button = Button(self.root, text="send", width=3, height=1, bg='blue', borderwidth=0, fg='yellow', command=self.send_mes)

        self.stop_threads = False
        self.chat_area = Listbox(self.root, width=24,height=23, bg='#ab23ff', fg='purple', borderwidth=0,
                                 selectbackground='purple', selectforeground='purple', font=('Helvetica 18'))

        self.thread = threading.Thread(target=self.check_pos)
        self.wait_message = threading.Thread(target=recieve_movie, args=(s,self.chat_area))
        self.username = "default"

    # get username from txt file
    def get_username(self):
        file = open('username.txt', 'r')
        self.username = file.read()
        file.close()

    # get input from text object
    def send_mes(self):
        taken = self.send_msg2.get(1.0, tkinter.END)
        taken = taken[0:len(taken)-1]
        self.get_message(self.username, taken)

    # a thread function to check position of the mouse and create messaging part, Text and Button or remove them
    def check_pos(self):
        # root.bind("<c>", func())

        while True:
            # if tkinter is close finish thread
            if self.stop_threads:
                break
            # frame.pack()
            print(pyautogui.position())
            # mouse is at right side
            if pyautogui.position()[0] > 1494:
                # bring back the messaging part
                self.chat_area.pack(fill=BOTH, side=TOP, expand=1)
                #            send_msg.pack(side=BOTTOM,fill=BOTH, expand=1)
                # send_msg2.grid()
                self.send_msg2.pack(fill=BOTH, side=BOTTOM, expand=1)
                self.button.pack(fill=BOTH, side=BOTTOM, expand=1)
            # mouse is on the left side
            else:
                # remove messaging objects from screen
                self.chat_area.pack_forget()
                # send_msg.pack_forget()
                self.send_msg2.pack_forget()
                self.button.pack_forget()
            # wait a second
            time.sleep(1)

    # send message to server
    def get_message(self, nick, message):

        out = "[" + nick + "]" + ": " + message
        send(s, nick, out)

        self.wait_message.start()

    # run app
    def start_app(self):
        self.get_username()
        self.thread.start()
        self.root.mainloop()
        self.stop_threads = True


it = App()
it.start_app()
