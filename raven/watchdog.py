import signal


class TimeoutError(Exception):
    pass


class Watchdog:
    def __init__(self, timeout, handler=None):
        self.timeout = timeout
        self.started = False

        def signal_handler(signum, frame):
            self._stop()
            self.started = False
            if handler:
                handler()
            else:
                self.default_handler()

        self.handler = signal_handler

    def start(self):
        signal.signal(signal.SIGALRM, self.handler)
        signal.setitimer(signal.ITIMER_REAL, self.timeout)
        self.started = True

    def reset(self):
        if not self.started:
            raise RuntimeError("Watchdog timer not started")
        signal.setitimer(signal.ITIMER_REAL, self.timeout)

    def _stop(self):
        signal.setitimer(signal.ITIMER_REAL, 0)

    def stop(self):
        if not self.started:
            raise RuntimeError("Watchdog timer not started")
        self._stop()
        self.started = False

    def default_handler(self):
        raise TimeoutError()

    def __del__(self):
        self._stop()
