from pydub import AudioSegment


# 给音频文件加背景音乐
def add_back(data):
    # 获取 来源的音频路径、背景音乐文件路径、背景音乐音量降低的大小，保存路径
    from_path, to_path, background_music, background_volume_reduction = data
    original_audio = AudioSegment.from_mp3(from_path)
    background_music = AudioSegment.from_mp3(background_music)
    # 调整背景音乐的音量
    reduced_background_music = background_music - background_volume_reduction

    if len(original_audio) > len(reduced_background_music):
        reduced_background_music = reduced_background_music * (1 + len(original_audio) // len(reduced_background_music))
    else:
        reduced_background_music = reduced_background_music[:len(original_audio)]

        # 将调整后的背景音乐与原始音频叠加
    new_audio = original_audio.overlay(reduced_background_music)
    # 导出结果
    new_audio.export(to_path, format="mp3", codec="libmp3lame")
