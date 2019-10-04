
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

from Timer import Timer

from LED_Strip import LED_Strip

from Button import Button

SAMPLE_PERIOD = 0.3 # sample period in seconds, controls how fast the game starts out

LED_PINS = [26, 21, 20, 16, 12]

BUTTON_PIN = 13

def cleanup():
    for pin in LED_PINS:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()   

def main():
    
    led_timer = Timer(SAMPLE_PERIOD)
    led_strip = LED_Strip(LED_PINS)
    button = Button(BUTTON_PIN)

    while(True):
        
        if (led_timer.outatime()):
            led_strip.tick()

        if (button.is_clicked()):
            if (led_strip.is_in_the_middle()):
                led_strip.do_victory_blink()
                print("you won!")
                # return? what happens?
            else:
                led_timer.speed_up()

if __name__ == '__main__':

    try:
        main()
        cleanup()
    except KeyboardInterrupt:
        cleanup()