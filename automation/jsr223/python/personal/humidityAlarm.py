
from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
from org.joda.time import DateTime
from core.date import seconds_between, human_readable_seconds 
from core.actions import PersistenceExtensions

#import json

minTimeEmpty = 2 *60
longAvgMin = 120
#shortAvgMin = 3

lHumKueche=[]
lTriggerKueche = [8,13,20]
samplesKueche = 3
alertCount_Kueche = 0

lHumBad=[]
lTriggerBad = [8,13,20]
samplesBad = 4 
alertCount_Bad = 0

def blogg(msg):
    actions.get("telegram", "telegram:telegramBot:d50985af").sendTelegram(u"{}".format(msg))

def logg(msg):
    humidityCheck_kueche.log.info(u"{}".format(msg))



@rule("humidityCheck_kueche", description="check whether we have a hum spike up", tags=["humidity,alarm,kueche,telegram"])
@when("Item sensor_humidity_Kueche changed")
#@when("Item lastMsg_bot1 received update")

def humidityCheck_kueche(event):
    global alertCount_Kueche,lHumKueche
    # alle werden wie global behandelt aber nur alertCount_Kueche verlangt danach, deklariert zu werden.
    logg(u"Kueche: samplesKueche: {}  longAvgMin: {} minTimeEmpty: {} alertCount_Kueche: {}".format(samplesKueche,longAvgMin,minTimeEmpty,alertCount_Kueche))

    # only check this if no one is in the room
    last = PersistenceExtensions.previousState(ir.getItem("PirState_Kueche2")).timestamp
    timeEmpty = seconds_between(last, DateTime.now())

    if timeEmpty < minTimeEmpty:
        #logg(u"only {}s  since last movement here, no check".format(timeEmpty))
        pass
    else:

        #logg(u"already {}s since last movement here, will check".format(timeEmpty))

        avgLong  = PersistenceExtensions.averageSince(ir.getItem("sensor_humidity_Kueche"),DateTime.now().minusMinutes( longAvgMin ) ) 
        # etwas ulkige Typumwandlung        
        sAL = u"{}".format( avgLong ) 
        fAvgLong = float(sAL)

        currMeasurement=float(ir.getItem("sensor_humidity_Kueche").state.toString())
        lHumKueche.append(currMeasurement)
        # if (humKuecheList.size() >samplesKueche){humKuecheList.remove(0)}
        if len(lHumKueche)>samplesKueche:
            lHumKueche.pop(0)

        if avgLong == None:
            blogg(u"nothing to compare with  avgLong {} ".format(avgLong))
            # nothing to compare with...
            return

        # check if values increase stetig
        iter = 0
        sum = 0
        stetig=True
        for el in lHumKueche:
            sum += el
            if iter > 0:
                if lHumKueche[iter-1]>lHumKueche[iter]:
                    stetig=False
            iter+=1
        avgMeasured = sum/iter
        nextTrigger = lTriggerKueche[alertCount_Kueche]

        if avgMeasured > fAvgLong + nextTrigger and stetig:
            if alertCount_Kueche < len(lTriggerKueche)-1:
                alertCount_Kueche +=1
                lEmoji=[unichr(127788),unichr(128168),unichr(127786)]
                emoji=lEmoji[alertCount_Kueche]
                blogg(u"{} Wasserkessel auf dem Herd vergessen?   jsr-Alarm{}  ".format(emoji,alertCount_Kueche))
            #else:

        if not stetig:
            alertCount_Kueche=0
            lHumKueche = [currMeasurement]

        logg(u"Kueche: fAvgLong: {} avgMeasured {}  sum {} iter {} stetig {} nextTrigger {} lHumKueche:{}".format(fAvgLong,avgMeasured,sum,iter,stetig,nextTrigger,lHumKueche))

    #blogg(u"AlertCount_Kueche: {} ".format(alertCount_Kueche))





@rule("humidityCheck_bad", description="check whether we have a hum spike down", tags=["humidity,alarm,bad,telegram"])
@when("Item sensor_humidity_Bad changed")
@when("Item lastMsg_bot1 received update")

def humidityCheck_bad(event):
    global alertCount_Bad,lHumBad
    # alle werden wie global behandelt aber nur alertCount_Kueche verlangt danach, deklariert zu werden.
    logg(u"Bad: samplesBad: {} longAvgMin: {} minTimeEmpty: {} alertCount_Bad: {}".format(samplesBad,longAvgMin,minTimeEmpty,alertCount_Bad))

    # only check this if no one is in the room
    last = PersistenceExtensions.previousState(ir.getItem("PirState_Bad")).timestamp
    timeEmpty = seconds_between(last, DateTime.now())

    if timeEmpty < minTimeEmpty:
        #logg(u"only {}s  since last movement here, no check".format(timeEmpty))
        pass
    else:

        #logg(u"already {}s since last movement here, will check".format(timeEmpty))

        avgLong  = PersistenceExtensions.averageSince(ir.getItem("sensor_humidity_Bad"),DateTime.now().minusMinutes( longAvgMin ) ) 
        # etwas ulkige Typumwandlung        
        sAL = u"{}".format( avgLong ) 
        fAvgLong = float(sAL)

        currMeasurement=float(ir.getItem("sensor_humidity_Bad").state.toString())
        lHumBad.append(currMeasurement)
        
        if len(lHumBad)>samplesBad:
            lHumBad.pop(0)

        if avgLong == None:
            logg(u"nothing to compare with  avgLong {} ".format(avgLong))
            # nothing to compare with...
            return

        # check if values increase stetig
        iter = 0
        sum = 0
        stetig=True
        for el in lHumBad:
            sum += el
            if iter > 0:
                if lHumBad[iter-1]<lHumBad[iter]:
                    stetig=False
            iter+=1
        avgMeasured = sum/iter
        nextTrigger = lTriggerBad[alertCount_Bad]

        if avgMeasured < fAvgLong - nextTrigger and stetig:
            if alertCount_Bad < len(lTriggerBad)-1:
                alertCount_Bad +=1
                lEmoji=[u'\U00002744',u'\U000026C4',u'\U00002603']
                emoji=lEmoji[alertCount_Bad]
                blogg(u"{} Fenster im Bad vergessen?   jsr-Alarm{}  ".format(emoji,alertCount_Bad))
            #else:

        if not stetig:
            alertCount_Bad=0
            lHumBad = [currMeasurement]

        logg(u"Bad: fAvgLong: {} avgMeasured {}  sum {} iter {} stetig {} nextTrigger {} lHumBad:{}".format(fAvgLong,avgMeasured,sum,iter,stetig,nextTrigger,lHumBad))