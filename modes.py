from field import *
import time

class MainMenu:
    def __init__(self, screen, Input):
        self.screen = screen
        self.Input = Input
        self.options = [
            ('Normal', Basic, lambda x: Basic.__init__(x, x.screen, x.Input)),
            ('20L Sprint', Sprint, lambda x: Sprint.__init__(x, 20, x.screen, x.Input)),
            ('40L Sprint', Sprint, lambda x: Sprint.__init__(x, 40, x.screen, x.Input)),
        ]
        self.selected = 0

    def run(self, key, dt):
        for i,o in enumerate(self.options):
            attr = 3 if i == self.selected else 0
            self.screen.print_at(o[0],
                self.screen.width//2-len(o[0])//2,
                self.screen.height-len(self.options)+i-self.screen.height//4,
                attr=attr)

        if key == self.screen.KEY_DOWN:
            self.selected = (self.selected + 1) % len(self.options)
        elif key == self.screen.KEY_UP:
            self.selected = (self.selected - 1) % len(self.options)
        # enter
        elif key == 13:
            self.__class__ = self.options[self.selected][1]
            self.options[self.selected][2](self)

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