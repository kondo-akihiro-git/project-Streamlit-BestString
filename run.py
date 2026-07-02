# run.py
from model.init import init_database
from routing.routing import router

init_database()
router()