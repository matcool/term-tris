from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from field import Field
import time
import modes
import Input
import json

with open('config.json','r') as f:
    js = json.load(f)['client']['controls']
    for action, key in js.items():
        Input.bind(key, action)

def background(screen,color=0):
    for y in range(screen.height):
        screen.print_at(' '*screen.width, 0, y, bg=color)

def main(screen):
    framerate = 1/60
    dt = 0
    mode = modes.MainMenu(screen, Input, True)
    while True:
        start = time.perf_counter()
        Input.update()
        background(screen)
        ev = screen.get_event()
        key = ev.key_code if isinstance(ev, KeyboardEvent) else None
        if key in (ord('Q'), ord('q')):
            if hasattr(mode,'quit'):
                mode.quit()
            return
        elif key in (ord('E'), ord('e')):
            if hasattr(mode,'quit'):
                mode.quit()
            mode = modes.MainMenu(screen, Input)

        mode.run(key, dt)

        screen.refresh()
        end = time.perf_counter()
        if end - start < framerate:
            time.sleep(framerate - (end - start))
        dt = time.perf_counter() - start

Screen.wrapper(main)
