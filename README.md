# Arcaea

基于HoshinoBotV2的Arcaea查询插件
项目地址：https://github.com/Yuri-YuzuChaN/Arcaea

# 使用方法

1. 搭建API服务器，[BotArcAPI](https://github.com/TheSnowfield/BotArcAPI)
2. 将该项目放在HoshinoBot插件目录 `modules` 下，或者clone本项目 `git clone https://github.com/Yuri-YuzuChaN/Arcaea`
3. 在`config/__bot__.py`模块列表中添加`Arcaea`

# 指令

| 指令              | 功能     | 可选参数              | 说明                            |
| :---------------- | :------- | :-------------------- | :------------------------------ |
| arcinfo           | 查询b30  | 无                    | 查询b30成绩                     |
|                   |          | [@QQID]               | 查询群友的b30成绩               |
|                   |          | [arcid]              | 查询TA人b30成绩                 |
| arcrecent / arcre | 查询最近 | 无                    | 查询最近一次游玩成绩            |
|                   |          | [@QQID]               | 查询群友最近一次游玩成绩        |
|                   |          | [arcid]              | 查询TA人最近一次游玩成绩        |
| arcscore          | 查询成绩 | [song]                | 查询游玩该曲的成绩，默认查询FTR |
|                   |          | [song] [diff]         | 查询游玩该曲其它难度的成绩      |
|                   |          | [@QQID] [song]            | 查询群友游玩该曲的成绩          |
|                   |          | [@QQID] [song] [diff]     | 查询群友游玩该曲其它难度的成绩  |
|                   |          | [arcid] [song]        | 查询TA人游玩该曲的成绩          |
|                   |          | [arcid] [song] [diff] | 查询TA人游玩该曲其它难度的成绩  |
| arcbind           | 绑定     | [arcid]               | 绑定用户                        |
| arcun             | 解绑     | 无                    | 解除绑定                        |

# 问题

1. 在查询b30的时候，如果是第一次使用该指令，需要等待2-3分钟的时间
