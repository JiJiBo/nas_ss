import os
import time
import uuid

from asgiref.sync import sync_to_async

from back_progress.utils.add_back import add_back
from back_progress.utils.ftp_client import get_def_ftp_client
from back_progress.utils.txt2voice import text2audio
from my_sql_db.models import SmallSay, Books
from my_sql_db.utils.utils import haveThisBookTitle, saveBookMsg
from utils.utils.TimeUtils import time_to_time_length


class CreateAudioBookBase:
    def __init__(self, book_id, saveBookPath, saveAudioPath, saveBgmPath, voice, background_music,
                 background_volume_reduction=10, encoding="utf-8", is_to_ftp=True):
        self.book_id = book_id
        self.voice = voice
        self.background_music = background_music
        self.background_volume_reduction = background_volume_reduction
        self.encoding = encoding
        self.saveAudioPath = saveAudioPath
        self.saveBgmPath = saveBgmPath
        self.saveBookPath = saveBookPath
        self.is_to_ftp = is_to_ftp
        self.book_name = None  # 初始化 book_name 属性
        self.type = "base"

    def del_all_files(self):
        if self.type == "link":
            for root, dirs, files in os.walk(self.saveBookPath):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
        elif self.type == "path":
            os.remove(self.saveBookPath)
        for root, dirs, files in os.walk(self.saveAudioPath):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
        for root, dirs, files in os.walk(self.saveBgmPath):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
        print("删除文件夹中的所有文件")

    async def get_whole_file(self):
        raise NotImplementedError("This method should be overridden in subclasses")

    async def get_all_file(self, books):
        print("读取中...")
        chapters = []
        for book in books:
            book_path = book["path"]
            with open(book_path, "r", encoding=self.encoding) as f:
                content = f.read()
                chapters.append([book["name"], content])
        print("读取完成")
        return chapters

    async def split_by_chapter(self):
        raise NotImplementedError("This method should be overridden in subclasses")

    async def read_one_chapter(self, title, content, page):
        if not os.path.exists(self.saveAudioPath):
            os.makedirs(self.saveAudioPath)
        savePath = os.path.join(self.saveAudioPath, f"{title}.mp3")
        if await self.is_had_ftp(title, 2) or await self.is_had_ftp(title, 5):
            print("已经转换过该章节")
            if self.check_file(savePath):
                return savePath, title
            else:
                print("文件已损坏，重新转换")
        if os.path.exists(savePath):
            print("文件已存在，删除重新转换")
            await  self.delect_a_conver_history(title, page)
            os.remove(savePath)
        data = content, savePath, self.voice
        await text2audio(data)
        remote_file = self.merge_audio(savePath)
        if remote_file:
            await self.save_convert_history(title, page, remote_file)
        return savePath, title

    def merge_audio(self, audio_files):
        if self.is_to_ftp:
            print("文件转移到FTP服务器")
            timeStr = time.strftime("%Y%m%d", time.localtime())
            timeStr = os.path.join(timeStr, time.strftime("%H", time.localtime()))
            ftp_client = get_def_ftp_client()
            ftp_client.connect()
            remote_file = ftp_client.upload_file(audio_files, timeStr)
            ftp_client.disconnect()
            return remote_file
        else:
            print("文件并不会转移")
            return None

    async def is_had_ftp(self, title, get_step):
        res = await haveThisBookTitle((self.small_say, title, get_step))
        return res

    # 保存章节转换记录
    async def save_chapter_history(self, path, get_step, name, page, dir):
        man_uuid = str(uuid.uuid4())
        data = path, self.small_say, get_step, dir, name, man_uuid, page
        return await saveBookMsg(data)

    # 保存语音转换进度
    async def save_convert_history(self, name, page, path):
        print("保存语音转换进度", name)
        return await self.save_chapter_history(path, 2, name, page, self.saveAudioPath)

    async def delect_a_bgm_history(self, name, page):
        await  self.delect_a_history(name, page, 5)

    async def delect_a_conver_history(self, name, page):
        await self.delect_a_history(name, page, 2)

    @sync_to_async
    def delect_a_history(self, name, page, get_step):
        Books.objects.filter(book_id=self.book_id, get_step=get_step, name=name, page=page).delete()

    # 保存下载进度
    async def save_download_history(self, name, page, path):
        print("保存下载进度", name)
        return await self.save_chapter_history(path, 1, name, page, self.saveAudioPath)

    # 保存背景音转换进度
    async def save_bgm_history(self, name, page, path):
        print("保存背景音转换进度", name)
        return await self.save_chapter_history(path, 5, name, page, self.saveBgmPath)

    @sync_to_async
    def get_small_say(self):
        return SmallSay.objects.get(id=self.book_id)

    async def add_bg_music(self, from_path, title, background_music, background_volume_reduction, page):
        if not os.path.exists(self.saveBgmPath):
            os.makedirs(self.saveBgmPath)
        to_path = os.path.join(self.saveBgmPath, f"{title}.mp3")
        if await self.is_had_ftp(title, 5) and self.check_file(to_path):
            print("该章节已经加了背景音")
            return None
        if os.path.exists(to_path):
            print("文件已存在，删除重新转换")
            await self.delect_a_bgm_history(title, page)
            os.remove(to_path)
        data = from_path, to_path, background_music, background_volume_reduction
        add_back(data)
        remote_file = self.merge_audio(to_path)
        if remote_file:
            await self.save_bgm_history(title, page, remote_file)
        return data

    # 检查文件完整性
    def check_file(self, filepath):
        if not os.path.exists(filepath):
            print(f"文件 {filepath} 不存在")
            return False
        if os.path.getsize(filepath) == 0:
            print(f"文件 {filepath} 为空")
            return False
        return True

    async def forward(self):
        self.small_say = await self.get_small_say()
        self.book_name = self.small_say.name
        chapters = await self.split_by_chapter()
        print("--------------------------------------")
        print("开始合成...")
        bookStart = time.time()
        countTime = 0
        totalChapters = len(chapters)
        await self.saveMaxProgress(totalChapters)
        await self.saveName(self.book_name)
        processedChapters = 0
        page = 0
        for title, content in chapters:

            if len(content) == 0:
                totalChapters -= 1
                processedChapters -= 1
                print(f"跳过 {title}，没有内容")
                continue
            page += 1
            print(f"正在合成 {title}", "总字数", len(content))
            startTimme = time.time()
            savePath, title = await self.read_one_chapter(title, content, page)
            readTme = time.time() - startTimme
            print(f"{title} 阅读完成", f"耗时：{time_to_time_length(readTme)} ")
            print(f"{title} 开始加背景音...")
            bgTme = time.time()
            await self.add_bg_music(savePath, title, self.background_music, self.background_volume_reduction, page)
            bgTme = time.time() - bgTme
            print(f"{title} 加背景音完成", f"耗时：{time_to_time_length(bgTme)} ")
            allTme = time.time() - startTimme
            countTime += allTme
            processedChapters += 1

            progress = processedChapters / totalChapters
            estimatedTotalTime = countTime / progress
            remainingTime = estimatedTotalTime - countTime

            print(f"{title} 完成", f"耗时：{time_to_time_length(allTme)} ", "预计总耗时：",
                  f"{time_to_time_length(estimatedTotalTime)} ",
                  f"还得{time_to_time_length(remainingTime)} ")
            print("--------------------------------------")

        bookEnd = time.time()
        if self.is_to_ftp:
            self.del_all_files()
        print(f"{self.book_name} 合成完成", f"耗时：{time_to_time_length(bookEnd - bookStart)} ")

    @sync_to_async
    def saveMaxProgress(self, chapters):
        self.small_say.download_max = chapters
        self.small_say.add_back_max = chapters
        self.small_say.conversion_max = chapters
        self.small_say.save()

    @sync_to_async
    def saveName(self, name):
        self.small_say.name = name
        self.small_say.save()
