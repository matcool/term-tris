from field import *
from constants import *
from helpers import *
from timer import *
import time
import asyncio
import websockets
import threading

class MainMenu:
    def __init__(self, screen, Input, animate=False):
        self.screen = screen
        self.Input = Input
        self.options = [
            ('Normal', Basic, lambda x: Basic.__init__(x, x.screen, x.Input)),
            ('Multiplayer', Multiplayer, lambda x: Multiplayer.__init__(x, x.screen, x.Input)),
            ('20L Sprint', Sprint, lambda x: Sprint.__init__(x, 20, x.screen, x.Input)),
            ('40L Sprint', Sprint, lambda x: Sprint.__init__(x, 40, x.screen, x.Input)),
        ]
        self.selected = 0
        self.animate = animate
        self.typedIndex = 0
        self.typeTimer = Timer(7)
        self.beginTimer = Timer(30,loop=False)
        self.blinkTimer = Timer(60)
        updateColors(screen)

    def run(self, key, dt):
        yOff = self.drawlogo() + 1

        for i,o in enumerate(self.options):
            attr = 3 if i == self.selected else 0
            self.screen.print_at(o[0],
                self.screen.width//2-len(o[0])//2,
                yOff + i,
                attr=attr)

        if key == self.screen.KEY_DOWN:
            self.selected = (self.selected + 1) % len(self.options)
        elif key == self.screen.KEY_UP:
            self.selected = (self.selected - 1) % len(self.options)
        # enter
        elif key in (10,13):
            self.__class__ = self.options[self.selected][1]
            self.options[self.selected][2](self)

    def drawlogo(self):
        size = self.screen.height // 2
        sx = self.screen.width // 2 - size
        sy = size // 4
        corners = [(sx,sy),(sx+size*2,sy),(sx,sy+size),(sx+size*2,sy+size)]
        corners = [tuple(map(int,i)) for i in corners]
        fancyRect(self.screen,sx,sy,size*2,size)

        self.screen.print_at('>', corners[0][0] + 3, corners[0][1] + 4)
        text = 'term-tris'
        if not self.animate:
            self.screen.print_at(text, corners[0][0] + 5, corners[0][1] + 4)
        else:
            self.screen.print_at(text[:self.typedIndex], corners[0][0] + 5, corners[0][1] + 4)
            if self.beginTimer.check(1) and self.typeTimer.check(1):
                self.typedIndex += 1
                if self.typedIndex == len(text):
                    self.animate = False

        x = len(text) if not self.animate else self.typedIndex
        c = 7 if self.blinkTimer.timer < self.blinkTimer.after/2 else 0
        self.screen.print_at(' ', corners[0][0] + 5 + x, corners[0][1] + 4, bg=c)
        self.blinkTimer.check(1)

        return sy+size

class Basic:
    def __init__(self, screen, Input):
        self.screen = screen
        self.Input = Input
        self.field = Field(screen,Input)

    def run(self, key, dt):
        self.field.update(key, dt)
        self.field.show()

class Multiplayer(Basic):
    def __init__(self, screen, Input):
        super().__init__(screen, Input)
        self.response = None
        self.last = None
        self.timer = Timer(2)
        self.loop = asyncio.get_event_loop()
        self.thread = None
        self.uuid = None
        self.host = '10.0.0.107'
        self.port = 8000
        self.connect('login')
        self.others = []
        self.fields = []
        self.prevLines = 0

    def connect(self, path, *send):
        if self.loop.is_running():
            return
        self.response = None
        self.last = path
        def blocking(loop):
            async def connect():
                async with websockets.connect(f'ws://{self.host}:{self.port}/{path}') as websocket:
                    for i in send:
                        await websocket.send(i)
                    msg = await websocket.recv()
                    self.response = msg
            loop.run_until_complete(connect())
        self.thread = threading.Thread(target=blocking,args=(self.loop,))
        self.thread.start()

    def run(self, key, dt):
        super().run(key, dt)
        self.screen.print_at(str(self.uuid),0,0)
        for f in self.fields:
            f.show()

        if self.response != None and self.last != None and not self.loop.is_running():
            p = self.last
            if self.last == 'login':
                self.uuid = self.response
            elif self.last == 'send':
                self.connect('get', self.uuid)
            elif self.last == 'get':
                self.others = self.response.split(',')
                if self.others[0] == '':
                    self.others = []
                self.fields = []
                self.field.x = 10 # 10 because its the average width of a held piece times 2 and plus 2 for spacing
                xSpacing = (self.screen.width - self.field.width - 20) // (len(self.others) + 1)
                for j,o in enumerate(self.others):
                    f = Field(self.screen,basic=True)
                    f.x = (j+1) * xSpacing + self.field.x + self.field.width + 10
                    f.grid = list(o)
                    f.grid = [None if i == ' ' else i for i in f.grid]
                    self.fields.append(f)

                self.connect('garbage', self.uuid, str(self.field.lines - self.prevLines))
                self.prevLines = self.field.lines
            elif self.last == 'garbage':
                garbage = self.response
                if garbage != '':
                    garbage = [tuple(map(int,i.split(','))) for i in garbage.split(';')]
                    gblock = 'Z'
                    for g in garbage:
                        for _ in range(g[0]): self.field.move('up')
                        for y in range(g[0]):
                            for x in range(self.field.width):
                                if x == g[1]:
                                    continue
                                self.field.setCell(x,(self.field.height + self.field.hidden - 1) - y, gblock)



            if p == self.last:
                self.last = None
                self.response = None
            
        elif self.last == None:
            if self.timer.check(dt):
                fieldstr = ''.join(i if i != None else ' ' for i in self.field.grid)
                self.connect('send',self.uuid,fieldstr)

    def quit(self):
        async def connect():
            async with websockets.connect(f'ws://{self.host}:{self.port}/logout') as websocket:
                await websocket.send(self.uuid)
        self.loop.run_until_complete(connect())

                


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