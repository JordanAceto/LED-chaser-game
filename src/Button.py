
import RPi.GPIO as GPIO

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