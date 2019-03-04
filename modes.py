from field import *
from constants import *
import time

class MainMenu:
    def __init__(self, screen, Input, animate=False):
        self.screen = screen
        self.Input = Input
        self.options = [
            ('Normal', Basic, lambda x: Basic.__init__(x, x.screen, x.Input)),
            ('20L Sprint', Sprint, lambda x: Sprint.__init__(x, 20, x.screen, x.Input)),
            ('40L Sprint', Sprint, lambda x: Sprint.__init__(x, 40, x.screen, x.Input)),
        ]
        self.selected = 0
        self.animate = animate
        self.typedIndex = 0
        self.typeTimer = 0
        self.beginTimer = 0
        self.blinkTimer = 5
        updateColors(screen)

    def run(self, key, dt):
        for i,o in enumerate(self.options):
            attr = 3 if i == self.selected else 0
            self.screen.print_at(o[0],
                self.screen.width//2-len(o[0])//2,
                self.screen.height-len(self.options)+i-self.screen.height//4,
                attr=attr)

        self.drawlogo()

        if key == self.screen.KEY_DOWN:
            self.selected = (self.selected + 1) % len(self.options)
        elif key == self.screen.KEY_UP:
            self.selected = (self.selected - 1) % len(self.options)
        # enter
        elif key == 13:
            self.__class__ = self.options[self.selected][1]
            self.options[self.selected][2](self)

    def drawlogo(self):
        tiles = ['│','─','┌','┐','└','┘']
        size = self.screen.height // 2
        sx = self.screen.width // 2 - size
        sy = size // 4
        def line(x1,y1,x2,y2,char):
            self.screen.move(int(x1),int(y1))
            self.screen.draw(int(x2),int(y2),char=char)
        corners = [(sx,sy),(sx+size*2,sy),(sx,sy+size),(sx+size*2,sy+size)]
        corners = [tuple(map(int,i)) for i in corners]
        line(*corners[0],*corners[1],tiles[1])
        line(*corners[0],*corners[2],tiles[0])
        line(*corners[2],*corners[3],tiles[1])
        line(*corners[1],*corners[3],tiles[0])
        self.screen.print_at(tiles[2],*corners[0])
        self.screen.print_at(tiles[3],*corners[1])
        self.screen.print_at(tiles[4],*corners[2])
        self.screen.print_at(tiles[5],*corners[3])


        self.screen.print_at('>', corners[0][0] + 3, corners[0][1] + 4)
        text = 'term-tris'
        if not self.animate:
            self.screen.print_at(text, corners[0][0] + 5, corners[0][1] + 4)
        else:
            self.screen.print_at(text[:self.typedIndex], corners[0][0] + 5, corners[0][1] + 4)
            self.beginTimer += 1
            if self.beginTimer > 30:
                self.beginTimer -= 1
                self.typeTimer += 1
                if self.typeTimer == 7:
                    self.typeTimer = 0
                    self.typedIndex += 1
                    if self.typedIndex == len(text):
                        self.animate = False

        x = len(text) if not self.animate else self.typedIndex
        blinkAfter = 30
        c = 7 if self.blinkTimer < blinkAfter else 0
        self.screen.print_at(' ', corners[0][0] + 5 + x, corners[0][1] + 4, bg=c)
        self.blinkTimer = (self.blinkTimer + 1) % (blinkAfter * 2)


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