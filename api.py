import aiohttp

url = 'https://webapi.lowiro.com/'
me = 'webapi/user/me'
login = 'auth/login'

async def get_web_api(email, password):
    data = {'email': email, 'password': password}
    async with aiohttp.ClientSession() as session:
        async with session.post(url + login, data=data) as req:
            await req.json()

        async with session.get(url + me) as reqs:
            return await reqs.json()
