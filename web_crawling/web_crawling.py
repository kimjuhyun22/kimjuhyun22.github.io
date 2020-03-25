# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 10:57:05 2020

@author: juhyun.kim
"""


import requests
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd


def blog_crawling(url):
   
    response = requests.get(url)
    
    # print(response)
    # print(response.status_code)
    # print(response.text)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    """  
    # Parsing tag p
    p_count = 0
    for p in soup.select('p'):
        p_count += 1
        print('\n', p_count)
        print(p)

    
    # Parsing tag a (= link)
    a_count = 0
    for link in soup.select('a'):
        a_count += 1
        print('\n', a_count)
        print(link.get('href'))
    """
  
          
    # Parsing definition lists
    blog_post_list = []
    li_count = 0
    
    for def_lists in soup.select('li.sh_blog_top > dl'):
        #li_count += 1
        #print('li_count: ', li_count)
        #print(def_lists)
        
        def_term = def_lists.select('dt > a')
        #print(def_term)
        title = def_term[0].get('title')
        #print('title: ', title)
        
        def_desc1 = def_lists.select('dd.sh_blog_passage')
        content = def_desc1[0].text
        #print('content: ', content)
        
        def_desc2 = def_lists.select('dd.txt_block a')
        author = def_desc2[0].text
        #print('author: ', author)
        
        blog_post = {'title': title, 'content': content, 'author': author}
        blog_post_list.append(blog_post)
                
    return blog_post_list
    

def save_data(blog_post):
    print(type(blog_post))
    
    if True:
        data = pd.DataFrame(blog_post)
        print(data.head())
        data.to_csv('blog_crawling1.csv', encoding='cp949') # encoding for Microsoft Office
    else:
        keys = blog_post[0].keys()
        with open('blog_crawling2.csv', 'w') as file:
            writer = csv.DictWriter(file, keys)
            writer.writeheader()
            writer.writerows(blog_post)
    
    
if __name__ == '__main__':
    
    blog_post_list = []
    blog_page_count = 0
    for i in range(1, 100, 10):
        blog_page_count += 1    
        #print('blog_page_count:', blog_page_count)  #10 posts per one page
        
        url = 'https://search.naver.com/search.naver?where=post&sm=tab_jum&query=%ED%99%8D%EB%8C%80+%EB%A7%9B%EC%A7%91'.format(page=i)
        if True:
            blog_post_list.extend(blog_crawling(url))
        else:          
            debug_temp = blog_crawling(url)
            print(debug_temp)
            blog_post_list.extend(debug_temp)                      
                                                 
    time.sleep(1)
        
    save_data(blog_post_list)
    print('Data write to a csv file is finished!')
    
    
    
    