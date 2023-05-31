# Written by Sadik Emre Duzgun
import subprocess
import requests
import json
import time


# start program
def return_invite_key():
    # check if ngrok is working
    try:
        ngrok_working = subprocess.Popen(['powershell', 'Get-Process ngrok -ErrorAction SilentlyContinue'], stdout=subprocess.PIPE)
    # when it is linux
    except:
        ngrok_working = subprocess.Popen(['ps aux | grep ngrok'])
    # start if ngrok is not working by performing error handling
    try:
        # if ngrok is not working
        if not ngrok_working.stdout.read().decode():
            # start ngrok at port 5555
            try:
                ngrok = subprocess.Popen(['ngrok','tcp','5555'],stdout=subprocess.PIPE)
            except:
                ngrok = subprocess.Popen(['./ngrok', 'tcp', '5555'],stdout=subprocess.PIPE)
    except Exception as e:
        print(e)
    # tunnel url can't be taken using subprocess because of a problem
    # wait for ngrok to fetch the url from the server
    time.sleep(3)
    # get url
    localhost_url = "http://localhost:4040/api/tunnels"
    # get tunnel url information
    tunnel_url = requests.get(localhost_url).text
    # load xml information into json
    j = json.loads(tunnel_url)
    # parse to get tunnel url
    tunnel_url = j['tunnels'][0]['public_url']
    print(tunnel_url)
    tunnel_url = str(tunnel_url)
    invite = tunnel_url.split(':')[1][2:len(tunnel_url.split(':')[1])]+"&"+tunnel_url.split(':')[2]
    print(invite)
    # send invite key to be shared
    return invite
    # encrypt the invite and add encryption key in.


print(return_invite_key())
