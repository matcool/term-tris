import asyncio
import websockets
import uuid
import random

players = {}
"""
players is supposed to have this structure:
    { 
        uuid : {
            'field' : (grid as a flat string),
            'garbage' : [(amount, x), (3, 1), (10, 9)]
        }
    }

"""

uid_display = 5

async def server(websocket, path):
    global players
    if path == '/login':
        u = uuid.uuid4().hex
        players[u] = {}
        print('Someone logged in: '+u[:uid_display])
        await websocket.send(u)
    elif path == '/send':
        u = await websocket.recv()
        field = await websocket.recv()
        players[u]['field'] = field
        print(f'{u[:uid_display]} sent their field')
        await websocket.send('ok')
    elif path == '/get':
        u = await websocket.recv()
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



start_server = websockets.serve(server, '10.0.0.107', 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()