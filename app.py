import os
import json
import base64
import subprocess
import _thread as thread
import time

UUID = "2ac61062-7cad-4d10-b84a-a3e4ac286bd6"
PATH = "/sss"
IBMEMAIL = "email"
IBMPASS = "password"
CFNAME = "app name"


def restart():

    time.sleep(30)
    args = ("rm", "app","a.json", "a.py", "-rf")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    print(output)

    time.sleep(60*60*24*4)

    args = ("./cf", "l", "-a", "https://api.us-south.cf.cloud.ibm.com",
            "login", "-u", IBMEMAIL, "-p", IBMPASS)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    print(output)

    args = ("./cf", "rs", CFNAME)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    print(output)


if __name__ == '__main__':
    with open("source.py", "rb") as f:
        with open('app', 'wb') as fi:
            app = base64.b64decode(f.read())
            fi.write(app)
            fi.close()
        f.close()

    data = {}

    inbounds = {}
    settings = {}
    clients = {}
    clients["id"] = UUID
    clients["level"] = 0
    settings["clients"] = [clients]
    settings["decryption"] = "none"
    streamSettings = {}
    streamSettings["network"] = "ws"
    path = {}
    path["path"] = PATH
    streamSettings["wsSettings"] = path
    inbounds["port"] = 8080
    inbounds["protocol"] = "vless"
    inbounds["settings"] = settings
    inbounds["streamSettings"] = streamSettings

    protocol = {}
    protocol["protocol"] = "freedom"

    data["inbounds"] = [inbounds]
    data["outbounds"] = [protocol]

    with open("a.json", "w") as fjs:
        json.dump(data, fjs)
        fjs.close
    args = ("chmod", "+x", "a.json")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    print(output)

    args = ("chmod", "+x", "app")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    print(output)

    thread.start_new_thread(restart, ())

    args = ("./app", "-c", "a.json")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    print(output)
    print("ok")
