import asyncio
import os
import time

from back_progress.utils.add_back import add_back
from back_progress.utils.config import tesst_dir_data, txt_url_path
from back_progress.utils.qm.pachong import pachong
from back_progress.utils.txt2voice import text2audio
from utils.utils.TimeUtils import time_to_time_length


class CreateByUrlFile:
    def __init__(self, txt_url_path, saveBookPath, saveAudioPath, saveBgmPath, voice, background_music,
                 background_volume_reduction=10,
                 encoding="utf-8",
                 title_pattern=r"第[一二三四五六七八九十1234567890]+章 \S+"):
        self.txt_url_path = txt_url_path
        self.title_pattern = title_pattern
        print("小说网址：", self.txt_url_path)
        print("标题正则表达式：", self.title_pattern)
        self.voice = voice
        print("语音：", self.voice)
        self.background_music = background_music
        print("背景音乐：", self.background_music)
        self.background_volume_reduction = background_volume_reduction
        print("背景音量：", self.background_volume_reduction)
        self.encoding = encoding
        print("编码：", self.encoding)
        self.saveAudioPath = saveAudioPath
        self.saveBgmPath = saveBgmPath
        self.saveBookPath = saveBookPath

        self.book_name = os.path.basename(self.txt_url_path).split(".")[0]
        print("书名：", self.book_name)
        self.saveAudioPath = os.path.join(self.saveAudioPath, self.book_name)
        print("音频保存路径：", self.saveAudioPath)
        self.saveBookPath = os.path.join(self.saveBookPath, self.book_name)
        print("书籍保存路径：", self.saveBookPath)
        self.saveBgmPath = os.path.join(self.saveBgmPath, self.book_name)
        print("背景音乐保存路径：", self.saveBgmPath)
        if not os.path.exists(self.saveAudioPath):
            os.makedirs(self.saveAudioPath)
        if not os.path.exists(self.saveBgmPath):
            os.makedirs(self.saveBgmPath)
        if not os.path.exists(self.saveBookPath):
            os.makedirs(self.saveBookPath)

    # 读取整个文件
    async def get_whole_file(self):
        return await pachong(self.txt_url_path, self.saveBookPath)
        # 读取一个目录下的所有文件

    async def get_all_file(self, books):
        print("读取中...")
        chapters = []
        for book in books:
            book_path = os.path.join(self.saveBookPath, book["path"])
            with open(book_path, "r", encoding=self.encoding) as f:
                content = f.read()
                chapters.append({book["name"], content})
        print("读取完成")
        return chapters

    # 按照章分割
    async def split_by_chapter(self):
        print("爬取...")
        books = await  self.get_whole_file()
        print("爬取完成")
        print("读取中...")
        chapters = await self.get_all_file(books)
        print("读取完成")
        print(self.book_name, "分割结果如下：", len(chapters), "章")

        print("--------------------------------------")
        return chapters

    # 阅读一章小说
    async def read_one_chapter(self, title, content):
        savePath = os.path.join(self.saveAudioPath, f"{title}.mp3")
        data = content, savePath, self.voice
        await text2audio(data)
        return savePath, title

    # 给一章小说加背景音
    def add_bg_music(self, from_path, title, background_music, background_volume_reduction):
        to_path = os.path.join(self.saveBgmPath, f"{title}.mp3")
        data = from_path, to_path, background_music, background_volume_reduction
        add_back(data)
        return data

    # 一步方法

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

            # 计算进度
            progress = processedChapters / totalChapters
            estimatedTotalTime = countTime / progress
            remainingTime = estimatedTotalTime - countTime

            print(f"{title} 完成", f"耗时：{time_to_time_length(allTme)} ", "预计总耗时：",
                  f"{time_to_time_length(estimatedTotalTime)} ",
                  f"还得{time_to_time_length(remainingTime)} ")
            print("--------------------------------------")

        bookEnd = time.time()
        print(f"{self.book_name} 合成完成", f"耗时：{time_to_time_length(bookEnd - bookStart)} ")


async def main():
    root = tesst_dir_data
    background_music = os.path.join(root, "fzg.mp3")
    saveBookPath = os.path.join(root, "txt")
    saveAudioPath = os.path.join(root, "audio")
    saveBgmPath = os.path.join(root, "bgm")
    voice = "zh-CN-YunxiNeural"
    creater = CreateByUrlFile(txt_url_path, saveBookPath, saveAudioPath, saveBgmPath, voice, background_music,
                              encoding="utf-8")
    await creater.forward()


if __name__ == '__main__':
    asyncio.run(main())
