import edge_tts


# 文字转语音
async def text2audio(data):
    # 获取文本、保存路径、音色
    text, savePath, voice = data
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(savePath)
