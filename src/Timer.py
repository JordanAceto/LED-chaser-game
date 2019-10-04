
import time

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