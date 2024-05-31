# 导入必要的模块
import re
import os
import threading
import time

from requests import Timeout
from tqdm import tqdm
from colorama import Fore, Style, init

from back_progress.utils.qm import the_public
from back_progress.utils.qm.the_public import rename

init(autoreset=True)


# 定义分章节保存模式用来下载7猫小说的函数
async def pachong(utils, url, book_folder, encoding="utf-8", start_chapter_id="0"):
    book_id = re.search(r"/(\d+)/", url).group(1)

    # 调用异步函数获取7猫信息（模拟浏览器）
    try:
        title, introduction, chapters = the_public.get_book_info(url)
    except Timeout:
        print(Fore.RED + Style.BRIGHT + "连接超时，请检查网络连接是否正常。")
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"发生异常: \n{e}")
        return
    # 获取保存路径
    # 创建保存文件夹
    book_folder = os.path.join(book_folder, title)
    os.makedirs(book_folder, exist_ok=True)

    # 转换简介内容格式
    introduction_data = introduction.encode(encoding, errors='ignore')

    # 定义简介路径
    introduction_use = False
    introduction_path = None

    # 检查用户是否指定起始章节
    start_index = 0
    if start_chapter_id == '0':
        pass
    else:
        # 找到起始章节的索引
        for i, chapter in enumerate(chapters):
            chapter_id_tmp = chapter["id"]
            if chapter_id_tmp == start_chapter_id:  # 将 开始索引设置为用户的值
                start_index = i

    page = 0
    lock = threading.Lock()
    books = []
    await utils.saveMaxProgress(len(chapters))
    await utils.saveName(title)
    for chapter in chapters[start_index:]:
        lock.acquire()
        try:
            page += 1

            chapter_title = chapter["title"]
            chapter_title = rename(chapter_title)
            file_path = os.path.join(book_folder, f"{chapter_title}.txt")
            if os.path.exists(file_path):
                print(f"{chapter_title} 已存在")
                books.append({"name": chapter_title, "path": file_path})
                continue
            time.sleep(0.25)
            result = the_public.get_api(book_id, chapter)

            if result == "skip":
                continue
            elif result == "terminate":
                break
            else:
                chapter_title, chapter_text, _ = result
            # 在章节内容字符串中添加章节标题和内容
            content_all = f"{chapter_title}\n{chapter_text}"

            # 转换章节内容格式
            data = content_all.encode(encoding, errors='ignore')

            # 重置file_path
            # noinspection PyUnusedLocal

            if introduction_use is False:
                introduction_path = os.path.join(book_folder, "简介.txt")

            if introduction_use is False:
                with open(introduction_path, "wb") as f:
                    f.write(introduction_data)
                tqdm.write("简介已保存")
                # 将简介保存标记为已完成
                introduction_use = True

            with open(file_path, "wb") as f:
                f.write(data)
            print(f"{chapter_title} 已保存")
            books.append({"name": chapter_title, "path": file_path})
            await utils.save_download_history(chapter_title, page, file_path)
        except Exception:
            print(f"处理失败")
        finally:
            lock.release()
    return books, title
