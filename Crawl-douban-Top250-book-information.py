# 导入库
import requests
from bs4 import BeautifulSoup
 
 
# 发出请求并获得HTML源码的函数
def get_html(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}   # 伪装成浏览器访问
    resp = requests.get(url, headers=headers).text 
    return resp


# 获得所有页面的函数
def all_page():
    base_url = 'https://book.douban.com/top250?start='
    urllist = []
    # 从0到225，间隔25的数组
    for page in range(0, 250, 25):      # range()左闭右开，故取0到250
        allurl = base_url + str(page)
        urllist.append(allurl)          # 将所有页面地址存入urllist列表
    return  urllist


# 解析页面而获得数据信息的函数
# 思路：以每本书为单位，获取每本书的书名、作者、评分、简介等信息；部分书目缺乏简介时，返回'无'
def html_parse():
    # 调用all_page()函数，for循环迭代出所有页面
    for url in all_page():
        # 利用BeautifulSoup进行解析
        soup = BeautifulSoup(get_html(url), 'lxml')
        # 获取每本书全部信息所在的元素
        div = soup.find('div',  class_='indent')    # 检查网页，发现所有书籍信息都在<div class_='indent'>区域
        all_table = div.find_all('table')           # 每本书籍信息都对应于<div class_='indent'>区域下的每个table标签
        for table in all_table:
            # 书名
            name = table.find('div', class_='pl2').find('a')['title']   # 每本书籍的书名在<div class_='p12'>区域下的a标签中的title属性；直接用get_text()会把a标签中的空行也计入，因此用a.title
            name = '书名：' + str(name) + '\n'
            # 作者
            author = table.find('p', class_='pl').get_text()            # 每本书籍的作者在<p, class_='pl'>标签内部，直接用get_text()获得
            author = '作者：' + str(author) + '\n'
            # 评分
            score = table.find('span', class_='rating_nums').get_text() # 每本书籍的评分在<span, class_='rating_nums'>标签内部
            score = '评分：' + str(score) + '\n'
            # 简介
            if (table.find('span', class_='inq')):                      # 每本书籍的简介在<span, class_='inq'>标签内部，用if条件判断该书籍信息是否有简介，缺乏简介时，返回'无'
                sum = table.find('span', class_='inq').get_text()
            else:
                sum = '无'
            sum = '简介：' + str(sum) + '\n'
            # 整合每本书的书名、作者、评分、简介信息
            data = name + author + score + sum
            # 保存数据
            f.writelines(data + '=======================' + '\n')
 

# 文件名
filename = '豆瓣Top250图书信息.txt'
# 保存文件操作
f = open(filename, 'w', encoding='utf-8')
# 调用函数
html_parse()
f.close()
print('保存完成')

