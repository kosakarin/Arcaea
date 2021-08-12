import aiohttp, websockets, json, brotli

url = 'https://webapi.lowiro.com/'
me = 'webapi/user/me'
login = 'auth/login'
est = 'wss://arc.estertion.win:616/'

async def get_web_api(email, password, ac: bool = False):
    data = {'email': email, 'password': password}
    async with aiohttp.ClientSession() as session:
        async with session.post(url + login, data=data) as req:
            if ac:
                ok = True if req.status == 200 else False
                return ok 

        async with session.get(url + me) as reqs:
            return await reqs.json()

async def arcb30(arcid: str, re: bool = False):
    try:
        b30_data = []
        async with websockets.connect(est) as ws:
            await ws.send(str(arcid))
            while True:
                if ws.closed:
                    break
                data = await ws.recv()
                if data == 'error,add':
                    return '连接查分器错误'
                elif data == 'bye':
                    return b30_data
                elif isinstance(data, bytes):
                    info = json.loads(brotli.decompress(data))
                    if info['cmd'] == 'userinfo' and re:
                        return info
                    elif info['cmd'] == 'scores':
                        b30_data.append(info)
    except Exception as e:
        return f'Error: {type(e)}'
