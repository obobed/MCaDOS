import time
import inspect
from pynput import keyboard
from actions import ACTIONS

# we need vars for thresholds
TAP_MAX = 0.35 # press and release combo before this time = a tap
TIMEOUT = 0.35 # silence longer than this = timeout and sequence is finished

class PatternDetector:
    def __init__(self, on_pattern, on_update=None) -> None: # on_pattern being the handler function
        self.on_pattern = on_pattern
        self.on_update = on_update
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
        if self.on_update:
            self.on_update(self.sequence)
    
    def check_timeout(self): # call every like 50ms from a loop or timer, basically checks if the sequence has timed out
        if self.sequence and self.last_event_time and not self.press_time:
            if time.monotonic() - self.last_event_time > TIMEOUT:
                self.on_pattern(self.sequence)
                self.sequence = ""
                self.last_event_time = None

def validate_config(config):
    errors = []

    trigger_name = config.get("trigger_key")
    if not trigger_name or not hasattr(keyboard.Key, trigger_name):
        errors.append(f"invalid trigger_key: {trigger_name!r}") # !r incase theres a space so yall can see it

    seen_patterns = set()
    for i, binding in enumerate(config.get("bindings", [])):
        pattern = binding.get("pattern")
        action_name = binding.get("action")

        if not pattern or any(c not in "TH" for c in pattern):
            if any(c.isspace() for c in pattern):
                errors.append(f"binding {i}: pattern contains whitespace: {pattern!r}")
            else:
                errors.append(f"binding {i}: invalid pattern: {pattern!r} (only T/H permitted)")
        
        if pattern in seen_patterns:
            errors.append(f"binding {i}: duplicate pattern {pattern!r}")
        seen_patterns.add(pattern)

        if action_name not in ACTIONS:
            errors.append(f"binding {i}: unknown action {action_name!r} (not in ACTIONS dict?)")
        
        else: # check args match function expectations
            func = ACTIONS[action_name]
            signature = inspect.signature(func)
            expected_args = set(signature.parameters.keys())
            provided_args = set(binding.get("args", {}).keys())
            unexpected = provided_args - expected_args
            if unexpected:
                errors.append(f"binding {i}: unexpected args {unexpected} for action {action_name}")

    if errors:
        raise ValueError("Config validation failed:\n" + "\n".join(f" - {e}" for e in errors))
