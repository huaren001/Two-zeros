# Two-zeros
# 项目介绍
本项目把chatpgt接入QQ，实现在QQ中和通义千问群聊或私聊。

项目基于go-cqhttp和chatgpt 的 api，部署本项目前请先部署好go-cqhttp，并获得gpt的api-key。

go-cqhttp项目地址：[go-cqhttp]([https://github.com/Mrs4s/go-cqhttp](https://github.com/huaren001/Two-zeros))


# 项目使用
1. ``main.py``中第七行的"bnt_qq=  "改为自己的机器人QQ号
2. ``mst.py``中第三行改为自己的api密钥
3. 运行go-cqhttp
4. 运行main.py
