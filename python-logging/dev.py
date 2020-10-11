import logging
import sys

import mymodule
import mymodule.sub

FORMAT='%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging.basicConfig(format=FORMAT, level=logging.DEBUG, stream=sys.stderr)

log = logging.getLogger(__name__)

mine = mymodule.Thing()
my_sub = mymodule.sub.Thing()

log.info("Loaded all required modules")

my_sub.safer()
