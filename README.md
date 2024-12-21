# OSC Leash for PiShock
This program will take a float value from VRChat using OSC to continually shock the user using a PiShock. The PiShock API can only do minimum of 1 second shocks, so it is what it is. There is also some delay in the API that I can't do anything with.

Yes I know this script is a mess, I originally made it for a different use and ended up frankensteining it into this. It is my first python script that actually does something useful, so don't expect beautiful code if you decide to look through it.

## 2.0 is using MultiShock
It can shock multiple shockers and has less delay than 1.0
It has some different variables:
- **Websocket:** The websocket used. Default value is "ws://localhost:8765" and should be correct. See MultiShocks website if you already use that port.
- **AuthKey:** Set the same auth key here as in the settings tab in MultiShock.
- **Delay:** The delay in seconds between shocks. I have found that a value of 0.5 will feel like a continous shock.

The rest should be the same as for 1.0, so go read that too.

## How to use (1.0): 
The program will make a .json file to save its data.
Input everything and click each set button. Next time you open this will be saved.

- **Parameter:** The stretch parameter used in VRC (or any other float). E.g. "/avatar/parameters/Leash_Stretch"
- **Username:** Username you use to log into PiShock.com. Can be found in the Account section of the website.
- **API-key:** API Key generated on PiShock.com Can be found in the Account section of the website.
- **Sharecode:** Sharecode generated on PiShock.com. Limitations can be set when generating the code.
- **Max shock value:** What the maximum shock value will be when the parameter is 1.

When everything is set up, click "Set parameter" to start the program. 
Next time you open the program you only need to click "Set parameter" for it to start working.

If you want to change the port you can do so in the .json file. Remember to restart the program after doing so.

If being used with a leash, setup whatever leash you want with a PhysBone script. Set max stretch to whatever you want, I like to have it around 0.5 - 1. If the stretch is too low it can be difficult to control and act more like a on/of interraction. At the bottom under Options you will have to add a parameter, I have used "Leash". The PhysBone script will then make a parameter called "Leash_Stretch" that can be used in the program.
VRChat also adds some bits to the parameter which is "/avatar/parameters/" so you will then end up with the entire parameter that goes into the program which is "/avatar/parameters/Leash_Stretch"

##
Compiled to .exe using PyInstaller
