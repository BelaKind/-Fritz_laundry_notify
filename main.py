import os
import time
import threading
import requests
from datetime import datetime

from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation
from fritzconnection.lib.fritzhosts import FritzHosts
from dotenv import load_dotenv


load_dotenv()
FRITZ_USERNAME = os.getenv("FRITZ_USERNAME")
FRITZ_PASSWORD = os.getenv("FRITZ_PASSWORD")
FRITZ_BOX_IP = os.getenv("FRITZ_BOX_IP")
DEVICE_AIN = os.getenv("DEVICE_AIN")
CALLMEBOT_APIKEY = os.getenv("CALLMEBOT_APIKEY")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")


#I would recommend to use an extra Fritz!box user with limited rights
fc = FritzConnection(address=FRITZ_BOX_IP, user=FRITZ_USERNAME, password=FRITZ_PASSWORD)
fh = FritzHosts(fc)
fha = FritzHomeAutomation(fc)


automation_devices = fha.get_device_information_list()
print_parameters = ['NewDeviceName', 'NewAIN', 'NewDeviceId', 'NewPresent']


writingFile = False
isWashing = False
startTime = None


    

def process_commands(userInput):
    if userInput.lower() == "write_file":
        threading.Thread(target=write_file, daemon=True).start()
    elif (userInput.lower() == "stop_writing"):
        global writingFile 
        writingFile = False
    elif (userInput.lower() == "print_devices"):
        scan_for_smarthome_devices()
    elif (userInput.lower() == "print_power"):
        print(f"{return_power(DEVICE_AIN)} watts")
    elif (userInput.lower() == "help"):
        print("ALL COMMANDS: \n write_file \n stop_writing \n print_devices \n print_power \n help")
    else: 
        return


def idle_measurements():
    global isWashing
    global startTime
    while True:
        if not isWashing:
                currentWatt = return_power(DEVICE_AIN)

                if currentWatt > 20:

                    if startTime is None:
                        #sets the start time
                        startTime = time.time()
                    alreadyActiveTime = time.time() - startTime
                    #If the power is high enough over some time the washine machine was started
                    #That prevents from errors
                    if alreadyActiveTime >= 300:                        
                        isWashing = True
                        startTime = None
                        print("\nThe washing machine is running")
                        threading.Thread(target=handle_washing, daemon=True).start()

                else:

                    if startTime is not None:
                        startTime = None  
                time.sleep(15)
        else:
            time.sleep(30)


def handle_washing():
    global isWashing
    while isWashing:
        currentWatt = return_power(DEVICE_AIN)
        if currentWatt < 5:
            isWashing = False
            print("\nThe washing machine is finished!")
            notify_user("The washing machine is finished! ✅") 
            return 
        time.sleep(20)

def notify_user(message):
    #I use CallMeBot here because I wanted to use Whatsapp
    #Maybe I will add other services here

    #The phone number is the number of your whatsapp account 
    #You get the api key when setting up CallMeBot
    encodedMessage = requests.utils.quote(message)
    url = f"https://api.callmebot.com/whatsapp.php?phone={PHONE_NUMBER}&text={encodedMessage}&apikey={CALLMEBOT_APIKEY}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            print("Message was sent successfully!")
        else:
            print(f"Failed to send. Statuscode: {response.status_code}")
    except Exception as e:
        print(f"Network error: {e}")


#---------------commands------------------#


def write_file():
    global writingFile
    writingFile = True
    nr = 0
    print("\nwriting file logfile.md ...")
    with open("logfile.md", "a", encoding="utf-8") as file:
        file.write("----------------------------\n\n")
    while writingFile:
        nr += 1
        data = return_power(DEVICE_AIN)
        now = datetime.now()
        with open("logfile.md", "a", encoding="utf-8") as file:
                file.write(f"{now.strftime('%H:%M:%S')} -> value {nr}: -- {data} watt\n")
        time.sleep(20)
    return print("\nprocess stopped")
                
def scan_for_smarthome_devices():
    for device in automation_devices:
        for parameter in print_parameters:
            clean_parameter = parameter.replace("New", "")
            print(f"{clean_parameter}:  {device[parameter]}")
        print()

def return_power(ain):
    device_information = fha.get_device_information_by_identifier(ain)
    return device_information['NewMultimeterPower']/100    


#------------------------------------------#



#-----------Main Function------------#

def main_program():
    global isWashing
    isWashing = False
    threading.Thread(target=idle_measurements, daemon=True).start()
    print("++++++FRITZ! Laundry notify++++++")
    print("enter your commands below (type help for a list of all commands)")
    while True:
        userInput = input("enter command (e.g write_file): ")
        process_commands(userInput)
        
#------------------------------------#

if __name__ == '__main__':
  main_program()