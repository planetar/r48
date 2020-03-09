
# Your code goes below this line

from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
import json

@rule("tgBot01_newMsg", description="handle new msg", tags=["telegram"])
@when("Item lastMsg_bot1 received update")
def tgBot01_newMsg(event):
    msg=ir.getItem("lastMsg_bot1").state.toString()
    tgBot01_newMsg.log.info(msg.encode('utf-8'))
    lCharCodes=[]
    for c in msg:
        lCharCodes.append(ord(c))
    tgBot01_newMsg.log.info(lCharCodes)
