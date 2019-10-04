
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

import time

SAMPLE_PERIOD = 0.5 # sample period in seconds

LED_PINS = [26, 21, 20, 16, 12]

BUTTON_PIN = 13

class Timer():

    def __init__(self, sample_period):
        '''
        set up the initial sample period and last tick
        '''
        self.sample_period = sample_period
        self.last_tick = time.time()
    
    def outatime(self):
        '''
        return True if the timer has expired, else False
        '''
        self.elapsed_time = time.time() - self.last_tick

        if (self.elapsed_time >= self.sample_period):
            self.last_tick = time.time()
            return True

        return False

    def speed_up(self):
        self.sample_period *= 0.75

    def slow_down(self):
        self.sample_period *= 1.25

class Direction():
    LEFT = 1
    RIGHT = -1

def opposite(direction):
    if (direction == Direction.RIGHT):
        return Direction.LEFT
    else:
        return Direction.RIGHT

class LED_Strip():
    def __init__(self, led_pins):
        self.led_pins = led_pins
        
        for pin in self.led_pins:
            GPIO.setup(pin, GPIO.OUT)

        self.current_led_index = len(self.led_pins) // 2
        self.current_direction = Direction.RIGHT

    def tick(self):
        '''
        executes one tick of the led strip
        '''
        # print("current led:", self.current_led_index)
        # turn the old LED off
        GPIO.output(self.led_pins[self.current_led_index], GPIO.LOW)

        # swap directions if you hit one of the ends
        if (self.hit_one_of_the_ends()):
            self.current_direction = opposite(self.current_direction)

        # move the current led to its new spot
        self.current_led_index += self.current_direction

        # turn the new LED on
        GPIO.output(self.led_pins[self.current_led_index], GPIO.HIGH)

    def is_in_the_middle(self):
        return self.current_led_index == (len(self.led_pins) // 2)

    def turn_all_on(self):
        for led_pin in self.led_pins:
            GPIO.output(led_pin, GPIO.HIGH)
    
    def turn_all_off(self):
        for led_pin in self.led_pins:
            GPIO.output(led_pin, GPIO.LOW)

    def do_victory_blink(self):
        for i in range(7):
            self.turn_all_on()
            time.sleep(0.15)
            self.turn_all_off()
            time.sleep(0.15)

    def hit_one_of_the_ends(self):
        return self.current_led_index == 0 or self.current_led_index == len(self.led_pins) - 1

class Button():
    def __init__(self, pin_num):
        self.pin_num = pin_num
        GPIO.setup(self.pin_num, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.last_state = True

    def is_clicked(self):
        '''
        if the current state is low and the last state was high, set the
        last state to low and return True
        '''
        # reverse logic, False means the button is pressed
        if self.last_state == True and GPIO.input(self.pin_num) == False:
            self.last_state = False
            return True

        self.last_state = GPIO.input(self.pin_num)
        return False

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