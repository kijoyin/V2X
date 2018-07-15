import logging
import logging.handlers
import argparse
import sys
import os
import time
import RPi.GPIO as gpio
from bluetooth.bluez import *


class LoggerHelper(object):
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level

    def write(self, message):
        if message.rstrip() != "":
            self.logger.log(self.level, message.rstrip())


def setup_logging():
    # Default logging settings
    LOG_FILE = "/var/log/raspibtsrv.log"
    LOG_LEVEL = logging.INFO

    # Define and parse command line arguments
    argp = argparse.ArgumentParser(description="Raspberry PI Bluetooth Server")
    argp.add_argument("-l", "--log", help="log (default '" + LOG_FILE + "')")

    # Grab the log file from arguments
    args = argp.parse_args()
    if args.log:
        LOG_FILE = args.log

    # Setup the logger
    logger = logging.getLogger(__name__)
    # Set the log level
    logger.setLevel(LOG_LEVEL)
    # Make a rolling event log that resets at midnight and backs-up every 3 days
    handler = logging.handlers.TimedRotatingFileHandler(LOG_FILE,
        when="midnight",
        backupCount=3)

    # Log messages should include time stamp and log level
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    # Attach the formatter to the handler
    handler.setFormatter(formatter)
    # Attach the handler to the logger
    logger.addHandler(handler)

    # Replace stdout with logging to file at INFO level
    sys.stdout = LoggerHelper(logger, logging.INFO)
    # Replace stderr with logging to file at ERROR level
    sys.stderr = LoggerHelper(logger, logging.ERROR)


# Main loop
def main():
    # Setup logging
    #setup_logging()

    # We need to wait until Bluetooth init is done
    time.sleep(10)

    # Make device visible
    os.system("hciconfig hci0 piscan")

    # Create a new server socket using RFCOMM protocol
    server_sock = BluetoothSocket(RFCOMM)
    # Bind to any port
    server_sock.bind(("", PORT_ANY))
    # Start listening
    server_sock.listen(1)

    # Get the port the server socket is listening
    port = server_sock.getsockname()[1]

    # The service UUID to advertise
    uuid = "7be1fcb3-5776-42fb-91fd-2ee7b5bbb86d"

    # Start advertising the service
    advertise_service(server_sock, "RaspiBtSrv",
                       service_id=uuid,
                       service_classes=[uuid, SERIAL_PORT_CLASS],
                       profiles=[SERIAL_PORT_PROFILE])

    # These are the operations the service supports
    # Feel free to add more
    operations = ["Start", "ping", "example"]

    init()

    # Main Bluetooth server loop
    while True:

        print("Waiting for connection on RFCOMM channel %d" % port)
        
        try:
            client_sock = None

            # This will block until we get a new connection
            client_sock, client_info = server_sock.accept()
            print("Accepted connection from ", client_info)

            # Read the data sent by the client
            data = client_sock.recv(1024)
            if len(data) == 0:
                break

            print("Received [%s]" % data)
            data = data.decode("utf-8") 
            # Handle the request
            if data == "getop":
                response = "op:%s" % ",".join(operations)
            elif data == 'Start':
                response = "msg:Starting the car"
                start()
            elif data == 'Stop':
                response = "msg:Stopping the car"
                stop()
            elif data == 'Left':
                response = "msg:Turning left"
            elif data == 'Right':
                response = "msg:Turning right"
            elif data == 'Accelerate':
                response = "msg:Increasing speed"
                accelerate(True)
            elif data == 'Decelerate':
                response = "msg:Decreasing speed"
                accelerate(False)
            # Insert more here
            else:
                response = data

            client_sock.send(response)
            print("Sent back [%s]" % response)

        except IOError:
            pass

        except KeyboardInterrupt:

            gpio.cleanup()
            
            if client_sock is not None:
                client_sock.close()

            server_sock.close()
	    

            print("Server going down")
            break



speed = 50
PMWPIN = 18
LEFTForward = 21
LEFTBackward = 20
RIGHTForward = 26
RIGHTBackward = 19
gpio.setmode(gpio.BCM)
gpio.setup(PMWPIN, gpio.OUT)
pwm = gpio.PWM(PMWPIN, speed)

def init():
    gpio.setup(LEFTForward, gpio.OUT)
    gpio.setup(LEFTBackward, gpio.OUT)
    gpio.setup(RIGHTForward, gpio.OUT)
    gpio.setup(RIGHTBackward, gpio.OUT)
    gpio.output(LEFTForward,gpio.LOW)
    gpio.output(LEFTBackward,gpio.LOW)
    gpio.output(RIGHTForward,gpio.LOW)
    gpio.output(RIGHTBackward,gpio.LOW)
    
def start():
    gpio.output(LEFTBackward,gpio.LOW)
    gpio.output(LEFTForward, gpio.HIGH)
    gpio.output(RIGHTBackward,gpio.LOW)
    gpio.output(RIGHTForward, gpio.HIGH)
    pwm.start(1)
    speed = 50
    pwm.ChangeDutyCycle(speed)
    
def stop():
    speed =50
    pwm.ChangeDutyCycle(speed)
    pwm.stop()
    gpio.output(LEFTForward, gpio.LOW)
    gpio.output(RIGHTForward, gpio.LOW)

def accelerate(acc):
    global speed
    if(acc and speed < 90):
        speed = speed + 5
        pwm.ChangeDutyCycle(speed)
        print("faster")
    elif(acc != True and speed > 50 ):
        speed = speed - 5
        pwm.ChangeDutyCycle(speed)
        print("slower")
    print(speed)    

main()
