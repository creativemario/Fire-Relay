from picozero import DigitalOutputDevice, Button, LED, pico_led
from time import sleep_ms as sleep
from random import randint

# Setup fire relay (RELAY 1) on GPIO 18 (Connect fire to NO and 240v to COM on RELAY 1).
fire = DigitalOutputDevice(18)
# Turn off the fire
fire.off()

# global control for fire enable
I_CAN_HAS_FIRE = False

# global fire duration constraints
MIN_FIRE_DURATION_MS = 1000
MAX_FIRE_DURATION_MS = 3000

# global lockout duration constraints
MIN_LOCKOUT_DURATION_MS = 5000
MAX_LOCKOUT_DURATION_MS = 10000

# setup the LED on GPIO 1.
led = LED(1)
led.off()

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
        pico_led.off()
        LED_BLINKING = False
        I_CAN_HAS_FIRE = False
        print("flame on")
        fire.on()
        fireduration = randint(MIN_FIRE_DURATION_MS, MAX_FIRE_DURATION_MS)
        print("flaming for", fireduration, "ms")
        sleep(fireduration)
        print("flame off")
        fire.off()


# Do the loop
while(True):
    # Blink LED if lockout disabled, and not already blinking
    if(I_CAN_HAS_FIRE and not LED_BLINKING):
        led.pulse()
        pico_led.blink()
        LED_BLINKING = True
    
    # if the button is being pressed and you are allowed to, do the fire
    if(I_CAN_HAS_FIRE and button.is_pressed):
        check_and_trigger_fire()
    
    # handle lockout
    if(not I_CAN_HAS_FIRE):
        lockoutduration = randint(MIN_LOCKOUT_DURATION_MS, MAX_LOCKOUT_DURATION_MS)
        print("lockout for", lockoutduration, "ms")
        sleep(lockoutduration)
        print("enabling fire")
        I_CAN_HAS_FIRE = True