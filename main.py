from gpiozero import DigitalInputDevice
import requests
import datetime
import time

POLL_RATE = 1  # 1 seconds
TIMEOUT = 30  # 30 seconds
GPIO_PIN = 3
MESSAGE = "Achtung: Erdbeeren leer!"
LAST_STATE = False
TOPIC = "checktec"

def send_msg():
    """ Sends a message to the topic """
    requests.post(f"https://ntfy.sh/{TOPIC}", data=MESSAGE.encode(encoding='utf-8'))

if __name__ == '__main__':
    device = DigitalInputDevice(GPIO_PIN, active_state=True)
    while True:
        if device.is_active:
            # Currently something inserted
            if not LAST_STATE:
                # Was not inserted before
                print(f"Insertion detected @{datetime.now()}")
            # Pass other option (as it was already True before)
            LAST_STATE = True
        else:
            # Currently nothing inserted
            if LAST_STATE:
                print(f"Removal detected @{datetime.now()}")
                # Awaiting the timeout and checking again
                device.wait_for_active(TIMEOUT)
                if not device.is_active:
                    print(f"Sending message as product has not been returned @{datetime.now()}")
                    send_msg()
                else:
                    print(f"Product has been returned @{datetime.now()}")
            LAST_STATE = False
        time.sleep(POLL_RATE)
