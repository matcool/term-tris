from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from field import Field

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
    field = Field(screen,Input)
    while True:
        Input.update()
        background(screen)
        ev = screen.get_event()
        key = ev.key_code if isinstance(ev, KeyboardEvent) else None
        if key in (ord('Q'), ord('q')):
            return

        field.update(key)
        field.show()

        screen.refresh()

Screen.wrapper(main)