from configparser import ConfigParser


# create a user config
def create_user_settings():
    # define config objects
    config = ConfigParser()
    # define USER
    config["USER"] = {
        "username": "default",
        "password": 0000,
        "friends": [],
        "role": "server"
    }
    # save user into .ini
    with open("user_info.ini", "w") as f:
        config.write(f)
        f.close()


# update user information
def update_user(config, username: str = "default", password: int = 0000, friend=None, role: str = "server"):
    # will be changed after adding friends by database configuration
    if friend is None:
        friend = []

    # config = ConfigParser()
    # define USER
    config["USER"] = {
        "username": username,
        "password": password,
        "friends": friend,
        "role": role
    }
    # save updated USER into .ini file
    with open("user_info.ini", "w") as f:
        config.write(f)
        f.close()


# read user config file
def read_config():
    config = ConfigParser()
    config.read("user_info.ini")
    return config


# return username
def get_uname():
    config = ConfigParser()
    config.read("user_info.ini")
    user = config["USER"]
    user = user["username"]
    return user


# change role
def change_connection_key(config: ConfigParser, role: str):
    user_infor = config["USER"]
    uname = user_infor["username"]
    passwd = user_infor["password"]
    friends = user_infor["friends"]
    #role = user_infor["role"]

    config["USER"] = {
        "username": uname,
        "password": passwd,
        "friends": friends,
        "role": role
    }
    with open('user_info.ini', 'w') as f:
        config.write(f)
        f.close()


# return connection key
def get_conn_key():
    config = ConfigParser()
    config.read("user_info.ini")
    user = config["USER"]
    key = user["role"]
    return key


# upcoming after regulating friend part
def remove_friend(name):
    pass


# upcoming after regulating friend part
def add_friend(name):
    pass


# create network configuration file
def create_network_settings():
    # define config object
    config = ConfigParser()
    # define NETWORK
    config["NETWORK"] = {
        "port": 5555,
        "max_user": 25
    }
    # save NETWORK into .ini config file
    with open("network.ini", "w") as f:
        config.write(f)
        f.close()


# return config file read object
def return_network_settings():
    config = ConfigParser()
    config.read("network.ini")
    config = config["NETWORK"]
    # print(config['port'])
    return config


# change port by incrementing one by one
def change_port():
    config = ConfigParser()
    # get max user and port from network configuration file
    config.read("network.ini")
    config = config["NETWORK"]
    port = config['port']
    max_user = config['max_user']
    # if initial port 5555 is full change it to another port
    if port == 5555:
        changed_port = 48808
    else:
        # increment port
        changed_port = int(port) + 1

    changed_config = ConfigParser()
    changed_config["NETWORK"] = {
        "port": changed_port,
        "max_user": max_user
    }

    # save changed NETWORK into .ini config file
    with open("network.ini", "w") as f:
        changed_config.write(f)
        f.close()


#create_network_settings()
#create_user_settings()
# get_uname()
print(get_conn_key())
