import asyncio
import os

from back_progress.utils.CreateAudioBookBase import CreateAudioBookBase
from back_progress.utils.config import tesst_dir_data, txt_url_path
from back_progress.utils.qm.pachong import pachong


class CreateByUrlFile(CreateAudioBookBase):
    def __init__(self, book_id, txt_url_path, saveBookPath, saveAudioPath, saveBgmPath, voice, background_music,
                 background_volume_reduction=10, encoding="utf-8", engine="qm"):
        super().__init__(book_id, saveBookPath, saveAudioPath, saveBgmPath, voice, background_music,
                         background_volume_reduction, encoding)
        self.txt_url_path = txt_url_path
        print("下载地址：", txt_url_path)
        self.engine = engine
        self.type = "link"

    async def get_whole_file(self):
        if self.engine == "qm":
            return await pachong(self, self.txt_url_path, self.saveBookPath)
        return await pachong(self, self.txt_url_path, self.saveBookPath)

    async def split_by_chapter(self):
        print("爬取...")
        books, title = await self.get_whole_file()
        self.book_name = title
        self.saveAudioPath = os.path.join(self.saveAudioPath, self.book_name)
        print("音频保存路径：", self.saveAudioPath)
        self.saveBookPath = os.path.join(self.saveBookPath, self.book_name)
        print("书籍保存路径：", self.saveBookPath)
        self.saveBgmPath = os.path.join(self.saveBgmPath, self.book_name)
        print("背景音乐保存路径：", self.saveBgmPath)
        os.makedirs(self.saveAudioPath, exist_ok=True)
        os.makedirs(self.saveBgmPath, exist_ok=True)
        os.makedirs(self.saveBookPath, exist_ok=True)
        print("爬取完成")
        print("读取中...")
        chapters = await self.get_all_file(books)
        print("读取完成")
        print(self.book_name, "分割结果如下：", len(chapters), "章")

        print("--------------------------------------")

        return chapters


async def main():
    root = tesst_dir_data
    background_music = os.path.join(root, "fzg.mp3")
    saveBookPath = os.path.join(root, "txt")
    saveAudioPath = os.path.join(root, "audio")
    saveBgmPath = os.path.join(root, "bgm")
    voice = "zh-CN-YunxiNeural"
    creater = CreateByUrlFile(1, txt_url_path, saveBookPath, saveAudioPath, saveBgmPath, voice, background_music,
                              encoding="utf-8")
    await creater.forward()


if __name__ == '__main__':
    asyncio.run(main())
