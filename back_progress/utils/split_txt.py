import re

import chardet


def split_txt(text, title_pattern=r'(\n\s*第\s*[\d一二三四五六七八九十百千万]+\s*章.*)'):
    # 使用re.split方法来分割文本，保留括号内的分割模式作为分割结果的一部分
    # 正则表达式已更新，以包括中文数字
    parts = re.split(title_pattern, text, flags=re.MULTILINE)

    # 由于re.split会在每个匹配的章节标题前后分割文本，第一部分通常是前言或引言
    # 为避免数组越界错误，需要检查parts数组的长度
    if len(parts) < 3:
        return []  # 如果没有章节或格式不正确，返回空列表

    # 首部不属于任何章节的内容，可以单独处理或丢弃
    # parts列表中，奇数索引为章节标题，偶数索引为对应的内容
    return [(parts[i].strip(), parts[i + 1].strip()) for i in range(1, len(parts), 2)]


def detect_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    return chardet.detect(raw_data)['encoding']


if __name__ == '__main__':
    # 示例使用
    txt_content = ""
    path = r'C:\Users\Nas\Downloads\ '
    with open(path, 'r', encoding=detect_file_encoding(path)) as f:
        txt_content = f.read()

    # 假设txt_content是一个包含章节标题和内容的字符串

    result = split_txt(txt_content)
    print(len(result))
    for title, content in result[:400]:
        if len(content) == 0:
            continue
        print(f"{title} --  ")
        print("-----")
