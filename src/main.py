from picozero import DigitalOutputDevice, Button, DigitalLED
from time import sleep_ms as sleep

# Setup fire relay (1) on GPIO 18 (Connect fire to NO and 240v to COM).
fire = DigitalOutputDevice(18)
# Turn off the fire
fire.off()

# global control for fire enable
icanhasfire = False

# global fire duration
fire_duration_ms = 3000
# global lockout duration
lockout_duration_ms = 10000

# setup the LED on GPIO 19 (this is a relay pin for testing, use a real LED on a different pin IRL).
led = DigitalLED(19)

# global control for tracking LED state
led_blinking = False

# Setup the button on GPIO 15
button = Button(15)

# method for handling button press
def checkandtriggerfire():
    global icanhasfire
    global led_blinking
    if icanhasfire:
        led.off()
        led_blinking = False
        icanhasfire = False
        print("flame on")
        fire.on()
        print("waiting", fire_duration_ms, "ms")
        sleep(fire_duration_ms)
        print("flame off")
        fire.off()


# Do the loop
while(True):
    # Blink LED if lockout disabled, and not already blinking
    if(icanhasfire and not led_blinking):
        led.blink()
        led_blinking = True
    
    # if the button is being pressed and you are allowed to, do the fire
    if(icanhasfire and button.is_pressed):
        checkandtriggerfire()
    
    # handle lockout
    if(not icanhasfire):
        print("lockout for", lockout_duration_ms, "ms")
        sleep(lockout_duration_ms)
        print("enabling fire")
        icanhasfire = True