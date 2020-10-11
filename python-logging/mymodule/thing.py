import logging

log = logging.getLogger(__name__)

class Thing:

    def __init__(self):
        log.debug("Loading class Thing...")

    def do_work(self):
        log.debug("About to do my work...")

    def dangerous(self):
        log.warning("This is a dangerous action that is being performed")
