# Motorbike security device that detects motion and sends warning messages to owner
# Author: Peter Bassett

import time
import sys
import smtplib
import socket
import threading

# Import the ADXL345 module.
import Adafruit_ADXL345

#Thread used to communicate with google home via Node-red using UDP messages
def ga_commands():

    global kill, alarm_switch

    UDP_IP = "0.0.0.0"
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock2.bind((UDP_IP, 5005))
    sock2.settimeout(1)

    while(kill):
        try:
            data, addr = sock2.recvfrom(1024)
        except:
            continue
        if(data == "Sensor Armed"):
            alarm_switch = True
        if(data == "Sensor Disarmed"):
            alarm_switch = False

#Thread used to kill program using standard input
def kill_thread():
    global kill

    raw_input("Hit enter to kill process\n")
    kill = False



def main():
        
    # Create an ADXL345 instance.
    accel = Adafruit_ADXL345.ADXL345()
    
    #Set up SMTP email
    smtpUser = '[insert email address]'
    smtpPass = '[password]'

    toAddr = '[insert email address to send to]'

    subject = 'Someone is moving your motorbike!'
    header = 'To: ' + toAddr + '\n' + 'From: ' + smtpUser + '\n' + 'Subject: ' +subject

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo

    s.login(smtpUser, smtpPass)
    
    #Set up UDP socket for sending messages to Node-red for google home integration
    UDP_IP = "0.0.0.0"
    UDP_PORT = 5000
    Message = "Motorbike movement detected. Alarm active"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    global kill, alarm_switch
    kill = True #To terminate program
    alarm_switch = True #To arm and disarm device

    #Start up threads
    t1 = threading.Thread(target = ga_commands)
    t1.start()

    t2 = threading.Thread(target = kill_thread)
    t2.start()
    
    #Initialise variables   
    x, y, z = accel.read()
    count = 0
              
    while(kill):
        x_, y_, z_ = accel.read() #Update parameters

        if(alarm_switch):
            #If a movement of more than 30 degrees is detected for 5 seconds
            #Perform immobilsing routine
            if (abs(x-x_) > 30 or abs(y-y_) > 30 or abs(z-z_) > 30):
                count = count +1
                if (count > 5):
                    body = 'Motorbike movement detected'
                    s.sendmail(smtpUser, toAddr, header +'\n' + body) #Send emali
                    sock.sendto(Message, (UDP_IP, UDP_PORT)) #Broadcast over google home
                    print('Sending Message')
                    x, y, z = accel.read()
                    count = 0
            else:
                count = 0
        
        # Wait half a second and repeat.
        time.sleep(0.5)

    s.quit()

if (__name__ == "__main__"):
    main()
