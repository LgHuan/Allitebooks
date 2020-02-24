import requests
from bs4 import BeautifulSoup
from lxml import etree
import json
import csv


url='http://www.allitebooks.org/page/{}'
page=1
headers={
    "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
}


class BookSpider():
    def __init__(self,url,page,headers):
        self.url=url
        self.page=page
        self.headers=headers
    def get_response(self,url):
        data_html=requests.get(url=url,headers=self.headers)
        data_html=data_html.content.decode()
        return data_html
    def get_parse_bs4(self,data_html):
        data_parse=BeautifulSoup(data_html,'lxml')
        data_parse.prettify()
        data_book=data_parse.select('article')

        data_book_dict={}
        data_book_list=[]
        for book in data_book:
            data_book_dict['data_name']=book.select_one('.entry-title').get_text()
            data_book_dict['data_img']=book.select_one('.attachment-post-thumbnail').get('src')
            data_book_dict['data_author'] = book.select_one('.entry-author').get_text()
            data_book_dict['data_info'] = book.select_one('.entry-summary').get_text()
            print(data_book_dict)
            data_book_list.append(data_book_dict)
        print(data_book_list)
        print(data_book_dict)
        return data_book_list
    def get_parse_xpath(self,data_html):
        data_parse = etree.HTML(data_html)
        data_book= data_parse.xpath('//div[@class="main-content-inner clearfix"]/article')
        '''
        data_book_dict={}

        book_name_list=[]
        for book in data_book:
            book_name=book.xpath('.//h2[@class="entry-title"]/a/text()')
            book_name_list.append(book_name)
        data_book_dict['book_name']=book_name_list

        book_img_list=[]
        for book in data_book:
            book_img=book.xpath('.//div[@class="entry-thumbnail hover-thumb"]/a/img/@src')
            book_img_list.append(book_img)
        data_book_dict['book_img']=book_img_list

        book_author_list=[]
        for book in data_book:
            book_author=book.xpath('.//h5[@class="entry-author"]/a/text()')
            book_author_list.append(book_author)
        data_book_dict['book_auther']=book_author_list

        book_info_list=[]
        for book in data_book:
            book_info=book.xpath('.//div[@class="entry-summary"]/p/text()')
            book_info_list.append(book_info)
        data_book_dict['book_info']=book_info_list
        '''
        data_book_dict = {}
        data_book_list=[]
        for book in data_book:
            book_name = book.xpath('.//h2[@class="entry-title"]/a/text()')
            data_book_dict['book_name'] = book_name
            book_img = book.xpath('.//div[@class="entry-thumbnail hover-thumb"]/a/img/@src')
            data_book_dict['book_img'] = book_img
            book_author = book.xpath('.//h5[@class="entry-author"]/a/text()')
            data_book_dict['book_auther'] = book_author
            book_info = book.xpath('.//div[@class="entry-summary"]/p/text()')
            data_book_dict['book_info'] = book_info
            data_book_list.append(data_book_dict)

        return data_book_list

    def save_data_json(self,data):
        f = open('allibook.json', 'w')
        json.dump(data, f)
        f.close()
    def save_data_txt(self,data):
        with open('allibook.csv','w') as f:
            title=['name','img','author','info']
            f_csv = csv.writer(f)
            f_csv.writerow(title)
            for i in data:
                print(i.values())
                f_csv.writerows(i.values())
        #with open('allibook.html','w')as f:
            #data=json.dumps(data)
            #f.write(data)

    def get_url_list(self):
        url_list=[]
        for i in range(1,self.page+1):
            url = self.url.format(i)
            url_list.append(url)
        return url_list
    def run(self):
        url_list=self.get_url_list()
        for url in url_list:
            data_html=self.get_response(url)
            data_parse=self.get_parse_bs4(data_html)
            #self.save_data_json(data_parse)
            #self.save_data_txt(data_parse)
            print(len(data_parse))
BookSpider(url=url,headers=headers,page=page).run()




