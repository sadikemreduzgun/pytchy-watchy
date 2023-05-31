import socket, time,os, random
import threading
# from main import *
import typing
from config import return_network_settings, change_port


# define server object
class Server:

    def __init__(self):
        # define initial variables
        self.config = return_network_settings()
        # get max user
        try:
            self.max_user = int(self.config['max_user'])
        except:
            self.max_user = 25
        # create socket object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # define local tunneling port to be 5555
        try:
            self.port = int(self.config['port'])
            self.server_socket.bind(('', self.port))
        # change port if port 5555 full
        except:
            tries = 0
            # run while free ports are running out
            while tries < 23:
                # change port
                change_port()

                try:
                    # get changed port and start streaming
                    self.port = int(self.config['port'])
                    self.server_socket.bind(('', self.port))
                    # if successful, stop trying
                    break
                except:
                    tries += 1

        # listen coming connections
        self.server_socket.listen(self.max_user)
        self.new_message = False
        # define client list to add connected clients
        self.client_list = []
        # define a duration directory to keep durations and perform on them
        self.durations = {}
        self.once_exec = True
        self.count = 0

    def handle_message(self, client:socket.socket):

        while True:
            # cool down
            time.sleep(1)

            try:
                print("in server")
                # get message by event handling
                msg = client.recv(1024)
                # if client left the connection stop
                if not msg.decode("utf-8"):
                    break

                # if message is not a time duration
                if msg.decode("utf-8")[0] != '+':
                    print(msg.decode("utf-8"))

                    try:
                        # get message and username by splitting
                        splitted = msg.decode("utf-8").split('&')
                        message = splitted[1] + "> " + splitted[0]
                        print(splitted[1], "> ", splitted[0])

                    except:
                        # if message doesn't include a username
                        message = msg.decode("utf-8")

                    try:
                        for clients in self.client_list:

                            print("message: ", message)
                            # important!
                            # send incoming message to all clients to be placed on messaging gui
                            clients.send(message.encode())
                            # fill duration directory
                            if self.once_exec:
                                self.durations[clients] = 1
                                self.once_exec = False
                    # people are waited
                    except:
                        # no other client
                        print("other clients are waited")
                # if a incoming data is time duration
                else:
                    # add the duration to the dictionary
                    self.durations[client] = msg.decode("utf-8")[0:len(msg.decode("utf-8"))-1]
                    print(msg.decode("utf-8")[0:len(msg.decode("utf-8"))-1])
                    print(self.durations)
                    # if directory is filled by steps
                    if self.count%len(self.durations) == 0:
                        print("inside")
                        # list(sa.keys())[1]
                        # order the time durations
                        for j in range(len(self.durations)):
                            # ordering using bubble sort algorithm
                            for i in range(len(self.durations)-1):
                                if list(self.durations.values())[i] < list(self.durations.values())[i+1]:
                                    hold = list(self.durations.values())[i]
                                    list(self.durations.values())[i] = list(self.durations.values())[i+1]
                                    list(self.durations.values())[i+1] = hold

                        # if difference is more than 9 seconds
                        for i in range(len(self.durations)-1):
                            if (list(self.durations.values())[i+1] - list(self.durations.values())[i])>9:
                                (list(self.durations.keys())[i+1]).send("!stop".encode())

                    print(self.durations)
            # exception handling when there is a problem og a huge code block, not possible
            except Exception as e:
                print(e)
                print("there are others")
            # incrase count to be used for duration checker
            self.count += 1
        # stop client at the end
        client.close()

    def choose_user_pm(self):
        pass

    # def send_pm(self):
        # option = tkinter.OptionMenu(root, stvar, *self.client_list)

    # function to handle connection
    def handle_connection(self):
        c = 0
        # max 25 connections are accepted and max 25 clients are defined
        while c < 25:
            # get client by accepting its connection
            client_socket, addr = self.server_socket.accept()
            # add client to client list
            self.client_list.append(client_socket)
            # start handler
            rec = threading.Thread(target=self.handle_message, args=(client_socket,))
            rec.start()
            # sendo = threading.Thread(target=send, args=(client_socket,))
            # sendo.start()

            try:
                client_socket.send("..connected".encode())
            except:
                print("ex")

            print("connect", addr)
            c += 1
            # client_socket.close()


# define and start server
server = Server()
server.handle_connection()
