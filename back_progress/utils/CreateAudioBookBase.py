import os
import time

from back_progress.utils.add_back import add_back
from back_progress.utils.txt2voice import text2audio
from utils.utils.TimeUtils import time_to_time_length



class CreateAudioBookBase:
    def __init__(self, saveBookPath, saveAudioPath, saveBgmPath, voice, background_music,
                 background_volume_reduction=10, encoding="utf-8"):
        self.voice = voice
        self.background_music = background_music
        self.background_volume_reduction = background_volume_reduction
        self.encoding = encoding
        self.saveAudioPath = saveAudioPath
        self.saveBgmPath = saveBgmPath
        self.saveBookPath = saveBookPath
        self.book_name = None  # 初始化 book_name 属性

    async def get_whole_file(self):
        raise NotImplementedError("This method should be overridden in subclasses")

    async def get_all_file(self, books):
        print("读取中...")
        chapters = []
        for book in books:
            book_path = os.path.join(self.saveBookPath, book["path"])
            with open(book_path, "r", encoding=self.encoding) as f:
                content = f.read()
                chapters.append([book["name"], content])
        print("读取完成")
        return chapters

    async def split_by_chapter(self):
        raise NotImplementedError("This method should be overridden in subclasses")

    async def read_one_chapter(self, title, content):
        savePath = os.path.join(self.saveAudioPath, f"{title}.mp3")
        data = content, savePath, self.voice
        await text2audio(data)
        return savePath, title

    def add_bg_music(self, from_path, title, background_music, background_volume_reduction):
        to_path = os.path.join(self.saveBgmPath, f"{title}.mp3")
        data = from_path, to_path, background_music, background_volume_reduction
        add_back(data)
        return data

    async def forward(self):
        chapters = await self.split_by_chapter()
        print("--------------------------------------")
        print("开始合成...")
        bookStart = time.time()
        countTime = 0
        totalChapters = len(chapters)
        processedChapters = 0

        for title, content in chapters:
            print(f"正在合成 {title}")
            startTimme = time.time()
            savePath, title = await self.read_one_chapter(title, content)
            readTme = time.time() - startTimme
            print(f"{title} 阅读完成", f"耗时：{time_to_time_length(readTme)} ")
            print(f"{title} 开始加背景音...")
            bgTme = time.time()
            self.add_bg_music(savePath, title, self.background_music, self.background_volume_reduction)
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
        print(f"{self.book_name} 合成完成", f"耗时：{time_to_time_length(bookEnd - bookStart)} ")
