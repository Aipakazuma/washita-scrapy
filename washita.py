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


def get_item_scrapy(url):
    resource = get_web_esource(url)
    read_resource = resource.read()
    bs_obj = BeautifulSoup(read_resource, 'lxml')

    # product codeの取得
    product_code = bs_obj.find('span', {'id': 'product_code_default'}).getText().strip()

    # カテゴリの取得
    pankuzu_list = bs_obj.find('ul', {'id': 'topicpath'}).findAll('li')
    category_name = pankuzu_list[1].getText().strip()

    # カテゴリリストの取得
    category_sum_name = pankuzu_list[2].getText().strip()

    print(product_code + ',' + category_name + ',' + category_sum_name)


def get_items_scrapy(items):
    for item in items:
        a = item.find('h3').find('a')
        get_item_scrapy(site_url + a['href'])


def main():
    # argv = sys.argv
    url = 'http://www.washita.co.jp/products/list.php?transactionid=a444640e487c0b51ad18c9a282be125f8a6259d7&mode=search&category_id=0&maker_id=0&name=&product_code=&product_jancode=&price02_min=&price02_max=&orderby=&disp_number=200&product_id=&classcategory_id1=&classcategory_id2=&product_class_id=&quantity=&rnd=mor'
    # parameter_array = ['pri', 'tea', 'sti', 'pai', 'rac', 'cla', 'dri', 'phi', 'wae', 'nou']
    # parameter_array = ['pri']
    parameter = '&pageno='
    for i in range(6, 11):
        resource = get_web_esource(url + parameter + str(i))
        read_resource = resource.read()
        bs_obj = BeautifulSoup(read_resource, 'lxml')
        items = bs_obj.findAll('li', {'class': 'product_item'})
        get_items_scrapy(items)


if __name__ == '__main__':
    main()
