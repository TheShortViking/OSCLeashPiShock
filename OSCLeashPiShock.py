import customtkinter
import asyncio
from typing import List, Any
from pythonosc import dispatcher
from pythonosc import osc_server
import aiohttp
import requests
import json
import os
import signal

Port = 9001
Username = "Type here"
APIkey = "Type here"
ShareCode = "Type here"
MaxShock = 20
para = "Type Here"
SaveFile = "OSCLeashPiShockSave.json"


def saveVars():
    data_to_save = {
        "UsernameSaved" : Username,
        "APIkeySaved" : APIkey,
        "ShareCodeSaved" : ShareCode,
        "MaxShockSaved" : MaxShock,
        "paraSaved" : para,
        "PortSaved" : Port
    }
    with open(SaveFile, 'w') as file:
        json.dump(data_to_save, file)

if not os.path.exists(SaveFile):
    saveVars()

else:
    with open(SaveFile, 'r') as file:
        loaded_data = json.load(file)
    Username = loaded_data["UsernameSaved"]
    APIkey = loaded_data["APIkeySaved"]
    ShareCode = loaded_data["ShareCodeSaved"]
    MaxShock = loaded_data["MaxShockSaved"]
    para = loaded_data["paraSaved"]
    Port = loaded_data["PortSaved"]
oldPara = "null"

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.geometry("700x600")
frame = customtkinter.CTkFrame(master=root)
frame.grid()
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


def setPara():
    global para
    global oldPara
    print("set")
    para = paraEntry.get()
    saveVars()
    disp.map(para, setVal)
    if (para != oldPara) and (oldPara != "null"):
        disp.unmap(oldPara, setVal)
    oldPara = para

def setUsername():
    global Username
    Username = UsernameEntry.get()

def setAPIkey():
    global APIkey
    APIkey = APIkeyEntry.get()

def setShareCode():
    global ShareCode
    ShareCode = ShareCodeEntry.get()

def setMaxShock():
    global MaxShock
    MaxShock = int(MaxShockEntry.get())

def die():
    print("QUIT")
    os.kill(os.getpid(), signal.SIGTERM)

mainLabal = customtkinter.CTkLabel(master=frame, text="OSC Leash for PiShock", font=("CTkDefaultFont",20))
mainLabal.grid(row=0, column=0, pady=20, padx=20)

paraEntry = customtkinter.CTkEntry(frame, width = 400)
paraEntry.insert(0, para)
paraEntry.grid(row=1, column=0, pady=20, padx=20)

button = customtkinter.CTkButton(frame, text = "Set parameter", command = setPara)
button.grid(row = 1, column = 1, sticky = customtkinter.W, padx=20)

UsernameEntry = customtkinter.CTkEntry(frame, width = 400)
UsernameEntry.insert(0, Username)
UsernameEntry.grid(row = 2, column = 0, pady=20, padx=20)
UsernameButton = customtkinter.CTkButton(frame, text = "Set Username", command = setUsername)
UsernameButton.grid(row = 2, column = 1, sticky = customtkinter.W, padx=20)

APIkeyEntry = customtkinter.CTkEntry(frame, width = 400)
APIkeyEntry.insert(0, APIkey)
APIkeyEntry.grid(row = 3, column = 0, pady=20, padx=20)
APIkeyButton = customtkinter.CTkButton(frame, text = "Set API-key", command = setAPIkey)
APIkeyButton.grid(row = 3, column = 1, sticky = customtkinter.W, padx=20)

ShareCodeEntry = customtkinter.CTkEntry(frame, width = 400)
ShareCodeEntry.insert(0, ShareCode)
ShareCodeEntry.grid(row = 4, column = 0, pady=20, padx=20)
ShareCodeButton = customtkinter.CTkButton(frame, text = "Set Sharecode", command = setShareCode)
ShareCodeButton.grid(row = 4, column = 1, sticky = customtkinter.W, padx=20)

MaxShockEntry = customtkinter.CTkEntry(frame, width = 400)
MaxShockEntry.insert(0, MaxShock)
MaxShockEntry.grid(row = 5, column = 0, pady=20, padx=20)
MaxShockButton = customtkinter.CTkButton(frame, text = "Set max shock value", command = setMaxShock)
MaxShockButton.grid(row = 5, column = 1, sticky = customtkinter.W, padx=20)

slider = customtkinter.CTkProgressBar(frame, width = 400)
slider.grid(row=6, column=0, pady=20, padx=20)

quitButton = customtkinter.CTkButton(frame, text="Quit", command=die, fg_color="red", hover_color="darkred")
quitButton.grid(row=7, column=0, pady=20, padx=20)

async def tkinterloop():
    while True:
        root.update()
        await asyncio.sleep(0.1)


ShockVal = "0"
pos = 0.0

url = 'https://do.pishock.com/api/apioperate'
async def loop():

    while True:
        ShockVal2 = int(ShockVal)
        try:
            slider.set(pos)
        except:
            print()
        if ShockVal2 != 0:
            print("sending ",ShockVal2)
            data = {
                "Username": Username,
                "Name": "OSCLeashPiShock",
                "Code": ShareCode,
                "Intensity": ShockVal2,
                "Duration": 1,
                "Apikey": APIkey,
                "Op": "0"
                }
            json_data = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, data=json_data, headers=headers) as response:
                        # Check the response
                        if response.status == 200:
                            print("Request was successful.")
                            #print(await response.json())  # If the response is in JSON format
                        else:
                            print(f"Request failed with status code {response.status}")
                            print(await response.text())  # Print the response content for further inspection
            except:
                print("except ", ShockVal2)
        else:
            print("not sending ", ShockVal2)
        await asyncio.sleep(0.1)


def setVal(address, args) -> None:
    global ShockVal
    global pos
    pos = args
    ShockVal = args*MaxShock
    print(ShockVal)

def handler(address, args) -> None:
    #print("handler ", args)
    #print()
    return

disp = dispatcher.Dispatcher()

disp.set_default_handler(handler)

async def init_main():
    server = osc_server.AsyncIOOSCUDPServer(("127.0.0.1", Port), disp, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    task = asyncio.create_task(tkinterloop())
    #await loop()  # Enter main loop of program
    await asyncio.gather(loop())

    transport.close()  # Clean up serve endpoint


asyncio.run(init_main())