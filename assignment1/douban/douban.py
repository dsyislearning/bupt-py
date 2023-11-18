import requests
from lxml import etree
import csv

# 豆瓣电影top250的url
url = ['https://movie.douban.com/top250?start=', 0, '&filter=']

# 伪造请求头
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

# 存储爬取的数据
data = []

# 每页25条数据，共10页
for i in range(10):
    url[1] = i * 25
    # 发送请求
    response = requests.get(''.join([url[0], str(url[1]), url[2]]), headers=headers)
    response.encoding = 'utf-8'

    # 解析html
    html = etree.HTML(response.text)

    # 获取每一页的电影信息列表
    items = html.xpath('//*[@id="content"]/div/div[1]/ol/li')

    for item in items:
        # 获取每一条电影信息的中文标题、短评、评分、评价人数
        title = item.xpath('./div/div[2]/div[1]/a/span[1]/text()')[0].strip()
        try:
            comment = item.xpath('./div/div[2]/div[2]/p[2]/span/text()')[0].strip()
        except IndexError:
            comment = 'NULL' # 有些电影没有短评
        score = item.xpath('./div/div[2]/div[2]/div/span[2]/text()')[0].strip()
        number = item.xpath('./div/div[2]/div[2]/div/span[4]/text()')[0].replace('人评价', '').strip()
        # 将每一条电影信息存入data
        data.append([title, comment, score, number])
    
# 将数据写入csv文件
with open('豆瓣top250.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='|')
    writer.writerow(['title', 'comment', 'score', 'number'])
    writer.writerows(data)
