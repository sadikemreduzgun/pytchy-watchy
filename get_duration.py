# import packages
import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import socket

# atvwebplayersdk-playpause-button


def stop_continue_movie(driver:webdriver.Chrome):
    try:
        # move the mouse to be able to stop the movie
        pyautogui.moveTo(pyautogui.position()[0] + 10, pyautogui.position()[1] + 10, 1)
        # stop the movie
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "atvwebplayersdk-playpause-button"))
        ).click()

    # if error, write it
    except:
        print("couldn't stop movie")


def receive_mov(client:socket.socket, webdriver:webdriver.Chrome):
    while True:
        get = client.recv(1024)
        get = get.decode("utf-8")
        if get[0] == '!':
            stop_continue_movie(webdriver)


def handle_duration(client:socket.socket):
    # define chrome driver
    driver = webdriver.Chrome()
    # get the movie's link
    driver.get("https://www.primevideo.com/")
    #threading.Thread(target=receive, args=(client,))

    while True:
        try:
            # get the element including time duration
            elem = driver.find_element(By.CLASS_NAME,"atvwebplayersdk-seekbar-range")
            # get time duration
            sa = elem.get_attribute("aria-valuetext")
            print(sa)
            min_sec = sa.split(':')
            total = int(min_sec[0])*60*60 + int(min_sec[1])*60 + int(min_sec[2])
            total = "+" + str(total)
            client.send(total.encode())
            #stop_continue_movie(driver)
            # wait for a second
            time.sleep(1)

        except:
            # wait for signing in
            print("waiting for opening the movie")
            time.sleep(3)

