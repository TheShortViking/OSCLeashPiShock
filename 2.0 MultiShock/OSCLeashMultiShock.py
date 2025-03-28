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
import websockets

Port = 9001
WebsocketVar = "ws://localhost:8765"
AuthKey = "Type Here"
DelayVar = float(0.5)
MaxShock = 20
para = "Type Here"
SaveFile = "OSCLeashMultiShockSave.json"

def saveVars():
    data_to_save = {
        "WebsocketVarSaved" : WebsocketVar,
        "AuthKeySaved" : AuthKey,
        "DelayVarSaved" : DelayVar,
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
    WebsocketVar = loaded_data["WebsocketVarSaved"]
    AuthKey = loaded_data["AuthKeySaved"]
    DelayVar = loaded_data["DelayVarSaved"]
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

def setWebsocketVar():
    global WebsocketVar
    WebsocketVar = WebsocketVarEntry.get()
    saveVars()

def SetAuthKey():
    global AuthKey
    AuthKey = AuthKeyEntry.get()
    saveVars()

def setDelayVar():
    global DelayVar
    DelayVar = float(DelayVarEntry.get())
    saveVars()

def setMaxShock():
    global MaxShock
    MaxShock = int(MaxShockEntry.get())
    saveVars()

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

WebsocketVarEntry = customtkinter.CTkEntry(frame, width = 400)
WebsocketVarEntry.insert(0, WebsocketVar)
WebsocketVarEntry.grid(row = 2, column = 0, pady=20, padx=20)
WebsocketVarButton = customtkinter.CTkButton(frame, text = "Set Websocket", command = setWebsocketVar)
WebsocketVarButton.grid(row = 2, column = 1, sticky = customtkinter.W, padx=20)

AuthKeyEntry = customtkinter.CTkEntry(frame, width = 400)
AuthKeyEntry.insert(0, AuthKey)
AuthKeyEntry.grid(row = 3, column = 0, pady=20, padx=20)
AuthKeyButton = customtkinter.CTkButton(frame, text = "Set Auth key", command = SetAuthKey)
AuthKeyButton.grid(row = 3, column = 1, sticky = customtkinter.W, padx=20)


DelayVarEntry = customtkinter.CTkEntry(frame, width = 400)
DelayVarEntry.insert(0, DelayVar)
DelayVarEntry.grid(row = 4, column = 0, pady=20, padx=20)
DelayVarButton = customtkinter.CTkButton(frame, text = "Set Delay", command = setDelayVar)
DelayVarButton.grid(row = 4, column = 1, sticky = customtkinter.W, padx=20)


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

async def loop():

    while True:
        ShockVal2 = int(ShockVal)
        try:
            slider.set(pos)
        except:
            print()
        if ShockVal2 != 0:
            print("sending ",ShockVal2)
            payload = {
                "cmd": "operate",
                "value": {
                    "intensity": ShockVal2, 
                    "duration": 0.1,
                    "shocker_option": "all", 
                    "action": "shock", 
                    "shocker_ids": [], 
                    "device_ids": [], 
                    "warning": False,
                    "held": False,
                },
                "auth_key": AuthKey
                }
            try:
                async with websockets.connect(WebsocketVar) as websocket:
                    # Send the JSON payload
                    await websocket.send(json.dumps(payload))
                    print(f"Sent: {payload}")

                    # Wait for a response
                    #response = await websocket.recv()
                    #print(f"Received: {response}")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("not sending ", ShockVal2)
        await asyncio.sleep(DelayVar)


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
