"""
The '.example' will need to be removed from this file's name in order to use
the personal package. This file is distributed as __init__.py.example to avoid
overwritting user files during an upgrade.

Here is where you will place your personally developed libraries. 
Helper methods, abstract classes, and other stuff like that will go here. 
There is an important distinction between the code placed here and the code placed in 
$OH_CONF/automation/JSR223/python/personal. 
Code placed here is statically compiled which means you need to force Jython to reload them 
(either through a restart of OH or an import directive). Simply saving the file will not cause your changed to be reloaded.

Take note, unlike with Rules DSL, functions and classes are very well supported in Jython.
"""
