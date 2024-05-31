import re

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

if __name__ == '__main__':
    # 示例使用
    txt_content = """
这里是前言，可能提到第一章的内容。
第1章 章节开始
这是一段内容，提到了第二章的一个事件。
第二章 另一个章节
这是正文，其中提到了“当我们来到第3章的时候”。
第三章 最后一个章节
哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈

哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈
"""

    result = split_txt(txt_content)
    for title, content in result:
        print(f"{title}   --   {content}")
        print("-----")
