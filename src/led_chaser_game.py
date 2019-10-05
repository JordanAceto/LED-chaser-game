
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

from Timer import Timer

from LED_Strip import LED_Strip

from Button import Button

SAMPLE_PERIOD = 0.3 # sample period in seconds, controls how fast the game starts out

LED_PINS = [26, 21, 20, 16, 12]

BUTTON_PIN = 13

STARTING_NUM_LIVES = 3

def cleanup():
    for pin in LED_PINS:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()   

def main():
    
    led_timer = Timer(SAMPLE_PERIOD)
    led_strip = LED_Strip(LED_PINS)
    button = Button(BUTTON_PIN)

    num_lives = STARTING_NUM_LIVES
    num_points = 0

    while(True):
        
        if (led_timer.outatime()):
            led_strip.tick()

        if (button.is_clicked()):
            if (led_strip.is_in_the_middle()):
                print("hit")
                led_strip.do_victory_blink()
                num_points += 1
            else:
                print("miss")
                num_lives -= 1

            led_timer.speed_up()
        
        if (num_lives == 0):
            led_strip.do_victory_blink()
            led_strip.show_binary(num_points)
            break
    
    print("You got", num_points, "points!")
    wait = input("press enter to quit")

if __name__ == '__main__':

    try:
        main()
        cleanup()
    except KeyboardInterrupt:
        cleanup()