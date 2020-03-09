from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
import json

# @rule("Rule Name", description="Optional Rule Description", tags=["Tag 1", "Tag 2"])
# @when("Time cron 0/10 * * * * ?")
# @when("Item mqOfficePack received update")


verbose=True

'''

  Sensor calibration offsets

*/'''
#// officePack nachEichen: averrage uber 83: temp: 0.13867470 hum: -1.77503988
#// bad        nachEichen: averrage uber 94: temp: 1.53542553 hum: -5.86596819

def getOffsetsForSensor(sensorId):
    
    dOffsetTable = {
        "officePack"    :   (1.7, 9.3) ,
        "officeDesk"    :   (2.8, 1)    ,
        "SK"            :   (0.8, 5)    ,
        "bad"           :   (2, 6,2)   ,
        "kueche"        :   (1.1, 10.4)   ,
        "medi"          :   (0.4, -0.8)    ,
        "clara"         :   (-0.2, -0.2)    ,
        "flur"          :   (0.9, 6.4)  ,
        "balkon"        :   (0,0)   ,
        "feinstaub"     :   (0,0)

    }
    return dOffsetTable[sensorId]


# flur 
# sensor DHT on koel

@rule("parseSensorFlur", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "flur"])
@when("Item mqSensorFlur received update")
def parseSensorFlur(event):
    id="flur"
    t=0
    h=1

    tOffSets=getOffsetsForSensor(id)
    jsondata = json.loads(str(ir.getItem("mqSensorFlur").state))

    hum=jsondata["hum"]
    temp=jsondata["temp"]
    if hum == 0 and temp == 0:
        pass
    else:
        hum -= tOffSets[h]
        temp -= tOffSets[t]

        events.sendCommand("sensor_humidity_Flur", str(hum))
        events.sendCommand("sensor_temperature_Flur", str(temp))

        if verbose:
            parseSensorFlur.log.info(u"parsed "+id+": "+str(temp)+u"°, "+str(hum)+"% ")


# pir on koel   
# mqPirFlurKoel

@rule("parsePirFlurKoel", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "Flur"])
@when("Item mqPirFlurKoel received update")

def parsePirFlurKoel(event):
    id="flur"
    jsondata = json.loads(str(ir.getItem("mqPirFlurKoel").state))

    if jsondata.get("pir1") == "ON":
        events.sendCommand("PirState_Flur1", "ON")
    if jsondata.get("pir2") == "ON":
        events.sendCommand("PirState_Flur2", "ON")

    if verbose:
            parsePirFlurKoel.log.info(u"parsed "+str(id))    



# pir on    mqPirFlur
# pir/flur/state {"pir1":"OFF","pir2":"OFF","tocStatus":0,"lux":17,"rssi":-55,"vers":"1.05"}


@rule("parsePirFlur", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "Flur"])
@when("Item mqPirFlur received update")

def parsePirFlur(event):
    id="flur"
    jsondata = json.loads(str(ir.getItem("mqPirFlur").state))

    if jsondata.get("pir1") == "ON":
        events.sendCommand("PirState_Flur3", "ON")
    if jsondata.get("pir2") == "ON":
        events.sendCommand("PirState_Flur4", "ON")
    if jsondata.get("tocStatus") == "ON":
        events.sendCommand("flurSonderWunsch", "ON")
        
    if verbose:
            parsePirFlur.log.info(u"parsed "+str(id))    



# pirGarde
# mqPirGarde

@rule("parsePirGarde", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "Flur"])
@when("Item mqPirGarde received update")

def parsePirGarde(event):
    id="flurGarde"
    jsondata = json.loads(str(ir.getItem("mqPirGarde").state))

    if jsondata.get("pir") == "ON":
        events.sendCommand("PirState_Garde", "ON")
 
        
    if verbose:
            parsePirGarde.log.info(u"parsed "+str(id))    


# mqRfid


@rule("parseRfid", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "Flur"])
@when("Item mqRfid received update")

def parseRfid(event):
    id="rfid"
    jsondata = json.loads(str(ir.getItem("mqRfid").state))

    # rfidValid
    rValid = jsondata.get("rfidValid")
    if rValid != None:
        events.sendCommand("rfidValid", rValid)
 
    # rfidEntry
    rEntry = jsondata.get("mqRfid")    
    if rEntry != None:
        events.sendCommand("rfidEntry", rEntry)

    if verbose:
            parseRfid.log.info(u"parsed "+str(id))    





# bad

@rule("parseSensorBad", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "bad"])
@when("Item mqSensorBad received update")
def parseSensorBad(event):
    id="bad"
    t=0
    h=1

    tOffSets=getOffsetsForSensor(id)
    jsondata = json.loads(str(ir.getItem("mqSensorBad").state))

    hum=jsondata["hum"]
    temp=jsondata["temp"]
    if hum == 0 and temp == 0:
        pass
    else:
        hum -= tOffSets[h]
        temp -= tOffSets[t]

        events.sendCommand("sensor_humidity_Bad", str(hum))
        events.sendCommand("sensor_temperature_Bad", str(temp))
        events.sendCommand("sensor_lux_2", str(jsondata["lux"]))
        if verbose:
            parseSensorBad.log.info(u"parsed "+id+": "+str(temp)+u"°, "+str(hum)+"%, "+str(jsondata["lux"])+"lux")


# mqPir_bad


@rule("parsePirBad", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "Bad"])
@when("Item mqPir_bad received update")

def parsePirBad(event):
    id="pirBad"
    jsondata = json.loads(str(ir.getItem("mqPir_bad").state))

    if jsondata.get("pir1") == "ON":
        events.sendCommand("PirState_Bad1", "ON")
    if jsondata.get("pir2") == "ON":
        events.sendCommand("PirState_Bad2", "ON")

    if verbose:
            parsePirBad.log.info(u"parsed "+str(id))    


# mqPirBad3

@rule("parsePirBad3", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "Bad"])
@when("Item mqPirBad3 received update")

def parsePirBad(event):
    id="pirBad3"
    jsondata = json.loads(str(ir.getItem("mqPirBad3").state))

    if jsondata.get("pir") == "ON":
        events.sendCommand("PirState_Bad3", "ON")

    intenseState = jsondata.get("intense")
    events.sendCommand("IntenseBad", intenseState)

    if verbose:
            parsePirBad.log.info(u"parsed "+str(id))    



# kueche {"hum": 54.1, "temp": 20.6}

@rule("parseSensorKueche", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "kueche"])
@when("Item mqSensorKueche received update")
def parseSensorKueche(event):
    id="kueche"
    t=0
    h=1

    tOffSets=getOffsetsForSensor(id)
    jsondata = json.loads(str(ir.getItem("mqSensorKueche").state))

    hum=jsondata["hum"]
    temp=jsondata["temp"]
    if hum == 0 and temp == 0:
        pass
    else:
        hum -= tOffSets[h]
        temp -= tOffSets[t]

        events.sendCommand("sensor_humidity_Kueche", str(hum))
        events.sendCommand("sensor_temperature_Kueche", str(temp))

        if verbose:
            parseSensorKueche.log.info(u"parsed "+id+": "+str(temp)+u"°, "+str(hum)+"% ")


# mqPirKueche


@rule("parsePirKueche", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "Kueche"])
@when("Item mqPirKueche received update")

def parsePirKueche(event):
    id="pirKueche"
    jsondata = json.loads(str(ir.getItem("mqPirKueche").state))

    if jsondata.get("pir1") == "ON":
        events.sendCommand("PirState_Kueche", "ON")
    if jsondata.get("pir2") == "ON":
        events.sendCommand("PirState_Kueche2", "ON")
    if jsondata.get("pir3") == "ON":
        events.sendCommand("PirState_Kueche3", "ON")

    if verbose:
            parsePirKueche.log.info(u"parsed "+str(id))    


# Balkon
# mqWetterBalkon
# sensor/wetterBalkon/state {"pir":"OFF","temp":7.22,"hum":68.92773,"press":988.5295,"rPress":994.5274,"lux":3,"broad":0,"infrared":0,"rssi":-83,"vers":"1.20"}


@rule("parseWetterBalkon", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "balkon"])
@when("Item mqPirSK received update")
def parseWetterBalkon(event):
    id="balkon"
    t=0
    h=1

    tOffSets=getOffsetsForSensor(id)
    jsondata = json.loads(str(ir.getItem("mqWetterBalkon").state))

    hum=jsondata["hum"]
    temp=jsondata["temp"]
    if hum == 0 and temp == 0:
        pass
    else:
        hum -= tOffSets[h]
        temp -= tOffSets[t]

        events.sendCommand("sensor_bme280_temperature", str(temp))
        events.sendCommand("sensor_bme280_humidity", str(hum))

        events.sendCommand("sensor_bme280_pressure", str(jsondata["press"]))
        events.sendCommand("sensor_bme280_rPressure", str(jsondata["rPress"]))

        events.sendCommand("sensor_lux_4", str(jsondata["lux"]))
        events.sendCommand("sensor_bme280_broadband", str(jsondata["broad"]))
        events.sendCommand("sensor_bme280_infrared", str(jsondata["infrared"]))

        events.sendCommand("sensor_rssi_Balkon", str(jsondata["rssi"]))

        if jsondata["pir"] == "ON":
            events.sendCommand("PirState_Balkon", "ON")

        if verbose:
            parseWetterBalkon.log.info(u"parsed "+id+": "+str(temp)+u"°, "+str(hum)+"% "+str(jsondata["lux"])+"lux")


# feinStaub /LuftDaten
# mqLuftdaten
# sensor/feinstaub/state {"_type": "airRohr", "sensor_feinstaub_pressure": 989, "sensor_feinstaub_rPressure": 995, "sensor_feinstaub_pm25": "6.12", "sensor_feinstaub_hum": "100.00", "sensor_feinstaub_pm10": "11.77", "sensor_feinstaub_temp": "5.60", "sensor_feinstaub_signal": "-65"}


@rule("parseLuftDaten", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "balkon"])
@when("Item mqLuftdaten received update")
def parseLuftDaten(event):
    id="balkon"

    tOffSets=getOffsetsForSensor(id)
    jsondata = json.loads(str(ir.getItem("mqLuftdaten").state))

    # hier gibt es kein Filtern

    events.sendCommand("sensor_feinstaub_temp", str(jsondata["sensor_feinstaub_temp"]))
    events.sendCommand("sensor_feinstaub_hum", str(jsondata["sensor_feinstaub_hum"]))

    events.sendCommand("sensor_feinstaub_pressure", str(jsondata["sensor_feinstaub_pressure"]))
    events.sendCommand("sensor_feinstaub_rPressure", str(jsondata["sensor_feinstaub_rPressure"]))

    events.sendCommand("sensor_feinstaub_pm25", str(jsondata["sensor_feinstaub_pm25"]))
    events.sendCommand("sensor_feinstaub_pm10", str(jsondata["sensor_feinstaub_pm10"]))

    events.sendCommand("sensor_feinstaub_signal", str(jsondata["sensor_feinstaub_signal"]))



    if verbose:
        parseLuftDaten.log.info(u"parsed "+id+": "+str(jsondata["sensor_feinstaub_pm25"])+u"°, "+str(jsondata["sensor_feinstaub_pm10"])+" ")





# SK  
# mqPirSK 
# sensor/sk/state {"pir1":"OFF","pir2":"OFF","toc":"OFF","temp":20.1,"hum":48,"lux":8,"rssi":-62,"vers":"1.11"}

@rule("parseSensorSK", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "SK"])
@when("Item mqPirSK received update")
def parseSensorSK(event):
    id="SK"
    t=0
    h=1

    tOffSets=getOffsetsForSensor(id)
    jsondata = json.loads(str(ir.getItem("mqPirSK").state))

    hum=jsondata["hum"]
    temp=jsondata["temp"]
    if hum == 0 and temp == 0:
        pass
    else:
        hum -= tOffSets[h]
        temp -= tOffSets[t]

        events.sendCommand("sensor_humidity_SK", str(hum))
        events.sendCommand("sensor_temperature_SK", str(temp))
        events.sendCommand("sensor_lux_3", str(jsondata["lux"]))
        events.sendCommand("sensor_rssi_SK", str(jsondata["rssi"]))
        if jsondata["pir1"] == "ON":
            events.sendCommand("PirState_SK", "ON")
        if jsondata["pir2"] == "ON":
            events.sendCommand("PirState_SK2", "ON")
        if jsondata["toc"] == "ON":
            events.sendCommand("TocState_SK", "ON")

        if verbose:
            parseSensorSK.log.info(u"parsed "+id+": "+str(temp)+u"°, "+str(hum)+"% "+str(jsondata["lux"])+"lux")


# Clara

# mqPirClara sensor/clara/state {"pir1":"OFF","pir2":"OFF","temp":20.8,"hum":46,"lastTemp":20.8,"lastHum":46.1,"fail2win":"0/369","lux":15,"rssi":"-38","vers":"1.09b"}

@rule("parsePirClara", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "Clara"])
@when("Item mqPirClara received update")
def parsePirClara(event):
    id="clara"
    jsondata = json.loads(str(ir.getItem("mqPirClara").state))
    events.sendCommand("sensor_lux_6", str(jsondata["lux"]))
    events.sendCommand("sensor_rssi_Clara", str(jsondata["rssi"]))
    if jsondata["pir1"] == "ON":
        events.sendCommand("PirState_Clara1", "ON")
    if jsondata["pir2"] == "ON":
        events.sendCommand("PirState_Clara2", "ON")
    if verbose:
            parsePirClara.log.info(u"parsed "+str(id)+": "+str(jsondata["lux"])+" lux")    




# mqMulti sensor/multi/state {"pir1":"OFF","pir2":"OFF","temperature":19.37,"humidity":43.79395,"pressure":994.2054,"rPressure":1000.594,"rssi":"-54","vers":"1.19"}

@rule("parseSensorClara", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "Clara"])
@when("Item mqMulti received update")
def parseSensorClara(event):
    id="clara"
    t=0
    h=1

    tOffSets=getOffsetsForSensor(id)
    jsondata = json.loads(str(ir.getItem("mqMulti").state))

    hum=jsondata["humidity"]
    temp=jsondata["temperature"]
    if hum == 0 and temp == 0:
        pass
    else:
        hum -= tOffSets[h]
        temp -= tOffSets[t]

        events.sendCommand("sensor_humidity_Clara", str(hum))
        events.sendCommand("sensor_temperature_Clara", str(temp))
        events.sendCommand("sensor_pressure_Clara", str(jsondata["pressure"]))
        events.sendCommand("sensor_rPressure_Clara", str(jsondata["rPressure"]))
        events.sendCommand("sensor_rssi_Multi", str(jsondata["rssi"]))
        if jsondata["pir1"] == "ON":
            events.sendCommand("PirState_Clara3", "ON")
        if jsondata["pir2"] == "ON":
            events.sendCommand("PirState_Clara4", "ON")
        
        if verbose:
            parseSensorClara.log.info(u"parsed "+id+": "+str(temp)+u"°, "+str(hum)+"% ")


# mqPirMedi 
# sensor/medi/state {"pir":"OFF","temp":21.4,"hum":51,"lastTemp":21.4,"lastHum":51.2,"fail2win":"0/399","temperature":19.5,"humidity":44.5,
#                    "pressure":995.6454,"rPressure":1001.686,"lux":38,"rssi":"-71","rushLux":"OFF","showPir":"OFF","showErr":"OFF","vers":"1.11"}

@rule("parseSensorMedi", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "medi"])
@when("Item mqPirMedi received update")
def parseSensorMedi(event):
    id="medi"
    t=0
    h=1

    tOffSets=getOffsetsForSensor(id)
    jsondata = json.loads(str(ir.getItem("mqPirMedi").state))

    hum=jsondata["humidity"]
    temp=jsondata["temperature"]
    if hum == 0 and temp == 0:
        pass
    else:
        hum -= tOffSets[h]
        temp -= tOffSets[t]

        events.sendCommand("sensor_humidity_Medi", str(hum))
        events.sendCommand("sensor_temperature_Medi", str(temp))
        events.sendCommand("sensor_lux_7", str(jsondata["lux"]))
        events.sendCommand("sensor_rssi_Medi", str(jsondata["rssi"]))
        if jsondata["pir"] == "ON":
            events.sendCommand("PirState_Medi", "ON")

        if verbose:
            #parseSensorMedi.log.info(u"parsed "+id+": "+str(temp)+u"°, "+str(hum)+"% "+str(jsondata["lux"])+"lux")
            parseSensorMedi.log.info(u"parsed {}: {}° -> {}  {}% -> {}  {} lux".format(id,str(jsondata["temperature"]), str(temp), str(jsondata["humidity"]),  str(hum),  str(str(jsondata["lux"]))  ) )

# office
# officeDesk
# sensor/officeDesk/state {"temp":23.5,"hum":41.7,"lastTemp":23.5,"lastHum":41.8,"fail2win":"0/6626","lux":74,"rssi":"-45","rushLux":"OFF","showPir":"OFF","showErr":"OFF","vers":"1.07"}
# sensor/officeDesk/state {"pir":"OFF","toc":"OFF","temp":0,"hum":0,"lastTemp":-128,"lastHum":-1,"fail2win":"10/0","lux":152,"rssi":"-43","rushLux":"OFF","showPir":"OFF","showErr":"OFF","vers":"1.08"}

@rule("parseOfficeDesk", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "officeDesk"])
@when("Item mqOfficeDesk received update")
def parseOfficeDesk(event):
    id="officeDesk"
    t=0
    h=1

    tOffSets=getOffsetsForSensor(id)
    jsondata = json.loads(str(ir.getItem("mqOfficeDesk").state))

    hum=jsondata["hum"]
    temp=jsondata["temp"]
    if hum == 0 and temp == 0:
        pass
    else:
        hum -= tOffSets[h]
        temp -= tOffSets[t]

        events.sendCommand("sensor_humidity_OfficeDesk", str(hum))
        events.sendCommand("sensor_temperature_OfficeDesk", str(temp))
        events.sendCommand("sensor_lux_8", str(jsondata["lux"]))

        if jsondata.get("pir") == "ON":
            events.sendCommand("PirState_OfficeDesk", "ON")
        if jsondata.get("toc") == "ON":
            events.sendCommand("sensor_temperature_OfficeDesk", "ON")

        if verbose:
            parseOfficeDesk.log.info(u"parsed "+id+": "+str(temp)+u"°, "+str(hum)+"%, "+str(jsondata["lux"])+"lux")



# officePack
# mqOfficePack
# sensor/officePack/state {"temp":22.26,"hum":52.67773,"press":996.5044,"rPress":1002.915,"lux":20,"pir":"ON","toc":"OFF","rushLux":"OFF","loopDsp":"ON","refDsp":"ON","scanWifi":"OFF","vers":"1.09"}


@rule("parseOfficePack", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "Clara"])
@when("Item mqOfficePack received update")
def parseOfficePack(event):
    id="officePack"
    t=0
    h=1

    tOffSets=getOffsetsForSensor(id)
    jsondata = json.loads(str(ir.getItem("mqOfficePack").state))

    hum=jsondata["hum"]
    temp=jsondata["temp"]
    if hum == 0 and temp == 0:
        pass
    else:
        hum -= tOffSets[h]
        temp -= tOffSets[t]

        events.sendCommand("sensor_temperature_OfficePack", str(temp))
        events.sendCommand("sensor_humidity_OfficePack", str(hum))
        events.sendCommand("sensor_pressure_OfficePack", str(jsondata["rPress"]))
        
        events.sendCommand("sensor_luminosity_OfficePack", str(jsondata["lux"]))
        #events.sendCommand("sensor_rssi_Multi", str(jsondata["rssi"]))

        if jsondata.get("pir") == "ON":
            events.sendCommand("PirState_OfficePack", "ON")

        # this will trigger an error: 
        #if jsondata["por"] == "ON":
        #    events.sendCommand("PirState_OfficePack", "ON")
        
        if verbose:
            parseOfficePack.log.info(u"parsed "+id+": "+str(temp)+u"°, "+str(hum)+"% ")



# officeTuer
# mqOfficeTuer
# PirState_OfficeTuer

@rule("parseOfficeTuer", description="parse JSON sensorData and apply correction", tags=["sensor", "mqtt", "office"])
@when("Item mqOfficeTuer received update")
def parseOfficeTuer(event):
    
    jsondata = json.loads(str(ir.getItem("mqOfficeTuer").state))
 
    if jsondata["pir"] == "ON":
        events.sendCommand("PirState_OfficeTuer", "ON")

