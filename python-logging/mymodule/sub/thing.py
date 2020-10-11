import logging

log = logging.getLogger(__name__)

class Thing:

    def __init__(self):
        log.debug("Loading class Thing...")

    def do_work(self):
        log.debug("About to do my work...")

    def safer(self):
        log.warn("A safer than dangerous action is being performed")
