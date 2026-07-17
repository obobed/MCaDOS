from main import PatternDetector
import time

p = PatternDetector(on_pattern=print)
p.press()
p.release()

p.press()
p.release()

p.press()
p.release()


time.sleep(0.5)
p.check_timeout()