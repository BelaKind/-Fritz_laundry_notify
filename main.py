import os
import time
import threading

from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation
from fritzconnection.lib.fritzhosts import FritzHosts
from dotenv import load_dotenv


load_dotenv()
FRITZ_USERNAME = os.getenv("FRITZ_USERNAME")
FRITZ_PASSWORD = os.getenv("FRITZ_PASSWORD")
FRITZ_BOX_IP = os.getenv("FRITZ_BOX_IP")
DEVICE_AIN = os.getenv("DEVICE_AIN")

fc = FritzConnection(address=FRITZ_BOX_IP, user=FRITZ_USERNAME, password=FRITZ_PASSWORD)
fh = FritzHosts(fc)
fha = FritzHomeAutomation(fc)


automation_devices = fha.get_device_information_list()
print_parameters = ['NewDeviceName', 'NewAIN', 'NewDeviceId', 'NewPresent']
device_ain = DEVICE_AIN

def scan_for_smarthome_devices():
    for device in automation_devices:
        for parameter in print_parameters:
            clean_parameter = parameter.replace("New", "")
            print(f"{clean_parameter}:  {device[parameter]}")
        print()

def return_power(ain):
    device_information = fha.get_device_information_by_identifier(ain)
    return device_information['NewMultimeterPower']/100        

def process_commands(userInput):
    if userInput.lower() == "write_file":
        write_file()
    else: 
        return


#---------------commands------------------#


def write_file():
    print("writing file measurments.md ...")
    with open("measurements.md", "a", encoding="utf-8") as file:
        file.write("----------------------------\n\n")
    for nr in range(0,10):
        data = return_power(DEVICE_AIN)
        with open("measurements.md", "a", encoding="utf-8") as file:
                time.sleep(20)
                file.write(f"value {nr}: -- {data} watt\n")
                



def main_program():
   # print(scan_for_devices())
    while True:
        userInput = input("enter command (e.g write_file): ")
        process_commands(userInput)
        


if __name__ == '__main__':
  main_program()