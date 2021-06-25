import hoshino
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os, time

from .api import get_api_info
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
    rgba_image = image.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    image_draw.text(pos, text, font=font, fill=color, anchor=anchor)
    return Image.alpha_composite(rgba_image, text_overlay)

def draw_text(image, class_text: datatext, color=(255, 255, 255, 255)):
    font = class_text.font
    text = class_text.text
    anchor = class_text.anchor
    return write_text(image, font, text, (class_text.L, class_text.T), color, anchor)

def pttbg(ptt):
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

def playtime(date):
    timearray = time.localtime(date / 1000)
    datetime = time.strftime('%Y-%m-%d %H:%M:%S', timearray)
    return datetime

def timediff(date):
    now = time.mktime(datetime.now().timetuple())
    time_diff = (now - date / 1000) / 86400
    return time_diff

async def draw_info(arcid):
    try:
        info = await get_api_info('info', arcid)
        if info['status'] != 0:
            return '查询错误'
        elif isinstance(info, str):
            return info
        scoreinfo = info['content']
        b30 = scoreinfo['best30_avg']
        r10 = scoreinfo['recent10_avg']
        b30_list = scoreinfo['best30_list']
        if not b30_list:
            return '您未上传过成绩'
        # 获取用户名
        user = await get_api_info('bind', arcid)
        content = user['content']
        arcname = content['name']
        code = content['code']
        character = content['character']
        is_char_uncapped = content['is_char_uncapped']
        is_char_uncapped_override = content['is_char_uncapped_override']
        icon_name = f'{character}u_icon.png' if is_char_uncapped ^ is_char_uncapped_override else f'{character}_icon.png'
        userrating = content['rating']
        # 图片整理
        icon = os.path.join(chardir, icon_name)
        ptt = os.path.join(pttdir, pttbg(userrating))
        # 新建底图
        bg = os.path.join(img, 'b30_bg.png')
        im = Image.new('RGBA', (1800, 3000))
        b30_bg = Image.open(bg).convert('RGBA')
        im.alpha_composite(b30_bg)
        # 角色
        icon_bg = Image.open(icon).convert('RGBA').resize((250, 250))
        im.alpha_composite(icon_bg, (175, 275))
        # ptt背景
        ptt_bg = Image.open(ptt).convert('RGBA').resize((150, 150))
        im.alpha_composite(ptt_bg, (300, 400))
        # ptt
        w_ptt = datatext(375, 475, 45, userrating / 100, Exo_Regular, anchor='mm')
        im = draw_text(im, w_ptt)
        # arcname
        w_arcname = datatext(455, 400, 85, arcname, GeosansLight, anchor='lb')
        im = draw_text(im, w_arcname)
        # arcid
        w_arcid = datatext(480, 475, 60, f'ID:{code}', Exo_Regular, anchor='lb')
        im = draw_text(im, w_arcid)
        # r10
        w_r10 = datatext(1100, 400, 60, f'Renct 10: {r10:.3f}', Exo_Regular, anchor='lb')
        im = draw_text(im, w_r10)
        # b30
        w_b30 = datatext(1100, 425, 60, f'Best 30: {b30:.3f}', Exo_Regular)
        im = draw_text(im, w_b30)
        # 30个成绩
        bg_y = 580
        for num, i in enumerate(b30_list):
            # 横3竖10
            if num % 3 == 0:
                bg_y += 240 if num != 0 else 0
                bg_x = 30
            else:
                bg_x += 600
            # 歌曲信息
            songid = i['song_id']
            difficulty = i['difficulty']
            # getsonginfo = await get_api_info('song', song=songid)
            # songinfo = getsonginfo['content']
            # try:
            #     title = songinfo['title_localized']['ja']
            # except KeyError:
            #     title = songinfo['title_localized']['en']
            # artist = songinfo['artist']
            # diffinfo = songinfo['difficulties'][difficulty]
            # 成绩整理
            song_rating = songrating[songid][str(difficulty)]
            score = i['score']
            sp_count = i['shiny_perfect_count']
            p_count = i['perfect_count']
            far_count = i['near_count']
            lost_count = i['miss_count']
            health = i['health']
            modifier = i['modifier']
            play_time = i['time_played']
            best_clear = i['best_clear_type']
            clear = i['clear_type']
            rating = i['rating']
            # 图片整理
            score30 = os.path.join(img, 'b30_score_bg.png')
            rank = os.path.join(rankdir, f'grade_{isrank(score).lower()}.png' if health != -1 else 'grade_f.png')
            songbg = os.path.join(songdir, songid, 'base.jpg')
            diffbg = os.path.join(diffdir, diffdict[str(difficulty)][0].upper() + '.png')
            newbg = os.path.join(img, 'new.png')
            # 底图
            score30_bg = Image.open(score30).convert('RGBA')
            im.alpha_composite(score30_bg, (10 + bg_x, bg_y))
            # 曲图
            song_bg = Image.open(songbg).convert('RGBA').resize((190, 190))
            im.alpha_composite(song_bg, (35 + bg_x, 5 + bg_y))
            # 难度
            diff_bg = Image.open(diffbg).convert('RGBA').resize((72, 72))
            im.alpha_composite(diff_bg, (161 + bg_x, bg_y - 3))
            # rank
            rank_bg = Image.open(rank).convert('RGBA').resize((135, 65))
            im.alpha_composite(rank_bg, (395 + bg_x, 95 + bg_y))
            # songrating
            w_songrating = datatext(187 + bg_x, 12 + bg_y, 20, f'{song_rating:.1f}', Exo_Regular)
            im = draw_text(im, w_songrating)
            # #
            w_rank = datatext(480 + bg_x, bg_y, 45, f'#{num + 1}', Exo_Regular, anchor='lm')
            im = draw_text(im, w_rank)
            # 分数
            w_score = datatext(235 + bg_x, 15 + bg_y, 55, f'{score:,}', GeosansLight)
            im = draw_text(im, w_score)
            # PURE 
            w_PURE = datatext(235 + bg_x, 75 + bg_y, 30, 'PURE', GeosansLight)
            im = draw_text(im, w_PURE)
            w_p_count = datatext(335 + bg_x, 75 + bg_y, 30, p_count, GeosansLight)
            im = draw_text(im, w_p_count)
            w_sp_count = datatext(400 + bg_x, 75 + bg_y, 20, f'+{sp_count}', GeosansLight)
            im = draw_text(im, w_sp_count)
            # FAR
            w_FAR = datatext(235 + bg_x, 105 + bg_y, 30, 'FAR', GeosansLight)
            im = draw_text(im, w_FAR)
            w_far_count = datatext(335 + bg_x, 105 + bg_y, 30, far_count, GeosansLight)
            im = draw_text(im, w_far_count)
            # LOST
            w_LOST = datatext(235 + bg_x, 135 + bg_y, 30, 'LOST', GeosansLight)
            im = draw_text(im, w_LOST)
            w_lost_count = datatext(335 + bg_x, 135 + bg_y, 30, lost_count, GeosansLight)
            im = draw_text(im, w_lost_count)
            # Rating
            w_Rating = datatext(235 + bg_x, 170 + bg_y, 30, 'Rating:', GeosansLight)
            im = draw_text(im, w_Rating)
            w_u_rating = datatext(335 + bg_x, 170 + bg_y, 30, f'{rating:.3f}', GeosansLight)
            im = draw_text(im, w_u_rating)
            # time
            game_time = playtime(play_time)
            w_time = datatext(280 + bg_x, 210 + bg_y, 30, game_time, Exo_Regular, anchor='mm')
            im = draw_text(im, w_time)
            # new
            if timediff(play_time) <= 7:
                new_bg = Image.open(newbg).convert('RGBA')
                im.alpha_composite(new_bg, (bg_x - 23, bg_y))

        # save
        outputiamge_path = os.path.join(img, 'out', f'{arcid}.png')
        im.save(outputiamge_path)
        msg = f'[CQ:image,file=file:///{outputiamge_path}]'
        return msg
    except Exception as e:
        hoshino.logger.error(e)
        return f'Error {type(e)}'

async def draw_score(project, arcid, diff=2, **kwargs):
    '''
    project：    可传入字符串`recent`, `bp`, `score` \n
    arcid：      查询9位数好友码 \n
    diff:        难度，默认为`ftr` \n
    **kwargs：   根据`project`带入参数
      - `recent` : 无
      - `bp` :     下标`limit`，类型为整形数字
      - `score` :  下标`song`，曲名类型为字符串
    '''
    try:
        if project == 'recent':
            info = await get_api_info(project, arcid)
            if info['status'] != 0:
                return '查询错误'
            elif isinstance(info, str):
                return info
            scoreinfo = info['content']['recent_score'][0]
            arcname = info['content']['name']
            songid = scoreinfo['song_id']
        elif project == 'bp':
            info = await get_api_info(project, arcid, limit=kwargs['limit'])
            if info['status'] != 0:
                return '查询错误'
            elif isinstance(info, str):
                return info
            scoreinfo = info['content']
            songid = scoreinfo['song_id']
        elif project == 'score':
            info = await get_api_info(project, arcid, diff, song=kwargs['song'])
            if info['status'] != 0:
                return '查询错误'
            elif isinstance(info, str):
                return info
            scoreinfo = info['content']
            songid = kwargs['song']
        else:
            raise 'Project Error'
        # 获取用户名
        asql = arcsql()
        result = asql.get_user_all(arcid)
        if not result:
            istrue = await bindinfo(0, arcid, True)
            if istrue:
                result = asql.get_user_all(arcid)
        arcname = result[0][1] if result else arcname
        # 歌曲信息
        getsonginfo = await get_api_info('song', song=songid)
        if getsonginfo['status'] == -1:
            return '未找到该曲目，请确认曲名'
        songinfo = getsonginfo['content']
        title = songinfo['title_localized']['en'] if len(songinfo['title_localized']) == 1 else songinfo['title_localized']['ja']
        artist = songinfo['artist']
        diffinfo = songinfo['difficulties'][diff]
        songrating = diffinfo['ratingReal']
        # 整理赋值
        difficulty = scoreinfo['difficulty']
        score = scoreinfo['score']
        sp_count = scoreinfo['shiny_perfect_count']
        p_count = scoreinfo['perfect_count']
        far_count = scoreinfo['near_count']
        miss_count = scoreinfo['miss_count']
        health = scoreinfo['health']
        modifier = scoreinfo['modifier']
        play_time = scoreinfo['time_played']
        best_clear = scoreinfo['best_clear_type']
        clear = scoreinfo['clear_type']
        rating = scoreinfo['rating']

        msg = f'''
Player: {arcname}
Code: {arcid}
Play Time: {playtime(play_time)}
---------------------------------
Song: {title}
Artist: {artist}
Difficulty: {diffdict[str(diff)][0].upper()} | SongRating: {songrating}
---------------------------------
Score: {score:,}
Rank: {'F' if health == -1 else isrank(score)}
Pure: {p_count} (+{sp_count})
Far: {far_count}
Lost: {miss_count}
Rating: {rating:.2f}'''
        return msg
    except Exception as e:
        hoshino.logger.error(e)
        return f'Error {type(e)}'

async def bindinfo(qqid, arcid, temp=False):
    asql = arcsql()
    info = await get_api_info('bind', arcid)
    if info['status'] == -6:
        return '未查询到该玩家'
    elif isinstance(info, str):
        return info
    arcid = info['content']['code']
    arcname = info['content']['name']
    asql.insert_user(qqid, arcid, arcname)
    if temp:
        return True
    return f'用户 {arcname} 已成功绑定QQ {qqid}'
