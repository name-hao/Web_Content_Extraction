# coding:utf-8
import re
import requests


def remove_js_css(pre_html):
    # 正则表达式,编译去掉script标签的内容
    r = re.compile(r'''<script.*?</script>''', re.I | re.M | re.S)
    clean_html = r.sub('', pre_html)
    # 编译去掉<style></style>标签中的内容
    r = re.compile(r'''<style.*?</style>''', re.I | re.M | re.S)
    clean_html = r.sub('', clean_html)
    # 编译去掉注释掉的内容
    r = re.compile(r'''<!--.*?-->''', re.I | re.M | re.S)
    clean_html = r.sub('', clean_html)
    # 编译去掉<meta>标签
    r = re.compile(r'''<meta.*?>''', re.I | re.M | re.S)
    clean_html = r.sub('', clean_html)
    # 编译去掉<ins>标签中的内容
    r = re.compile(r'''<ins.*?</ins>''', re.I | re.M | re.S)
    clean_html = r.sub('', clean_html)
    return clean_html


def remove_line_space(pre_html):
    # 移除多个空格
    r = re.compile(r'''^\s+$''', re.M | re.S)
    clean_html = r.sub('', pre_html)
    # 移除换行符
    r = re.compile(r'''\n+''', re.M | re.S)
    clean_html = r.sub('\n', clean_html)
    return clean_html


def remove_all_tags(html):
    # 移除所有标签的内容
    html = re.sub(r'''<[^>]+>''', '', html)
    # 去掉首尾的空格
    return html.strip()


def remove_all_tags_without_a(html):
    # 正则表达式匹配所有a标签
    all_a = re.findall(r'''<a[^r][^>]*>(.*?)</a>''', html, re.I | re.S | re.S)
    # 移除标签后剩下的内容
    remain = remove_all_tags(html)
    return len(''.join(all_a)), len(remain)


def replace_img(html, num=50):
    # 将img标签替换为50个a字符, 图片的权重为50
    image = 'a' * num
    r = re.compile(r'<img src="(\S*)"')
    html = r.sub(image, html)
    return html


def replace_video(html, num=1000):
    # 将video标签换为1000个a字符,视频权重为1000
    video = 'a' * num
    r = re.compile(r'''<embed.*?>''', re.I | re.M | re.S)
    html = r.sub(video, html)
    return html


# 评分函数,找所有groups中的正文部分，即
# 正文部分中的评分会比较高
def sum_max(groups):
    # 以第一组数据的长度为初始参考值
    current_max = groups[0]
    # 初始化最大值
    all_max = -1000000
    # 下标开始结束值都是0
    begin, end = 0, 0
    # 对于每一个groups中的下标和当前下标的value值
    for index, value in enumerate(groups):
        # 当前最大值递增
        current_max += value
        if current_max > all_max:
            all_max = current_max
            end = index
        elif current_max < 0:
            current_max = 0
    # 从结尾开始反方向开始寻找,来找到最大的内容
    for i in range(end, -1, -1):
        all_max -= groups[i]
        if abs(all_max < 0.00001):
            begin = i
            break
    return begin, end+1


def clean(content, k=1):
    # 当content为空时返回控制，
    if not content:
        return None, None
    # 使用\n换行符将原始内容分割进tmp数组中
    temp = content.split('\n')
    # 将每一行的内容进行清理
    groups = []
    # k步进为1
    # 处理每一行数据
    for i in range(0, len(temp), k):
        # 单组数据是group
        single_group = '\n'.join(temp[i:i+k])
        # 移除图片标签
        single_group = replace_img(single_group)
        # 移除视频标签
        single_group = replace_video(single_group)
        # 移除除a标签外的所有标签
        len_a, len_remain = remove_all_tags_without_a(single_group)
        result = (len_remain - len_a) - 8
        groups.append(result)
    return sum_max(groups)


def extract(url_path):
    # 获取网址响应的内容
    html_data = requests.get(url_path)
    # 获取编码格式
    encoding = (requests.utils.get_encodings_from_content(html_data.text))
    # 如果网页中定义了编码格式，则取到当前网页的编码格式
    if encoding:
        html_data.encoding = encoding[0]
    # 否则设置当前编码格式为gbk
    else:
        html_data.encoding = 'gbk'
    #  开始降噪
    clean_content = remove_line_space(remove_js_css(html_data.text))
    len_of_a, len_of_remain = clean(clean_content)
    return '\n'.join(clean_content.split('\n')[len_of_a:len_of_remain])
