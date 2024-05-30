import re


# 根据标题分割txt小说文件，并保留标题。
# 返回一个字典，key为标题，value为小说内容
def split_txt(txt_content, title_pattern=r"第[一二三四五六七八九十1234567890]+章 \S+"):
    # 使用正则表达式找到所有的标题
    titles = re.findall(title_pattern, txt_content)
    if not titles:
        return {}

    # 使用正则表达式分割内容，保留分隔符（标题）
    parts = re.split(f'({title_pattern})', txt_content)

    # 初始化字典
    novel_dict = []

    # 遍历分割后的部分，跳过第一个元素，因为它是在第一个标题之前的内容
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        novel_dict .append([title,content])

    return novel_dict


if __name__ == '__main__':
    # 示例使用
    txt_content = """
    第一章 开始
    这是第一章的内容。

    第二章 继续
    这是第二章的内容。
    
    
    
    第411章 继续
    这是第411章的内容。
    """

    result = split_txt(txt_content)
    for title, content in result.items():
        print(f"{title}: {content}")
