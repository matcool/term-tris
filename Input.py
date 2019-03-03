# big copy paste of this: https://github.com/deagahelio/hmbg-input
import keyboard

class Action:
    def __init__(self, name):
        self.name = name
        self.bound = []
        self.down = False
        self.pressed = False
        self.released = False

    def bind(self, key):
        self.bound.append(key)

    def update(self):
        self.pressed = False
        self.released = False

        for key in self.bound:
            if keyboard.is_pressed(key):
                if not self.pressed and not self.down:
                    self.pressed = True

                self.down = True
                return

        if not self.released and self.down:
            self.released = True

        self.down = False

actions = {}

def bind(key, action):
    global actions
    if actions.get(action) == None:
        actions[action] = Action(action)
    actions[action].bind(key)

def pressed(action): return actions[action].pressed
def released(action): return actions[action].released
def down(action): return actions[action].down

def update():
    global actions
    for action in actions.values():
        action.update()