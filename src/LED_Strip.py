
import RPi.GPIO as GPIO

from Direction import Direction, opposite

from int_to_list_of_binary_digits import int_to_list_of_binary_digits

import time

class LED_Strip():
    def __init__(self, led_pins):
        self.led_pins = led_pins
        
        for pin in self.led_pins:
            GPIO.setup(pin, GPIO.OUT)

        self.length = len(self.led_pins)
        self.current_led_index = self.length // 2
        self.middle_index = self.current_led_index
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
        return self.current_led_index == self.middle_index

    def turn_all_on(self):
        for led_pin in self.led_pins:
            GPIO.output(led_pin, GPIO.HIGH)
    
    def turn_all_off(self):
        for led_pin in self.led_pins:
            GPIO.output(led_pin, GPIO.LOW)

    def blink_all(self, num_blinks, delay):
        
        self.turn_all_off()

        for i in range(num_blinks):
            self.turn_all_on()
            time.sleep(delay)
            self.turn_all_off()
            time.sleep(delay)

    def do_special_pattern(self, num_times, delay):
        
        self.turn_all_off()

        for i in range(num_times):
            for j in range(self.middle_index, self.length):
                GPIO.output(self.led_pins[j], GPIO.HIGH)
                GPIO.output(self.led_pins[self.length - j - 1], GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(self.led_pins[j], GPIO.LOW)
                GPIO.output(self.led_pins[self.length - j - 1], GPIO.LOW)


    def hit_one_of_the_ends(self):
        return self.current_led_index == 0 or self.current_led_index == self.length - 1

    def show_binary(self, integer):
       
        self.turn_all_off()

        list_of_binary_digits = int_to_list_of_binary_digits(integer)

        for i in range(len(list_of_binary_digits)):
            if (list_of_binary_digits[i] == 1 and i < self.length):
                # go "backwards" so it shows the binary digits left-to-right
                GPIO.output(self.led_pins[self.length - 1 - i], GPIO.HIGH)
