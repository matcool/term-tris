import keyboard

PREVDOWN = []
DOWN = []
UP = []

def _callback(event):
    global DOWN, UP
    if event.event_type == keyboard.KEY_DOWN:
        if event.name not in DOWN: DOWN.append(event.name)
    else:
        if event.name not in UP: UP.append(event.name)

keyboard.hook(_callback)

def pressed(name):
    return name in DOWN and name not in PREVDOWN

def released(name):
    return name in UP

def down(name):
    return name in DOWN

def update():
    global DOWN, UP, PREVDOWN
    PREVDOWN = DOWN.copy()
    for i in UP.copy():
        if i in DOWN:
            DOWN.remove(i)
            UP.remove(i)