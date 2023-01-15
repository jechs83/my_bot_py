from decouple import config
from bot import *


chat = config("EXCELSIOR_CHAT_TOKEN")
bot_token = config("TOKEN_PICARD")
db1 = "excelsior1"
db2 = "excelsior2"
TOKEN = "5982396174:AAHNQb6hEGis5C_vsgY6v9b6w3Xej-AcTZU"
super_bot2(TOKEN, bot_token ,chat, db1,db2)

