import asyncio
import websockets
import uuid
import random
import json
from time import perf_counter

players = {}
"""
players is supposed to have this structure:
    { 
        uuid : {
            'field' : (grid as a flat string),
            'garbage' : [(amount, x), (3, 1), (10, 9)]
            'last-update': 3.543
        }
    }

"""

uid_display = 5

async def server(websocket, path):
    global players
    time = perf_counter()
    if path == '/login':
        u = uuid.uuid4().hex
        players[u] = {'last-update':time}
        print('Someone logged in: '+u[:uid_display])
        await websocket.send(u)
    elif path == '/send':
        u = await websocket.recv()
        field = await websocket.recv()
        players[u]['field'] = field
        players[u]['last-update'] = time
        print(f'{u[:uid_display]} sent their field')
        await websocket.send('')
    elif path == '/get':
        u = await websocket.recv()
        players[u]['last-update'] = time
        fields = []
        print(f'{u[:uid_display]} requested other fields')
        for uid, player in players.items():
            if uid == u or player.get('field') == None:
                continue
            fields.append(player['field'])
        await websocket.send(','.join(fields))
    elif path == '/logout':
        u = await websocket.recv()
        if u in players:
            players.pop(u)
        print(f'{u[:uid_display]} logged out')
    elif path == '/garbage':
        u = await websocket.recv()
        lines = int(await websocket.recv())
        players[u]['last-update'] = time

        print(f'{u[:uid_display]} sent {lines} lines.')

        if lines > 0:
            _ = list(filter(lambda x: x != u, players))
            if len(_) != 0:
                garbage_sent = (lines, random.randint(0,9))
                send_to = random.choice(_)
                if players[send_to].get('garbage') == None:
                    players[send_to]['garbage'] = []
                players[send_to]['garbage'].append(garbage_sent)

        if players[u].get('garbage') != None:
            g = players[u]['garbage']
            players[u]['garbage'] = []
            await websocket.send(';'.join(','.join(map(str,i)) for i in g))
        else:
            await websocket.send('')

with open('config.json','r') as f:
    a = {}
    js = json.load(f).get('server',a)
    host = js.get('host','localhost')
    port = js.get('port',8000)
    timeout = js.get('timeout',10)

async def check_timeout():
    global players
    while True:
        time = perf_counter()
        to_timeout = []
        for player, data in players.items():
            if time - data.get('last-update',0) >= timeout:
                to_timeout.append(player)
        for p in to_timeout:
            print(f'{p[:uid_display]} has been timeouted.')
            players.pop(p)
        await asyncio.sleep(timeout/2)


start_server = websockets.serve(server, host, port)

asyncio.get_event_loop().run_until_complete(asyncio.gather(
    start_server,
    check_timeout()
    ))
asyncio.get_event_loop().run_forever()