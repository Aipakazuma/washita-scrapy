# -*- coding:utf8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
import sys

site_url = 'http://www.washita.co.jp'


def get_web_esource(url):
    try:
        return urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    except URLError as e:
        print('The server could not be found!')
        return None


def get_item_scrapy(url, f):
    resource = get_web_esource(url)
    read_resource = resource.read()
    bs_obj = BeautifulSoup(read_resource, 'lxml')

    try:
        # product codeの取得
        product_code = bs_obj.find('span', {'id': 'product_code_default'}).getText().strip()

        # カテゴリの取得
        pankuzu_list = bs_obj.find('ul', {'id': 'topicpath'}).findAll('li')
        category_name = pankuzu_list[1].getText().strip()

        # カテゴリリストの取得
        category_sum_name = pankuzu_list[2].getText().strip()

        # 商品名の用意
        item_title = bs_obj.find('div', {'id': 'detailrightbloc'}).find('h3').getText().strip()

        # 画像を取得
        image_src = bs_obj.find('img', {'class': 'picture'})['src']

        # 説明を取得
        explain_text = bs_obj.find('div', {'class': 'main_comment'}).getText().strip().replace('\n', '').replace('\r', '')

        f.write(product_code + ',' +
                item_title + ',' +
                category_name + ',' +
                category_sum_name + ',' +
                image_src + ',"' +
                explain_text + '"\n')
    except IndexError as e:
        print(e)
        print(url)


def get_items_scrapy(items, f):
    for item in items:
        a = item.find('h3').find('a')
        get_item_scrapy(site_url + a['href'], f)


def main():
    # argv = sys.argv
    url = 'http://www.washita.co.jp/products/list.php?transactionid=b6d044fea3bfee66a24d564f03c105886e1452db&mode=search&category_id=0&maker_id=0&name=&product_code=&product_jancode=&price02_min=&price02_max=&orderby=&disp_number=200&product_id=&classcategory_id1=&classcategory_id2=&product_class_id=&quantity=&rnd=slo'
    parameter = '&pageno='
    f = open('result_20160616.csv', 'w')
    for i in range(1, 11):
        resource = get_web_esource(url + parameter + str(i))
        read_resource = resource.read()
        bs_obj = BeautifulSoup(read_resource, 'lxml')
        items = bs_obj.findAll('li', {'class': 'product_item'})
        get_items_scrapy(items, f)
        print(i)
    f.close()


if __name__ == '__main__':
    main()
