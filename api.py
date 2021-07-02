import aiohttp

api = 'http://xxxxx.cn'
url = 'https://webapi.lowiro.com/'
me = 'webapi/user/me'
login = 'auth/login'


async def get_api_info(project, arcid=0, diff=2, limit=0, song=None):
    try:
        if project == 'bind':
            url = f'{api}/v4/user/info?user={arcid}&usercode={arcid}&recent={limit}'
        elif project == 'info':
            url = f'{api}/v4/user/best30?user={arcid}&usercode={arcid}'
        elif project == 'recent':
            url = f'{api}/v4/user/info?user={arcid}&usercode={arcid}&recent=1'
        elif project == 'score':
            url = f'{api}/v4/user/best?user={arcid}&songname={song}&difficulty={diff}'
        elif project == 'bp':
            url = f'{api}/v4/user/best30?user={arcid}&usercode={arcid}&overflow={limit}'
        elif project == 'song':
            url = f'{api}/v4/song/info?songname={song}'
        else:
            raise 'Project Error'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as req:
                if req.status != 200:
                    return 'API服务器故障，请联系管理员'
                return await req.json()
    except Exception as e:
        return e

async def get_web_api(email, password):
    data = {'email': email, 'password': password}
    async with aiohttp.ClientSession() as session:
        async with session.post(url + login, data=data) as req:
            await req.json()

        async with session.get(url + me) as reqs:
            return await reqs.json()
            
