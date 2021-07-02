import hoshino, os, time

from .api import get_web_api
from .sql import *

img = os.path.join(os.path.dirname(__file__), 'img')
songdir = os.path.join(img, 'songs')

diffdict = {
    '0' : ['pst', 'past'],
    '1' : ['prs', 'present'],
    '2' : ['ftr', 'future'],
    '3' : ['byd', 'beyond']
}

log = hoshino.new_logger('Arcaea_draw')

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

def playtime(date):
    timearray = time.localtime(date / 1000)
    datetime = time.strftime('%Y-%m-%d %H:%M:%S', timearray)
    return datetime

def sql_diff(diff):
    if diff == 0:
        sql_diff = 'rating_pst'
    elif diff == 1:
        sql_diff = 'rating_prs'
    elif diff == 1:
        sql_diff = 'rating_ftr'
    else:
        sql_diff = 'rating_byn'
    return sql_diff

async def draw_score(user_id):
    try:
        # 获取成绩
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
        difficulty = recentscore['difficulty']

        # 歌曲信息
        songinfo = asql.song_info(songid, sql_diff(difficulty))
        for i in songinfo:
            title = i[1] if i[1] else i[0]
            artist = i[2]
            songrating = i[3] / 10
        # 整理赋值
        songbg = os.path.join(songdir, songid, 'base.jpg' if difficulty != 3 else '3.jpg')
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
