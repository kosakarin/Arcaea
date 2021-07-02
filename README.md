# 616已更新api，BotArcApi作者已删档跑路，项目暂停更新，仅能查询Recent

# Arcaea

基于HoshinoBotV2的Arcaea查询插件，所有文件适用于游戏版本 3.6.4

项目地址：https://github.com/Yuri-YuzuChaN/Arcaea

# 使用方法

1. 将该项目放在HoshinoBot插件目录 `modules` 下，或者clone本项目 `git clone https://github.com/Yuri-YuzuChaN/Arcaea`
2. 在`config/__bot__.py`模块列表中添加`Arcaea`
3. 在数据库`arcaea.db`中`LOGIN`表添加查询用账号密码以及绑定ID（随意数字）
 
# 另外

1. 后续游戏版本更新需自行修改数据库文件`arcsong.db`添加曲目，`img/song`的曲目图片
2. 每次添加完好友必须使用一次`arcup`指令

# 指令

| 指令              | 功能     | 可选参数              | 说明                            |
| :---------------- | :------- | :-------------------- | :------------------------------ |
| arcrecent / arcre | 查询最近 | 无                     | 查询最近一次游玩成绩            |
| arcup | 账号绑定 | 无               | 查询用账号添加完好友，使用该指令绑定查询账号，添加成功即可使用`arcre`指令|
| arcbind           | 绑定     | [arcid] [arcname]     | 绑定用户                        |
| arcun             | 解绑     | 无                    | 解除绑定                        |
