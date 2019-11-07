from raven.watchdog import Watchdog, TimeoutError
import time
import pytest

def test_watchdog_no_start():
	w = Watchdog(0.1)
	time.sleep(0.2)

def test_watchdog_reset():
	w = Watchdog(0.3)
	w.start()
	time.sleep(0.2)
	w.reset()
	time.sleep(0.2)
	w.stop()

def test_watchdog_stop():
	w = Watchdog(0.2)
	w.start()
	time.sleep(0.1)
	w.stop()
	time.sleep(0.2)

def test_watchdog_timeout():
	w = Watchdog(0.1)
	w.start()
	with pytest.raises(TimeoutError):
		time.sleep(0.2)
