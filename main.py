import time

# we need vars for thresholds
TAP_MAX = 0.35 # press and release combo before this time = a tap
TIMEOUT = 0.35 # silence longer than this = timeout and sequence is finished

class PatternDetector:
    def __init__(self, on_pattern) -> None: # on_pattern being the handler function
        self.on_pattern = on_pattern 
        self.sequence = ""
        self.press_time = None
        self.last_event_time = None
        
    def press(self):
        if self.press_time is None: # otherwise os auto-repeats will keep triggering presses during a hold event
            self.press_time = time.monotonic()

    def release(self):
        if self.press_time is None:
            return # maybe some debug logging here?
        duration = time.monotonic() - self.press_time
        self.sequence += "H" if duration > TAP_MAX else "T" # h & t are hold and tap respectively
        self.last_event_time = time.monotonic()
        self.press_time = None
    
    def check_timeout(self): # call every like 50ms from a loop or timer, basically checks if the sequence has timed out
        if self.sequence and self.last_event_time and not self.press_time:
            if time.monotonic() - self.last_event_time > TIMEOUT:
                self.on_pattern(self.sequence)
                self.sequence = ""
                self.last_event_time = None