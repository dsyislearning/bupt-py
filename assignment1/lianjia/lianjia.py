import requests
from lxml import etree
import csv

root_url = 'https://bj.lianjia.com'
url = 'https://bj.lianjia.com/ershoufang/'

# 伪造请求头
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)

html = etree.HTML(response.text)

areas = html.xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div/a')

targets = ['东城', '西城', '朝阳', '海淀']

for area in areas:
    if area.text in targets:
        # 获取每个区域的url，去掉最后的pg1
        area_url = root_url + area.xpath('./@href')[0].replace('pg1', '')
        # 存储爬取的数据
        data = []
        for i in range(5): # 爬取前5页
            page_url = area_url + 'pg' + str(i + 1) # 拼接每一页的url，如https://bj.lianjia.com/ershoufang/dongcheng/pg1
            response = requests.get(page_url, headers=headers)
            response.encoding = 'utf-8'
            html = etree.HTML(response.text)
            # 获取每一页的房源信息
            sell_list = html.xpath('/html/body/div[4]/div[1]/ul/li')
            for sell in sell_list:
                # 获取每一条房源信息的楼盘名称、面积、总价、单价
                title = sell.xpath('./div/div[2]/div/a/text()')[0].strip()
                area_value = sell.xpath('./div/div[3]/div/text()')[0].split('|')[1].replace('平米', '').strip()
                total_price = sell.xpath('./div/div[6]/div[1]/span/text()')[0].strip()
                unit_price = sell.xpath('./div/div[6]/div[2]/span/text()')[0].replace('元/平', '').replace(',', '').strip()
                # 将每一条房源信息存入data
                data.append([title, area_value, total_price, unit_price])
        # 将数据写入csv文件
        with open(area.text + '.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['title', 'area_value', 'total_price', 'unit_price'])
            writer.writerows(data)
