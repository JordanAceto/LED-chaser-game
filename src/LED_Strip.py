
import RPi.GPIO as GPIO

from Direction import Direction, opposite

from int_to_list_of_binary_digits import int_to_list_of_binary_digits

import time

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

    def show_binary(self, integer):
       
        self.turn_all_off()

        list_of_binary_digits = int_to_list_of_binary_digits(integer)

        for i in range(len(list_of_binary_digits)):
            if (list_of_binary_digits[i] == 1):
                # go "backwards" so it shows the binary digits left-to-right
                GPIO.output(self.led_pins[len(self.led_pins) - 1 - i], GPIO.HIGH)
