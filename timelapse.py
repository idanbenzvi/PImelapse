from picamera import PiCamera #camera interface API
import subprocess # call outside shell commands
from datetime import datetime,time,date #to get current time and date
import argparse #handle command line interface
from termcolor import colored #set colored text
from astral import * # get sun times according to date
import json # JSON file support


#RIGHT NOW THIS IS SIMPLY A PYTHON SCRIPT - LATER ON - CONVERT TO CLASS!

#setup command line argument parsing
parser = argparse.ArgumentParser(description='Get user response for timelapse settings')
parser.add_argument("--set",action="store_true",required=False,help='To get settings from the user or automatically from config file.')
args = parser.parse_args()


#create camera object instance
print colored(" ____ ___                _                          __     ___   ___",'yellow')
print colored("""|  _ \_ _|_ __ ___   ___| |    __ _ _ __  ___  ___  \ \   / / | / _ \"""",'yellow')
print colored("""| |_) | || '_ ` _ \ / _ \ |   / _` | '_ \/ __|/ _ \  \ \ / /| || | | |""",'white')
print colored("|  __/| || | | | | |  __/ |__| (_| | |_) \__ \  __/   \ V / | || |_| |",'red')
print colored("|_|  |___|_| |_| |_|\___|_____\__,_| .__/|___/\___|    \_/  |_(_)___/",'red')
print colored("                                   |_|					",'red')

#verbose init message to let user know how the script operates
print ("------------------------------------------ Starting Script ------------------------------")
print("Note: you must register the Gdrive script with google before starting your version of the PImeLapse")
print colored("Starting TimeLapse script...",'cyan')
print colored("Config. file for PhotoTimer can be found in config_pt",'green')
print colored("Running TimeLapse script according to parameters given, photos will be uploaded to Gdrive",'white')
print colored("If network connection fails, the photos will be backed-up offline until connection restore",'white')
print colored("Once restored - files will be synced and then deleted again",'white')
print colored("------------------------------------------------------------------------------------------",'cyan')
print colored("Next version will use PyDrive instead of subproecss calling gdrive",'red')


#get current dawn and sunset times from Astral
#using Astral to get dawn and sunset times - in order to use them as time boundries for time lapse

def getSettings():
	freq = int(input("How often would you like to take a picture (time in sec.) \n"))
	timeStamp = raw_input("Would you like to add a time stamp to the images? \n")
	lengthShots = int(input("How long would you like to continously take shots? (negative values will mean you will have to manually shut down \n"))
	return freq,timeStamp,lengthShots;

def loadJSONsettings():
	configFile = open('config_pl.json')
	configDict = json.load(configFile)
	configFile.close()
	return configDict;


#get user settings (add file settings loading later on)
#to get user settings the user must add a flag to the command line instruction (the usage of input is annoying)
#a = raw_input("Would you like to type in your settings or use the config.txt file? press Y / N for config file")

if args.set:
	settings = getSettings()
else:
	print('using automated settings...\n')
	settings = loadJSONsettings()

def getTimes():
	astralObj = Astral()
	location = astralObj['Jerusalem']
	d = datetime.today()

	#print('Information for %s' % location.name)
	#        Information for London
	#timezone = location.timezone
	#print('Timezone: %s' % timezone)
	#        Timezone: Europe/London
	sun = location.sun(local=True, date=d)
	#print('Dawn:    %s' % str(sun['dawn']))
	#       Dawn:    2009-04-22 05:12:56+01:00
	#sunset = location.sunset(local=True,date=d)
	#print('Sunset:	%s' % str(sun['sunset']))

	return sun;

print colored("Commencing Timelapse, Please make sure the camera is well positioned...",'cyan')

#set up camera object instance
print(settings)
camera = PiCamera(resolution=(2592,1944))

def wait():
# Calculate the delay to the start of the next hour
	next_hour = (datetime.now() + timedelta(hour=1)).replace(
	minute=0, second=0, microsecond=0)
	delay = (next_hour - datetime.now()).seconds
	sleep(delay)
	return;

def isValidTime(sun):
	tmin = datetime.time(sun['dawn'])
	tmax = datetime.time(sun['sunset'])
	if(datetime.time(datetime.now()) > tmin and datetime.time(datetime.now()) < tmax ):
		return True
	else:
		return False


def capture(settings):
	sun = getTimes()
	#location = a['jerusalem']
	#sun = location.sun(local=True, date=datetime.today())
	i = 1
	while(isValidTime(sun)):
		filename = camera.capture('/tmp/img' + str(i) + '.jpg',format='jpeg',quality=int(settings["imageSettings"]["quality"]))
		#Should we capture now ?
		if(isValidTime(sun)):
			print('Captured %s' % filename)
			i+=1
			subprocess.call('./gdrive-linux-rpi sync upload /tmp/ 0BxITvHmu2Y4FMEtpSFRER05rbHc',shell=True)
			subprocess.call('rm /tmp/*.jpg', shell=True)
		else:
			wait() #calculate how long we should wait until starting the process over, if time exceeds the required TL time - exit

#### ACTUAL TIME LAPSE ####

capture(settings)
