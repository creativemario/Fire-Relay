from picozero import DigitalOutputDevice, Button, DigitalLED
from time import sleep_ms as sleep

# Setup fire relay (1) on GPIO 18 (Connect fire to NO and 240v to COM).
fire = DigitalOutputDevice(18)
# Turn off the fire
fire.off()

# global control for fire enable
I_CAN_HAS_FIRE = False

# global fire duration
FIRE_DURATION_MS = 3000
# global lockout duration
LOCKOUT_DURATION_MS = 10000

# setup the LED on GPIO 19 (this is a relay pin for testing, use a real LED on a different pin IRL).
led = DigitalLED(19)

# global control for tracking LED state
LED_BLINKING = False

# Setup the button on GPIO 15
button = Button(15)

# method for handling button press
def check_and_trigger_fire():
    global I_CAN_HAS_FIRE
    global LED_BLINKING
    if I_CAN_HAS_FIRE:
        led.off()
        LED_BLINKING = False
        I_CAN_HAS_FIRE = False
        print("flame on")
        fire.on()
        print("waiting", FIRE_DURATION_MS, "ms")
        sleep(FIRE_DURATION_MS)
        print("flame off")
        fire.off()


# Do the loop
while(True):
    # Blink LED if lockout disabled, and not already blinking
    if(I_CAN_HAS_FIRE and not LED_BLINKING):
        led.blink()
        LED_BLINKING = True
    
    # if the button is being pressed and you are allowed to, do the fire
    if(I_CAN_HAS_FIRE and button.is_pressed):
        check_and_trigger_fire()
    
    # handle lockout
    if(not I_CAN_HAS_FIRE):
        print("lockout for", LOCKOUT_DURATION_MS, "ms")
        sleep(LOCKOUT_DURATION_MS)
        print("enabling fire")
        I_CAN_HAS_FIRE = True