import os

import edge_tts


# 文字转语音
async def text2audio(data):
    # 获取文本、保存路径、音色
    text, savePath, voice = data
    if os.path.exists(savePath):
        print(f"{savePath}已存在")
        return
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(savePath)
