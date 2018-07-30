# coding=utf-8
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import De_noise
import DFA


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置主界面
        self.setWindowTitle("网页去噪")
        self.resize(900, 600)
        self.show()

        # 设置中心组件为浏览器界面
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # 添加工具栏
        navigation_bar = QToolBar()
        navigation_bar.setMovable(False)
        self.addToolBar(navigation_bar)

        # 在工具栏上添加一个输入框
        self.urlBar = QLineEdit()
        # 直接设置一个简单的要过滤的网址
        self.urlBar.setText("http://new.qq.com/omn/20180512/20180512A0DJRR.html")
        # 设置回车时的事件处理
        self.urlBar.returnPressed.connect(self.navigate_to_url)
        navigation_bar.addWidget(self.urlBar)

    # 定义回车时的处理函数
    def navigate_to_url(self):
        # 只有网址栏不为空时才开始处理
        if self.urlBar.text() != '':
            # 先清空浏览器界面
            self.browser.setHtml("")
            # 网页去噪, 提取主要内容, 参数传递过去的是一个网址
            without_noise_html = De_noise.extract(self.urlBar.text())
            # dfa算法过滤敏感词
            clean_html = DFA.dfa_html(without_noise_html)
            # 将过滤后的网页居中显示
            html_head = '''<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
		<style type="text/css">
			div {
			    display: block;
			}
			#u_sp{
				position: absolute;
			    top: 0;
			    right: 0;
			    z-index: 100;
			    width: 590px;
			    font-size: 13px;
			    text-align: right;
			    color: #999;
			    margin-right: 11%;
			}
			.s-sp-menu a {
			    position: relative;
			    height: 32px;
			    line-height: 32px;
			    margin-left: 10px;
			    color: #555;
			    text-decoration: underline;
			    outline: none;
			    display: inline-block;
			    text-shadow: none;
			}
			.article{
				text-align: center;
				margin-top: 30px;
				width: 80%;
			 	margin-left: auto; 
			 	margin-right: auto;
			}
			.article p{
				text-align: left;				
			}
		</style>
	</head>
	<body>
		<div id = "u_sp" class="s-sp-menu">
			<a href="http://news.baidu.com" name="tj_trnews" class="mnav">新闻</a>
			<a href="http://www.hao123.com" name="tj_trhao123" class="mnav">hao123</a>
			<a href="http://map.baidu.com" name="tj_trmap" class="mnav">地图</a>
			<a href="http://v.baidu.com" name="tj_trvideo" class="mnav">视频</a>
			<a href="http://tieba.baidu.com" name="tj_trtieba" class="mnav">贴吧</a>
			<a href="http://xueshu.baidu.com" name="tj_trxueshu" class="mnav">学术</a>
			<a href="https://passport.baidu.com" name="tj_login" class="lb">登录</a>
			<a href="http://www.baidu.com/gaoji/preferences.html" name="tj_settingicon" class="pf">设置</a>
		</div>
		<div class="article">'''
            html_foot = "</div></body></html>"
            result = html_head+clean_html+html_foot
            # 浏览器页面设置显示过滤后的最终结果
            self.browser.setHtml(result)


if __name__ == '__main__':
    # PyQt库的主函数运行, 并显示界面
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

