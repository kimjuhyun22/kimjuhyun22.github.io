# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 14:34:12 2020
@author: juhyun.kim
@reference: https://neung0.tistory.com/34
"""

""" external library modules """
from selenium import webdriver # conda install selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip # pip install pyperclip
from bs4 import BeautifulSoup as bs # conda install bs4
import numpy as np
from numpy import genfromtxt
import pandas as pd
""" stadard library modules """
import time
import csv

driver = webdriver.Chrome('./chromedriver_win32/chromedriver.exe')
driver.implicitly_wait(3)

#key_down 메소드를 이용해 컨트롤키를 누르고, 그 상태에서 v를 입력시킨고 key_up 메소드를 이용, 컨트롤 키를 뗀다.
#즉, 클립보드에 있는 내용을 Ctrl+V를 이용해 붙여넣은 뒤 perform으로 실행시키는 형식이다.
# reference: https://neung0.tistory.com/34
def copy_input(xpath, input):
    pyperclip.copy(input)
    driver.find_element_by_xpath(xpath).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(0.1)
    
"""
1) URL에 접근하는 메소드,
get('http://url.com')
2) 페이지의 단일 element에 접근하는 메소드,
find_element_by_name('HTML_name')
find_element_by_id('HTML_id')
find_element_by_xpath('/html/body/some/xpath')
find_element_by_css_selector('#css > div.selector')
find_element_by_class_name('some_class_name')
find_element_by_tag_name('h1')
3) 페이지의 여러 elements에 접근하는 메소드 등이 있다. (대부분 element 를 elements 로 바꾸기만 하면 된다.)
find_elements_by_css_selector('#css > div.selector')
위 메소드들을 활용시 HTML을 브라우저에서 파싱해주기 때문에 굳이 Python와 BeautifulSoup을 사용하지 않아도 된다.
"""

"""
Selenium에 내장된 함수만 사용가능하기 때문에 좀더 사용이 편리한 soup객체를 이용하려면 driver.page_source API를 이용해 현재 렌더링 된 페이지의 Elements를 모두 가져올 수 있다.
1) driver.page_source:
    브라우저에 보이는 그대로의 HTML, 크롬 개발자 도구의 Element 탭 내용과 동일.
2) requests 통해 가져온 req.text:
    HTTP요청 결과로 받아온 HTML, 크롬 개발자 도구의 페이지 소스 내용과 동일.
위 2개는 사이트에 따라 같을수도 다를수도 있습니다.
"""

# 네이버 로그인 하기
# 네이버 로그인 페이지를 가져온다.
my_id = 'jhkim0204'
my_pw = 'enough8996!'
driver.get('https://nid.naver.com/nidlogin.login')
# 아이디/비밀번호를 입력해준다.
#wdriver.find_element_by_name('id').send_keys('jhkim0204')
#wdriver.find_element_by_name('pw').send_keys('enough8996!')

#클립보드에 input을 복사한 뒤
#해당 내용을 actionChain을 이용해 로그인 폼에 붙여넣기

copy_input('//*[@id="id"]', my_id)
time.sleep(0.1)
copy_input('//*[@id="pw"]', my_pw)
time.sleep(0.1)

"""
Selenium의 driver를 이용하여 아이디 및 비밀번호를 element.send_keys()메서드를 이용하여 로그인 시도 시 비정상적인 접근 방식으로 네이버 Captcha가 탐지하게 됐습니다.
비밀번호를 제외한 아이디만 element.send_keys()메서드를 통해 입력한 경우에도 네이버 Captcha가 탐지합니다.
-> solution: Ctrl+V 키 조합을 element에 보낼 경우 네이버 Captcha가 비정상적인 로그인 시도를 탐지하지 못하고 정상적인 로그인에 성공합니다.
"""

# 로그인 버튼을 눌러주자.
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
#wdriver.find_element_by_xpath('/html/body/div[2]/div[3]/div/form/fieldset/input').click()

"""
# Naver 페이 들어가기
wdriver.get('https://order.pay.naver.com/home')
html = wdriver.page_source
soup = BeautifulSoup(html, 'html.parser')
notices = soup.select('div.p_inr > div.p_info > a > span')
for n in notices:
    print(n.text.strip())
"""

# 카페로 이동
driver.get('https://cafe.naver.com/ArticleList.nhn?search.clubid=11525920')

# base_url = cafe main page url 
base_url = 'https://cafe.naver.com/ArticleList.nhn?search.clubid=11525920'
board_id = 14
#cnt = 0 # number of collected data
page = 0 # position of current page
view_items_cnt = 5
view_totalCount = view_items_cnt*10 + 1

# db connect and select
#conn = pymysql.connect(host='192.168.1.25', user = 'db_user', password='db_pw', db = 'mariadb',charset = 'utf8')
#curs = conn.cursor(pymysql.cursors.DictCursor)
job_seq = 0
temp_list = []

while page < 2 : # 게시글 페이지 수 입니다. 올해글이 약 102page를 차지하고 있었습니다. 
    page = page + 1 
    cnt = 0 
    quest_urls = [] 
    try :
        # add personal conditions 
        # &search.menuid = : 게시판 번호(카페마다 상이) 
        # &search.page = : 데이터 수집 할 페이지 번호 
        # &userDisplay = 50 : 한 페이지에 보여질 게시글 수 
        #https://cafe.naver.com/ArticleList.nhn?search.clubid=11525920
        #&search.menuid=14&userDisplay=10&search.boardtype=L&search.specialmenutype=&search.totalCount=101&search.page=3
        #board_url = base_url + '&search.menuid=14&userDisplay=10&search.boardtype=L&search.specialmenutype=&search.totalCount=101&search.page=2'
        board_url = base_url + '&search.menuid='+str(board_id) + '&userDisplay='+str(view_items_cnt) + '&search.boardtype=L&search.specialmenutype=&search.totalCount='+str(view_totalCount) + '&search.page='+str(page)     
        #print(board_url)
        driver.get(board_url)
        
        driver.switch_to.frame('cafe_main') #iframe으로 프레임 전환 
        quest_list = driver.find_elements_by_css_selector('div.inner_list > a.article') 
        quest_urls = [i.get_attribute('href') for i in quest_list]
        #print(quest_urls)        
        print('quest_urls: ', len(quest_urls))       
        
        for quest in quest_urls :
            cnt += 1
            try : #게시글이 삭제되었을 경우가 있기 때문에 try-exception
                #print(quest)   
                driver.get(quest)            
                driver.switch_to.frame('cafe_main')
                html = driver.page_source
                soup = bs(html, 'html.parser')
               
                #제목 추출
                title = soup.select('div.tit-box span.b')[0].get_text()
                print(cnt, ': ', title)
                
                #내용 추출
                content_tags = soup.select('#tbody')[0].select('p')
                content = ' '.join([tags.get_text() for tags in content_tags])                
                #print(content)                               
              
                #말머리 추출
                try :
                    #tag = soup.select('div.tit-box span.head')[0].get_text()
                    temp_list.append([title, content])         
                except : # 말머리 없으면 next 
                    pass  
                #temp_list.append((title, content))
                
            except : # chrome alert창 처리해줌
                driver.switch_to_alert.accpet()
                driver.switch_to_alert
                driver.switch_to_alert.accpet()
                    
    except :
        pass                 
        
    print([page, cnt]) #page로는 진행상황을 알 수 있고 cnt로는 몇개의 데이터를 모았는지 알 수 있음
            
""" csv file write 1 
with open('preg_quest.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(temp_list)
"""
"""  csv file write 2-1
# ndarray 타입인 data를 csv 파일에 쓰기 (한글 사용 불가)
np.savetxt('preg_quest.csv', tmp_list, fmt='%.1f,%.8f,%d', header='time,vel,alt', comments='')
"""
""" csv file write 2-2 """
with open('preg_quest.csv', 'w', newline='', encoding='utf8') as f:
    f.write('title, contents\n')
    writer = csv.writer(f)
    writer.writerows(temp_list)

""" csv file write 3
pd.DataFrame(tmp_list)
"""

""" csv file read 1
with open('preg_quest.csv', 'r', encoding='utf8') as f:
    reader = csv.reader(f) # reader: 반복가능 객체 
    read_dat = [k for k in reader]
    print(read_data)
"""
""" csv file read 2
read_dat = np.loadtxt('preg_quest.csv', delimiter=',', skiprows=1, dtype=float)
"""
""" csv file read 3
read_dat = genfromtxt('preg_quest.csv', skip_header=1, delimiter=',', dtype=float)
"""


    