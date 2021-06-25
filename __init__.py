from hoshino import Service, priv
from hoshino.typing import CQEvent
import re

from .sql import *
from .api import *
from .draw import *

sv = Service('arcaea', manage_priv=priv.ADMIN, enable_on_default=True, visible=True)
asql = arcsql()

diffdict = {
    '0' : ['pst', 'past'],
    '1' : ['prs', 'present'],
    '2' : ['ftr', 'future'],
    '3' : ['byd', 'beyond']
}

@sv.on_prefix('arcinfo')
async def arcinfo(bot, ev:CQEvent):
    qqid = ev.user_id
    msg = ev.message.extract_plain_text().strip()
    if 'CQ:at' in str(ev.message):
        result = re.search(r'\[CQ:at,qq=(.*)\]', str(ev.message))
        qqid = int(result.group(1))
    result = asql.get_user_id(qqid)
    if not result:
        await bot.finish(ev, '该账号尚未绑定，请输入 arcbind arcid(好友码) 绑定账号', at_sender=True)
    elif msg:
        if msg.isdigit() and len(msg) == 9:
            arcid = msg
        else:
            await bot.finish(ev, '仅可以使用好友码查询', at_sender=True)
    else:
        arcid = result[0][0]
    info = await draw_info(arcid)
    await bot.send(ev, info, at_sender=True)

@sv.on_prefix(['arcre', 'arcrecent'])
async def arcrecent(bot, ev:CQEvent):
    qqid = ev.user_id
    msg = ev.message.extract_plain_text().strip()
    if 'CQ:at' in str(ev.message):
        result = re.search(r'\[CQ:at,qq=(.*)\]', str(ev.message))
        qqid = int(result.group(1))
    result = asql.get_user_id(qqid)
    if not result:
        await bot.finish(ev, '该账号尚未绑定，请输入 arcbind arcid(好友码) 绑定账号', at_sender=True)
    elif msg:
        if msg.isdigit() and len(msg) == 9:
            arcid = msg
        else:
            await bot.finish(ev, '仅可以使用好友码查询', at_sender=True)
    else:
        arcid = result[0][0]
    info = await draw_score('recent', arcid)
    await bot.send(ev, info, at_sender=True)

@sv.on_prefix('arcscore')
async def arcscore(bot, ev:CQEvent):
    qqid = ev.user_id
    diff = 2
    msg = ev.message.extract_plain_text().strip().split()
    while '' in msg:
        msg.remove('')
    if not msg:
        await bot.finish(ev, '请输入曲名', at_sender=True)
    elif 'CQ:at' in str(ev.message):
        result = re.search(r'\[CQ:at,qq=(.*)\]', str(ev.message))
        qqid = int(result.group(1))
    result = asql.get_user_id(qqid)
    if len(msg) >= 2:
        if msg[0].isdigit() and len(msg[0]) == 9:
            arcid = msg[0]
            del msg[0]
        elif result:
            arcid = result[0][0]
        else:
            await bot.finish(ev, '该账号尚未绑定，请输入 arcbind arcid(好友码) 绑定账号', at_sender=True)
        for num in diffdict:
            if msg[-1].lower() in diffdict[num]:
                diff = int(num)
                del msg[-1]
                break
            elif msg[-1] == num:
                diff = int(num)
                del msg[-1]
                break
        song = ' '.join(msg)
    elif result:
        arcid = result[0][0]
        song = msg[0]
    else:
        await bot.finish(ev, '该账号尚未绑定，请输入 arcbind arcid(好友码) 绑定账号', at_sender=True)
    if not song:
        await bot.finish(ev, '请输入曲名', at_sender=True)

    info = await draw_score('score', arcid, diff, song=song)
    await bot.send(ev, info, at_sender=True)

@sv.on_prefix('arcbp')
async def arcbp(bot, ev:CQEvent):
    qqid = ev.user_id
    msg = ev.message.extract_plain_text().strip().split()
    while '' in msg:
        msg.remove('')
    if not msg:
        await bot.finish(ev, '请输入参数', at_sender=True)
    elif 'CQ:at' in str(ev.message):
        result = re.search(r'\[CQ:at,qq=(.*)\]', str(ev.message))
        qqid = int(result.group(1))
    result = asql.get_user_id(qqid)

@sv.on_prefix('arcbind')
async def bind(bot, ev:CQEvent):
    qqid = ev.user_id
    arcid = ev.message.extract_plain_text().strip()
    if not arcid:
        await bot.finish(ev, '请输入您的 arcid(好友码)', at_sender=True)
    result = asql.get_user_id(qqid)
    if result:
        await bot.finish(ev, '您已绑定，如需要解绑请输入arcun', at_sender=True)
    msg = await bindinfo(qqid, arcid)
    await bot.send(ev, msg, at_sender=True)

@sv.on_fullmatch('arcun')
async def unbind(bot, ev:CQEvent):
    qqid = ev.user_id
    result = asql.get_user_id(qqid)
    if result:
        if asql.delete_user(qqid):
            msg = '解绑成功'
        else:
            msg = '数据库错误'
    else:
        msg = '您未绑定，无需解绑'
    await bot.send(ev, msg, at_sender=True)
