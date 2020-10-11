import logging
import sys

import mymodule
import mymodule.sub

FORMAT='%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging.basicConfig(format=FORMAT, level=logging.WARNING, stream=sys.stderr)

log = logging.getLogger(__name__)

mine = mymodule.Thing()
my_sub = mymodule.sub.Thing()

log.info("Loaded all required modules")

mine.dangerous()
my_sub.do_work()
my_sub.safer()
