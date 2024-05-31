import asyncio
import os

from celery import shared_task

from back_progress.utils.create__by_txt_file import CreateByTxtFile
from back_progress.utils.create__by_url_file import CreateByUrlFile
from back_progress.utils.split_txt import detect_file_encoding
from my_sql_db.utils.utils import get_small_say
from nas_ss.celery import app


@app.task(time_limit=36000)
def download_novel_in_thread(nid):
    print("download_novel_in_thread")
    asyncio.run(download_novel(nid))


async def download_novel(id):
    # print(id)
    small_say = await get_small_say(id)
    small_say.download_progress = 0
    small_say.save()
    root = "./data"
    background_music = small_say.background_music
    saveBookPath = os.path.join(root, "txt")
    saveAudioPath = os.path.join(root, "audio")
    saveBgmPath = os.path.join(root, "bgm")
    voice = small_say.voice
    if small_say.type == "link":

        link = small_say.link
        creater = CreateByUrlFile(id, link, saveBookPath, saveAudioPath, saveBgmPath, voice, background_music,
                                  encoding="utf-8")
        await creater.forward()
    elif small_say.type == "path":
        path = small_say.path
        creater = CreateByTxtFile(id, path, saveAudioPath, saveBgmPath, voice, background_music,
                                  encoding=detect_file_encoding(path))
        await creater.forward()
