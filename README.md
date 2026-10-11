# Fritz_laundry_notify

This Project connects to your !FritzBox and reads the measured power of a selected Fritz! dect outlet. By analysing the measured power it checks if the washing machine is finished.

## Screenshots

Startup of the main.py script
![alt text](assets/web_dashboard.png)

Web dashboard (work in progress)
![alt text](assets/commando_line.png)


## Description

This project sends you a notification directly to your WhatsApp when your washing machine has finished washing. 
By checking the measured power at a smart outlet von FRITZ! it detects the start and also when the washing cycle is finished. Using CallMeBot you will recieve a message so you do not miss to take out your laundry.

## Prerequisites

To run the script you need following things set up:

### Python Libraries
- fritzconnection
- dotenv
- requests
- flask

### Other services
- a CallMeBot bot set up in your Messanger (check the documentation here: https://www.callmebot.com/?ae_global_templates=setup-whatsapp)
- a FRITZ!box user (I would recommend to create a new user with limited rights)

### .env file
create an .env file in your project folder and insert your variables:

```ini
FRITZ_USERNAME=username
FRITZ_PASSWORD=password
FRITZ_BOX_IP=fritz_box_ip
DEVICE_AIN=ain
CALLMEBOT_APIKEY=apikey
PHONE_NUMBER=phone_number
```

## Installtion & start

1. create a project folder and execute this command in this folder: git clone https://github.com/BelaKind/-Fritz_laundry_notify.git
2. On some systems it is necessary to install all libraries in a virtual environment (check it out here: https://docs.python.org/3/library/venv.html)
3. activate it by using 'project_folder/.venv/bin/activate'
4. install all libraries by using `pip3 install fritzconnection python-dotenv requests flask`
