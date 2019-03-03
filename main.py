from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from field import Field

def background(screen,color=0):
    for x in range(screen.width):
        for y in range(screen.height):
            screen.print_at(' ', x, y, bg=color)

def main(screen):
    field = Field(screen)
    while True:
        background(screen)
        ev = screen.get_event()
        key = ev.key_code if isinstance(ev, KeyboardEvent) else None
        if key in (ord('Q'), ord('q')):
            return

        field.update(key)
        field.show()

        screen.refresh()

Screen.wrapper(main)