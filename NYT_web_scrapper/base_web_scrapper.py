import requests
import bs4
import json
from datetime import datetime
import os

def get_items_from_req(url:str,element:str,el_class:str,inner_element:str,inner_el_class:str,json_file = False) -> set:
    req = requests.get(url)
    bs = bs4.BeautifulSoup(req.content,features="html.parser")
    all_items = bs.findAll(element, attrs = {'class':el_class})

    all_articles = []

    # go through each found section and find the class for the articles
    # then get each articles's title
    for row in all_items:
        
        #find the content through p tag
        contents = row.findAll("p",attrs = {'class': "summary-class"})
        #find the titles with h3 tag
        titles = row.findAll(inner_element,attrs = {'class' : inner_el_class})

        for title in titles:
            article = {"title": "", "content": ""}
            if title.text:
                article["title"] = title.text
        for content in contents:
            if content:
                article["content"] = content.getText()
        # make sure no duplicates
        if article not in all_articles:
            all_articles.append(article)

    if json_file:

        file_title = os.path.dirname(__file__) + f"\\articles_{datetime.now().strftime('%b')}_{datetime.now().day}.json"

        with open(file_title,'w',encoding='utf-8') as file:
            json.dump(list(all_articles),file,ensure_ascii=False,indent=4)

    return req,all_articles


if __name__ == "__main__":
    # this is what the function searches for
    # findAll('section', attrs = {'class':"story-wrapper"})
    # findAll('h3',attrs = {'class' : 'indicate-hover'})
    req, articles = get_items_from_req("https://www.nytimes.com/","section","story-wrapper","h3",'indicate-hover',json_file=True)
    for article in articles:
        print(article)
        print("-----------------------------")

    