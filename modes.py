from field import *
import time

class Basic:
    def __init__(self, screen, Input):
        self.screen = screen
        self.Input = Input
        self.field = Field(screen,Input)

    def run(self, key, dt):
        self.field.update(key, dt)
        self.field.show()

class Sprint(Basic):
    def __init__(self, lines, *args):
        super().__init__(*args)
        self.lines = lines
        self.start = time.perf_counter()
        self.end = None

    def run(self, key, dt):
        if self.end == None:
            self.field.update(key, dt)
        self.field.show()
        self.screen.print_at(f'{self.field.lines}/{self.lines}',0,0)
        cur = time.perf_counter() if self.end == None else self.end
        self.screen.print_at(str(cur-self.start),0,1)
        if self.field.lines >= self.lines:
            self.end = cur