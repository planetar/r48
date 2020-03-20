# von cycle.rules
# bestimme die aktuelle phase
# var String[] statesArray = newArrayList("early","morning","day","noon","afternoon","dusk","evening","salon","late","goodnight","night","away","gloomy")


from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
#import configuration
#reload(configuration)
#from configuration import mode_dict
from core.items import add_item
try:
    from org.openhab.core.thing import ChannelUID
except:
    from org.eclipse.smarthome.core.thing import ChannelUID

from org.joda.time import DateTime, Interval


from collections import OrderedDict 
'''

dieses dict in configuration.py zu halten hatte bei mir im ersten anlauf zur Folge, dass wegen eines Fehlers alle .py nicht mehr liefen.
Bisschen heiss

denke, dass kann hier gut der Treiber für die phasen sein, die weitere Ausfuehrung kann aber mehr an meinem bisherigen Modell orientiert bleiben

'''
mode_dict = OrderedDict([
    ("night"   , {"hour": 2, "minute": 0,  "second": 0}),
    ("early"   , {"channel": "astro:sun:local:civilDawn#event", "event": "START"}),
    ("morning" , {"channel": "astro:sun:local:rise#event", "event": "START"}),  
    ("day"    , {"hour": 9,  "minute": 0,  "second": 0}),
    ("noon"    , {"hour": 11,  "minute": 30,  "second": 0}),
    ("afternoon"    , {"hour": 14,  "minute": 0,  "second": 0}),
    ("dusk", {"channel": "astro:sun:local:civilDusk#event", "event": "START"}), 
    ("evening", {"hour": 20, "minute": 30,  "second": 0, "channel": "astro:sun:local:nauticDusk#event", "event": "START"}),
    ("salon", {"hour": 21, "minute": 45, "second": 0}),
    ("late"  , {"hour": 23, "minute": 59,  "second": 59})
])


if not itemRegistry.getItems("Mode"):
    add_item("Mode", item_type="String", label="Mode [%s]", category="House")

def mode_trigger_generator(mode_dict):
    def generated_triggers(function):
        for mode in list(mode_dict.keys()):
            if mode_dict[mode].get("second") is not None and mode_dict[mode].get("minute") is not None and mode_dict[mode].get("hour") is not None:
                when("Time cron {} {} {} * * ?".format(mode_dict[mode]["second"], mode_dict[mode]["minute"], mode_dict[mode]["hour"]))(function)
            if mode_dict[mode].get("channel") is not None and mode_dict[mode].get("event") is not None:
                when("Channel {} triggered {}".format(mode_dict[mode]["channel"], mode_dict[mode]["event"]))(function)
        return function
    return generated_triggers



# die phasen gloomy, away, goodnight und in der Regel auch night sind manuell ofer von anderen Ereignissen gesteuert,
# die übrigen sind die Mühle der mode of day
lPhasen = ["early","morning","day","noon","afternoon","dusk","evening","salon","late","goodnight","night","away","gloomy"]


@rule("Update Mode")
@when("System started")
@when("Item platzHalt27 received command ON")
@mode_trigger_generator(mode_dict)
def update_mode(event):
    last_mode_of_day = mode_dict.items()[-1][0]
    new_mode = last_mode_of_day
    for i, (mode, value) in enumerate(mode_dict.iteritems()):
        if mode != last_mode_of_day:
            if event is None and mode_dict[mode].get("hour") is not None and Interval(
                    DateTime.now().withTime(
                        value["hour"],
                        value["minute"],
                        value["second"],
                        0
                    ),
                    DateTime.now().withTime(
                        mode_dict.items()[i + 1][1].get("hour", value["hour"]),
                        mode_dict.items()[i + 1][1].get("minute", value["minute"] + 1),
                        mode_dict.items()[i + 1][1].get("second", value["second"]),
                        0
                    )
                ).contains(DateTime.now()):
                    new_mode = mode
                    break
            elif hasattr(event, "channel") and mode_dict[mode].get("channel") is not None and event.channel == ChannelUID(mode_dict[mode].get("channel")) and event.event == mode_dict[mode].get("event"):
                new_mode = mode
                break 

    ## der Sinn dieser Falunterscheidung entgeht mir, im Test fuehrt sie die ganze Prozedur ad absurdum
    ## nachgelesen, offenbar hat sie den Sinn, manuell gestzte Modes zu bewahren. Macht fuer mich trotzdem keinen Sinn
    #
    #if items["Mode"] != StringType(new_mode) and (str(items["Mode"]) in mode_dict.keys() or isinstance(items["Mode"], UnDefType)):
    #    update_mode.log.debug("Mode changed from [{}] to [{}]".format(items["Mode"], new_mode))
    #    events.sendCommand("Mode", new_mode)
    #else:
    #    update_mode.log.debug("Job ran but current Mode [{}] did not need to be changed: [{}]".format(items["Mode"], new_mode))

    update_mode.log.debug("Mode changed from [{}] to [{}]".format(items["Mode"], new_mode))
    
    # an 950_cycle.rules anbinden
    events.sendCommand("StateBtn_"+new_mode,"ON")

    # redundant?
    events.sendCommand("Mode", new_mode)