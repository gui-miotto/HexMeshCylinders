from datetime import datetime


class Printer():
    def __init__(self, verbose):
        self.verbose = verbose

    def __call__(self, text):
        if self.verbose:
            now = datetime.now()
            print(now.strftime("[%H:%M:%S]"), text)
