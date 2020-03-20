
# Your code goes below this line

from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
from org.joda.time import DateTime, Interval
from core.date import seconds_between, human_readable_seconds 
from core.actions import PersistenceExtensions

import json


def blogg(msg):
    actions.get("telegram", "telegram:telegramBot:d50985af").sendTelegram(u"{}".format(msg))



@rule("tgBot01_newMsg", description="handle new msg", tags=["telegram"])
@when("Item lastMsg_bot1 received update")
def tgBot01_newMsg(event):
    msg=ir.getItem("lastMsg_bot1").state.toString()
    tgBot01_newMsg.log.info(msg.encode('utf-8'))
    lCharCodes=[]
    for c in msg:
        lCharCodes.append(ord(c))
    tgBot01_newMsg.log.info(lCharCodes)
    smiley= unichr(127788)  # nebelFee
    smiley= unichr(128168)  # dichter Nebel
    smiley= unichr(127786)  # Tornado

    lEmoji=[unichr(127788),unichr(128168),unichr(127786)]
    blogg(smiley)
    return




    #tgBot01_newMsg.log.info(Telegram)
    #telegramAction = Telegram.getActions("telegram","telegram:telegramBot:d50985af")
    #telegramAction.sendTelegram("hallo Welt")
    #Telegram.sendTelegram("telegramBot:d50985af", "Test")
    # kueche2Millis = (ir.getItem("pirLastTriggered_Kueche2").state as DateTimeType).zonedDateTime.toInstant.toEpochMilli
    #kueche2last = ir.getItem("pirLastTriggered_Kueche2").state
    #kueche2Instant= kueche2last.zonedDateTime.toInstant
    #kueche2Millis=kueche2last.getMillis()
    
    #item=ir.getItem("sensor_humidity_Kueche")
    last = PersistenceExtensions.previousState(ir.getItem("pirLastTriggered_Kueche2")).timestamp

    # only check this if no one is in the room
    lastTriggered = ir.getItem("pirLastTriggered_Kueche2").state
    timeBetween= seconds_between(lastTriggered, DateTime.now())
    timeBetween1= seconds_between(last, DateTime.now())

    if timeBetween < 5*60:
        #tgBot01_newMsg.log.info("only {}s since last movement here, no check".format(timeBetween))
        reportGram(u"only {}s  {}s since last movement here, no check".format(timeBetween, timeBetween1))
    else:
        #tgBot01_newMsg.log.info("already {}s since last movement here, will check".format(timeBetween))
        reportGram(u"already {}s {}s since last movement here, will check".format(timeBetween,timeBetween1))
        #avg2=sensor_humidity_Kueche.averageSince(now.minusMinutes(compareMinutes))
        avg1= PersistenceExtensions.averageSince(ir.getItem("sensor_humidity_Kueche"),DateTime.now().minusMinutes(5) )
        avg2= PersistenceExtensions.averageSince(ir.getItem("sensor_humidity_Kueche"),DateTime.now().minusMinutes(230) )
        reportGram(u"avg1 {} avg2 {} ".format(avg1,avg2))
    #time_interval = human_readable_seconds(seconds_between(PersistenceExtensions.previousState(item).timestamp, DateTime.now()))


    #actions.get("telegram", "telegram:telegramBot:d50985af").sendTelegram(u"Hällö Welt {}".format(str(timeBetween)))
    reportGram("last: {}".format(last)) 

