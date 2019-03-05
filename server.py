import asyncio
import websockets
import uuid

players = {}

async def server(websocket, path):
    global players
    if path == '/login':
        u = uuid.uuid4().hex
        players[u] = None
        print('Someone logged in: '+u)
        await websocket.send(u)
    elif path == '/send':
        u = await websocket.recv()
        field = await websocket.recv()
        players[u] = field
        print(f'{u} sent their field: {field}')
        await websocket.send('ok')
    elif path == '/get':
        u = await websocket.recv()
        fields = []
        print(f'{u} requested other fields')
        for uid, field in players.items():
            if uid == u:
                continue
            if field == None:
                continue
            fields.append(field)
        print(f'found these: {repr(fields)}')
        await websocket.send(','.join(fields))
    elif path == '/logout':
        u = await websocket.recv()
        if u in players:
            players.pop(u)
        print(f'{u} logged out')


start_server = websockets.serve(server, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()