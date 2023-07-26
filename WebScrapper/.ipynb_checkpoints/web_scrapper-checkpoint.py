#https://www.orangecenter.bg/knizharnitsa/nay-prodavani-knigi
#https://www.ciela.com/knigi?p=1&product_list_order=position

import requests
from bs4 import BeautifulSoup
from collections import namedtuple
from itertools import islice
import json
import csv
import pandas as pd

# def get_data1(found_items:list) -> namedtuple:
#     books = namedtuple("Books","title author href_link img_link")
#     for item in found_items:
#         title = item.find('strong').span.text
#         author = item.find('div',attrs = {"class":'product-item-subnames'}).span.text.strip('\n')
#         href_link = item.a['href']
#         img_link = item.img['src']
#         yield books(title,author,href_link,img_link)

# def get_request(url:str) -> namedtuple:
#     req = requests.get(url)
#     bs = BeautifulSoup(req.content,features="html.parser")
#     found_items = bs.find_all('li',attrs={'class':'product item product-item-vertical product-item product--promo'})
#     return get_data(found_items)

# def get_data2(found_items:list) -> namedtuple:
#     books = namedtuple("Books","title author href_link img_link")
#     for item in found_items:
#         title = item.find('strong').a.text
#         author = item.find('div',attrs = {"class":'author-info'}).a.text
#         href_link = item.a['href'] 
#         img_link = item.img['src']
#         yield books(title,author,href_link,img_link)


def get_data(found_items:list,title_element:str,author_class:str,author_inner_element:str) -> namedtuple:
    print(len(found_items))
    books = namedtuple("Books","title author href_link img_link")
    for item in found_items:
        title = item.find('strong')
        title = title.a.text.strip('\n') if title_element == 'a' else item.find('strong').span.text.strip('\n')

        author = item.find('div',attrs = {"class":author_class})
        try:
            author = author.span.text.strip('\n') if author_inner_element == 'span' else author.a.text.strip('\n')
        except AttributeError:
            author = None

        href_link = item.a['href']
        img_link = item.img['src']
        yield books(title,author,href_link,img_link)

def get_request(url:str,title_element:str,author_class:str,author_inner_element:str,item_length:int = 50) -> namedtuple:
    found_items = []
    page_index = url.index("?p=") + len("?p=")
    page_number = int(url[page_index])
    while len(found_items) < item_length:
        req = requests.get(url)
        bs = BeautifulSoup(req.content,features="html.parser")
        found_items += (bs.find_all('li',attrs={'class':'product-item'}))
        page_number += 1
        url = url.replace(url[page_index],str(page_number))
    return get_data(found_items[:item_length],title_element,author_class,author_inner_element)

urls = ["https://www.orangecenter.bg/knizharnitsa/nay-prodavani-knigi?p=1","https://www.ciela.com/knigi?p=1&product_list_order=position"]


#get_request(urls[0],'span','product-item-subnames','span')
#get_request(urls[1],'a','author-info','a')

attributes = [('span','product-item-subnames','span'),('a','author-info','a')]

def to_json(file_name:str) -> None:

    with open("books.json",'w',encoding='utf-8') as file:
        for url,attr in zip(urls,attributes):
            print(url)
            #json.dump([url],file,indent=1)
            books = { url: list(get_request(url,*attr))}
            json.dump(books,file,indent=3,ensure_ascii=False)

def to_csv(file_name:str) ->None:
    # for url,attr in zip(urls,attributes):
    #     print(url)
    #     #json.dump([url],file,indent=1)
    #     books = { url: list(get_request(url,*attr))}

    with open("books.csv",'w',encoding='utf-8') as file:

        csv_file = csv.writer(file)
        csv_file.writerow(("Title","Author","Link","IMG")) #field headers
        for url,attr in zip(urls,attributes):
            csv_file.writerows(list(get_request(url,*attr)))

f_books = pd.read_csv("books.csv",delimiter=",",header=0)
print(f_books)
        

            

