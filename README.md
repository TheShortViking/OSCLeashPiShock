# OSCLeashPiShock
This program will take a float value from VRChat using OSC to continually shock the user using a PiShock. The PiShock API can only do minimum of 1 second shocks, so it is what it is. There is also some delay in the API that I can't do anything with.

Yes I know this script is a mess, I originally made it for a different use and ended up frankensteining it into this. It is my first python script that actually does something useful, so don't expect beautiful code if you decide to look through it.

## How to use: 
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

If being used with a leash, setup whatever leach you want with a PhysBone script. At the bottom you will have to add a parameter, I have used "Leash". The physbone script will then make a parameter called "Leash_Stretch" that can be used in the program.


