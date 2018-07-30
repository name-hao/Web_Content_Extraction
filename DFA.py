class Node(object):
    def __init__(self):
        self.children = None
        self.bad_word = None


def add_word(root, word):
    # 开始节点是根节点
    node = root
    # 对每一行的每一个字，开始添加进dfa节点中
    for i in range(len(word)):
        # 如果节点没有子节点，则讲该下标的字添加进子节点中
        if node.children is None:
            node.children = {word[i]: Node()}
        # 如果改行某下标的字不在子节点中，也进行添加
        elif word[i] not in node.children:
            node.children[word[i]] = Node()
        # 否则递进去匹配或者添加
        node = node.children[word[i]]
    # 设置最终匹配到的敏感词是当前词
    node.bad_word = word


def init(file_path):
    # 初始化一个根节点
    root = Node()
    # 打开敏感词文件, 开始添加敏感词
    with open(file_path, 'r', encoding='utf-8') as fp:
        # 处理文件中每一行的敏感词
        for line in fp:
            # 将结尾的换行符舍去，用的是Python的切片操作
            line = line[0:-1]
            # 将该行的单词添加进节点中
            add_word(root, line)
    return root


def clean_html(pre_html, root):
    clean = []
    i = 0
    # 开始匹配原始html文件的每一个字，如果匹配到了某一个字，则接着向后进行匹配整体
    # 敏感词
    while i < len(pre_html):
        # 从根节点开始匹配
        p = root
        # 从当前下标开始匹配
        j = i
        # 当j在原始html中时，p有子节点，当前下标的字在p的子节点中
        while j < len(pre_html) and p.children is not None and pre_html[j] in p.children:
            # 递进下一步
            p = p.children[pre_html[j]]
            j = j + 1
        # 如果匹配到的单词在i到j下标所包括的内容中
        if p.bad_word == pre_html[i:j]:
            # 讲敏感词用原始敏感词个数个*来替代
            clean.append('*'*len(p.bad_word))
            # 跳过敏感词，接着进行处理
            i += len(p.bad_word)

        else:
            clean.append(pre_html[i])
            i += 1
    # 将过滤后的结果进行拼接得到最后的网页
    result = ''.join(clean)
    return result


def dfa_html(pre_html):
    # 读取敏感词列表, 并初始化根节点
    root = init("filtered_words.txt")
    # 结果页面用root的敏感词列表来过滤
    result_html = clean_html(pre_html, root)
    return result_html


if __name__ == '__main__':
    dfa_html()
