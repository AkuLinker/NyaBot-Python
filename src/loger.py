import logging
import sys

log = logging.getLogger(sys.argv[0])
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler1 = logging.FileHandler('NyaBot.log')
handler2 = logging.StreamHandler(stream=sys.stdout)
handler1.setFormatter(formatter)
handler2.setFormatter(formatter)
log.setLevel(logging.DEBUG)
log.addHandler(handler1)
log.addHandler(handler2)
