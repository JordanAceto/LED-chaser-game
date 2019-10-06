
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

from Timer import Timer

from LED_Strip import LED_Strip

from Button import Button

from Constants import STARTING_SAMPLE_PERIOD, STARTING_NUM_LIVES, LED_PINS, BUTTON_PIN

class Game():

    def __init__(self, starting_sample_period, starting_num_lives, timer, led_strip, button):
        self.starting_num_lives = starting_num_lives
        self.num_lives = starting_num_lives
        self.num_points = 0

        self.starting_sample_period = starting_sample_period

        self.timer = timer
        self.led_strip = led_strip
        self.button = button

    def reset_game(self):
        self.led_strip.turn_all_off()
        self.num_lives = self.starting_num_lives
        self.num_points = 0
        self.timer.sample_period = self.starting_sample_period

    
    def play_round(self):

        self.reset_game()

        playing_this_round = True

        while(playing_this_round):
        
            if (self.timer.outatime()):
                self.led_strip.tick()

            if (self.button.is_clicked()):
                if (self.led_strip.is_in_the_middle()):
                    print("hit")
                    self.led_strip.blink_all(7, 0.12)
                    self.num_points += 1
                else:
                    print("miss")
                    self.num_lives -= 1

                self.timer.speed_up()
            
            if (self.num_lives == 0):
                self.led_strip.do_special_pattern(10, 0.1)
                self.led_strip.show_binary(self.num_points)

                print("You got", self.num_points, "points!")

                playing_this_round = False

def cleanup():
    for pin in LED_PINS:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()  

if __name__ == '__main__':

    try:
        button = Button(BUTTON_PIN)
        timer = Timer(STARTING_SAMPLE_PERIOD)
        led_strip = LED_Strip(LED_PINS)

        game = Game(STARTING_SAMPLE_PERIOD, STARTING_NUM_LIVES, timer, led_strip, button)

        playing_the_game = True
        
        while (playing_the_game):
            
            game.play_round()

            waiting_for_button_press_before_starting_new_round = True

            while (waiting_for_button_press_before_starting_new_round):
                if button.is_clicked():
                    waiting_for_button_press_before_starting_new_round = False

        cleanup()
    except KeyboardInterrupt:
        cleanup()