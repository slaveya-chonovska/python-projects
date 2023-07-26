import requests
from bs4 import BeautifulSoup
from collections import namedtuple
import os
import csv
import json
import tldextract
from logger import initialize_logger
import schedule
import time
from datetime import datetime
from urllib.parse import urlparse

class WebScrapper:

    """A class that can web scrape a bookstore page for certain number of items by given atributes, export the results to csv and/or json, and
        schedule a repeated scrapping. Note that the tag attributes need to be given in this order as a tuple:
        main parent tag (for book title), child tag(for author), child tag's class"""

    def __init__(self,url:str,attributes: tuple,item_length:int = 50,
                export_json:bool = False, json_file_name:str ="",
                export_csv:bool = False,csv_file_name:str = "",
                repeat:bool = False,repeat_in_minutes:int = 1) -> None:
        

        self.logger = initialize_logger()
        self.logger.info("Creating the web scrapper class instance.")
        self.title_element,self.author_class,self.author_inner_element = attributes

        #check if minutes repeated is correct
        if repeat and(repeat_in_minutes < 1 or not isinstance(repeat_in_minutes,int)):
            self.logger.debug("Repeat seconds error.")
            raise ValueError("The seconds for repeating must be at least 1 and a number!")

        self.repeat = repeat
        self.repeat_in_minutes = repeat_in_minutes
        if self.repeat:
            print(f"Scheduled repeat for every {self.repeat_in_minutes} seconds.")

        #some other checks for url and item length
        if not urlparse(url).scheme and not urlparse(url).netloc:
            self.logger.debug("Url error.")
            raise ValueError("Not a correct url link!")
        
        if item_length < 1 or not isinstance(item_length,int):
            self.logger.debug("Item length error.")
            raise ValueError("The item length must be at least 1 and a number!")
        
        self.url  = url 
        self.item_length = item_length

        self.export_csv = export_csv
        #if we need to record in csv
        if self.export_csv:
            #if no file name is given, make the default be the domain of the given website
            self.csv_file_name = (f"{os.path.dirname(__file__)}\\records\\") + (tldextract.extract(url).domain + ".csv" if not csv_file_name else csv_file_name)
            self.logger.info(f"The record csv file will have the name: '{self.csv_file_name}'.")
            #if the csv file does not exist, create it and write the field headers
            if not os.path.isfile(self.csv_file_name):
                with open(self.csv_file_name,'w',encoding='utf-8') as file:
                    csv_file = csv.writer(file)
                    self.logger.info(f"CSV file headers written.")
                    csv_file.writerow(("Title","Author","Link","IMG","Timestamp")) #field headers

        self.export_json = export_json
        #if we need to record in json
        if self.export_json:
            #if no file name is given, make the default be the domain of the given website
            self.json_file_name = (f"{os.path.dirname(__file__)}\\records\\") + (tldextract.extract(url).domain + ".json" if not json_file_name else json_file_name)
            self.logger.info(f"The record json file will have the name: '{self.json_file_name}'.")

#<----------------Request functions-------------------------------------------------->     
     
    # go through the html attributes and find what we are looking for
    def get_data(self,found_items) -> namedtuple:
        books = namedtuple("Books","title author href_link img_link timestamp")
        for item in found_items:
            self.logger.info("Getting item.")
            title = item.find('strong')
            title = title.find(self.title_element).text.strip('\n')

            author = item.find('div',attrs = {"class":self.author_class})
            try:
                author = author.find(self.author_inner_element).text.strip('\n')
            # sometimes author is empty
            except AttributeError:
                author = None

            href_link = item.a['href']
            img_link = item.img['src']
            #append the timestamp in a desired format
            yield books(title,author,href_link,img_link,datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    #get url request and loop through the pages to find the base of what we need to scrape
    def get_request(self) -> namedtuple:
        found_items = []
        req_url = self.url
        #find the index for the page number in the url, in case we need to request multiple pages
        page_index = req_url.index("?p=") + len("?p=")
        page_number = int(req_url[page_index])
        while len(found_items) < self.item_length:
            self.logger.info(f"Getting request from: {req_url}")
            req = requests.get(req_url)
            bs = BeautifulSoup(req.content,features="html.parser")
            found_items += (bs.find_all('li',attrs={'class':'product-item'}))
            page_number += 1
            #replace page number in url by the increased value
            req_url = req_url.replace(req_url[page_index],str(page_number))
        #return the generator named tuple only for the asked number of items
        return self.get_data(found_items[:self.item_length])
    
#<----------------CSV/JSON files functions-------------------------------------------------->   
 
    #create or open a csv file to record the data one by one
    def to_csv(self,data) ->None:

        # the file mode should be append to continue adding to the file
        with open(self.csv_file_name,'a',encoding='utf-8') as file:
            csv_file = csv.writer(file)
            self.logger.info(f"Putting data in the file {self.csv_file_name}")
            csv_file.writerow(data)

    # export in json format
    def to_json(self):

        with open(self.json_file_name,"a",encoding="utf-8") as file:
            self.logger.info(f"Writting to JSON file.")
            json.dump(list((item._asdict() for item in self.get_request())),file,ensure_ascii=False,indent=4)

#<----------------Sheduler function-------------------------------------------------->  

    #shedule job
    def create_job(self) -> None:
    
        schedule.every(self.repeat_in_minutes).minutes.do(self.scrape_data)
        while True:
            schedule.run_pending()
            time.sleep(1)

#<----------------Controller function-------------------------------------------------->  

    #controller for the scrapping
    def scrape_data(self) -> None:
        print(f"Scrapping from: {self.url}")
        self.logger.info(f"Scrapping from: {self.url}")

        self.logger.info("Printing the found data.")
        for data in self.get_request():
            print(data)
            # if we need to record to csv or json call the function
            if self.export_csv:
                self.to_csv(data)
        if self.export_json:
            self.to_json()

        #if we need to continue scrapping and no current jobs, create a shedule job
        if self.repeat and not schedule.get_jobs():
            self.logger.info(f"Repeating every {self.repeat_in_minutes} seconds")
            self.create_job()

if __name__ == "__main__":
    urls = ["https://www.orangecenter.bg/knizharnitsa/nay-prodavani-knigi?p=1","https://www.ciela.com/knigi?p=1&product_list_order=position"]
    attributes = [('span','product-item-subnames','span'),('a','author-info','a')]

    orange = WebScrapper(urls[0],attributes[0],export_csv=True,export_json=True,repeat = False)
    ciela = WebScrapper(urls[1],attributes[1],export_csv=True,export_json=True,repeat = False)

    orange.scrape_data()
    ciela.scrape_data()
