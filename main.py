from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from field import Field
import time
import modes
import Input

Input.bind('left', 'left')
Input.bind('right', 'right')
Input.bind('down', 'softDrop')
Input.bind('up', 'hardDrop')
Input.bind('x', 'rotateCw')
Input.bind('z', 'rotateCcw')
Input.bind('c', 'hold')

def background(screen,color=0):
    for y in range(screen.height):
        screen.print_at(' '*screen.width, 0, y, bg=color)

def main(screen):
    framerate = 1/60
    dt = 0
    mode = modes.Basic(screen, Input)
    while True:
        start = time.perf_counter()
        Input.update()
        background(screen)
        ev = screen.get_event()
        key = ev.key_code if isinstance(ev, KeyboardEvent) else None
        if key in (ord('Q'), ord('q')):
            return

        mode.run(key, dt)

        screen.refresh()
        end = time.perf_counter()
        if end - start < framerate:
            time.sleep(framerate - (end - start))
        dt = time.perf_counter() - start

Screen.wrapper(main)
