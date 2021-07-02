import hoshino, os, time, asyncio
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

from .arcaea_api import Arcaea
from .api import get_api_info, get_web_api
from .sql import *
from .song import songrating

img = os.path.join(os.path.dirname(__file__), 'img')
chardir = os.path.join(img, 'char')
pttdir = os.path.join(img, 'ptt')
rankdir = os.path.join(img, 'rank')
songdir = os.path.join(img, 'songs')
diffdir = os.path.join(img, 'diff')

Exo_Regular = os.path.join(img, 'font', 'Exo-Regular.ttf')
GeosansLight = os.path.join(img, 'font', 'GeosansLight.ttf')

diffdict = {
    '0' : ['pst', 'past'],
    '1' : ['prs', 'present'],
    '2' : ['ftr', 'future'],
    '3' : ['byd', 'beyond']
}

log = hoshino.new_logger('Arcaea_draw')

class datatext:
    #L=X轴，T=Y轴，size=字体大小，fontpath=字体文件，
    def __init__(self, L, T, size, text, path, anchor = 'lt'):
        self.L = L
        self.T = T
        self.text = str(text)
        self.path = path
        self.font = ImageFont.truetype(self.path, size)
        self.anchor = anchor

def write_text(image, font, text='text', pos=(0, 0), color=(255, 255, 255, 255), anchor='lt'):
    rgba_image = image
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    image_draw.text(pos, text, font=font, fill=color, anchor=anchor)
    return Image.alpha_composite(rgba_image, text_overlay)

def draw_text(image, class_text: datatext, color=(255, 255, 255, 255)):
    font = class_text.font
    text = class_text.text
    anchor = class_text.anchor
    return write_text(image, font, text, (class_text.L, class_text.T), color, anchor)

def open_img(img):
    with open(img, 'rb') as f:
        im = Image.open(f).convert('RGBA')
    return im

def pttbg(ptt):
    if ptt == -1:
        return 'rating_off.png'
    ptt /= 100
    if ptt < 3:
        name = 'rating_0.png'
    elif 3 <= ptt < 7:
        name = 'rating_1.png'
    elif 7 <= ptt < 10:
        name = 'rating_2.png'
    elif 10 <= ptt < 11:
        name = 'rating_3.png'
    elif 11 <= ptt < 12:
        name = 'rating_4.png'
    elif 12 <= ptt < 12.5:
        name = 'rating_5.png'
    else:
        name = 'rating_6.png'
    return name

def isrank(score):
    if score < 8600000:
        rank = 'D'
    elif 8600000 <= score < 8900000:
        rank = 'C'
    elif 8900000 <= score < 9200000:
        rank = 'B'
    elif 9200000 <= score < 9500000:
        rank = 'A'
    elif 9500000 <= score < 9800000:
        rank = 'AA'
    elif 9800000 <= score < 9900000:
        rank = 'EX'
    else:
        rank = 'EX+'
    return rank

def calc_rating(songid, difficulty, score):
    if score >= 10000000:
        rating = songrating[songid][str(difficulty)] + 2
    elif score >= 9800000:
        rating = songrating[songid][str(difficulty)] + 1 + (score - 9800000) / 200000
    else:
        rating = songrating[songid][str(difficulty)] + (score - 9500000) / 300000
    return rating

def playtime(date):
    timearray = time.localtime(date / 1000)
    datetime = time.strftime('%Y-%m-%d %H:%M:%S', timearray)
    return datetime

def timediff(date):
    now = time.mktime(datetime.now().timetuple())
    time_diff = (now - date / 1000) / 86400
    return time_diff

async def draw_score(user_id):
    try:
        # 获取用户名
        asql = arcsql()
        bindinfo = asql.get_bind_id(user_id)
        arcid, bind_id = bindinfo[0][0], bindinfo[0][1]
        result = asql.get_login(bind_id)
        scoreinfo = await get_web_api(result[0][0], result[0][1])
        friends = scoreinfo['value']['friends']
        for n, i in enumerate(friends):
            if user_id == i['user_id']:
                userinfo = friends[n]
                break

        arcname = userinfo['name']
        recentscore = userinfo['recent_score'][0]
        songid = recentscore['song_id']

        # 歌曲信息
        getsonginfo = await get_api_info('song', song=songid)
        if getsonginfo['status'] == -1:
            return '未找到该曲目，请确认曲名'
        songinfo = getsonginfo['content']
        song_id = songinfo['id']
        title = songinfo['title_localized']['en'] if len(songinfo['title_localized']) == 1 else songinfo['title_localized']['ja']
        artist = songinfo['artist']
        difficulty = recentscore['difficulty']
        diffinfo = songinfo['difficulties'][difficulty]
        songrating = diffinfo['ratingReal']
        # 整理赋值
        songbg = os.path.join(songdir, song_id, 'base.jpg' if difficulty != 3 else '3.jpg')
        score = recentscore['score']
        sp_count = recentscore['shiny_perfect_count']
        p_count = recentscore['perfect_count']
        far_count = recentscore['near_count']
        miss_count = recentscore['miss_count']
        health = recentscore['health']
        modifier = recentscore['modifier']
        play_time = recentscore['time_played']
        best_clear = recentscore['best_clear_type']
        clear = recentscore['clear_type']
        rating = recentscore['rating']

        msg = f'''
[CQ:image,file=file:///{songbg}]
Player: {arcname}
Code: {arcid}
Play Time: {playtime(play_time)}
---------------------------------
Song: {title}
Artist: {artist}
Difficulty: {diffdict[str(difficulty)][0].upper()} | SongRating: {songrating}
---------------------------------
Score: {score:,}
Rank: {'F' if health == -1 else isrank(score)}
Pure: {p_count} (+{sp_count})
Far: {far_count}
Lost: {miss_count}
Rating: {rating:.2f}'''
        return msg
    except Exception as e:
        log.error(e)
        return f'Error {type(e)}'

async def bindinfo(qqid, arcid, arcname):
    asql = arcsql()
    asql.insert_temp_user(qqid, arcid, arcname.lower())
    return f'用户 {arcid} 已成功绑定QQ {qqid}， 请等待管理员确认是否为好友'

async def newbind():
    try:
        asql = arcsql()
        result = asql.get_all_login()
        for i in result:
            bind_id = i[0]
            info = await get_web_api(i[1], i[2])
            friend = info['value']['friends']
            for m in friend:
                arcname = m['name']
                user_id = m['user_id']
                name = asql.get_user_name(user_id)
                if name: continue
                asql.insert_user(arcname.lower(), user_id, bind_id)
        log.info('添加成功')
        return '添加成功'
    except Exception as e:
        log.error(f'Error {e}')
        return '添加失败'
