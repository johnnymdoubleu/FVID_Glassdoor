from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

email = "elainespak@gmail.com" #계정 이메일 주소
pw = "glassdoorteam!" #게정 비밀 번호
# email = "flamewndls@gmail.com"
# pw = "xkq4q5yi"

class Scrapper(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="./chromedriver") #chromedriver.exe가 이 파일과 같은 곳에 있기만 하면됩니다.
        self.wait = WebDriverWait(self.driver, 5)
        # self.page_source = ''
        self.login()

    def login(self):
        try:
            self.driver.get("https://www.jobplanet.co.kr/users/sign_in")
            user_login = self.wait.until(EC.presence_of_element_located((By.NAME, "user[email]")))
            # pw_login = self.driver.find_element_by_class_name("signin-password")
            pw_login = self.driver.find_element_by_name("user[password]")
            # login_button = self.driver.find_element_by_class_name("gd-ui-button.minWidthBtn.css-1i7s2wy")

            user_login.send_keys(email)
            user_login.send_keys(Keys.TAB)
            pw_login.send_keys(pw)
            pw_login.send_keys(Keys.RETURN)

        except TimeoutException:
            print("TimeoutException! Username/password field or login button not found on glassdoor.com")
            exit()

    def getPage(self, url):
        time.sleep(2)
        self.driver.get(url)

    def getNextPage(self,):
        soup = bs(self.driver.page_source,'html.parser')
        pageNo = soup.find('a',{'class':'btn_pgnext'}).get('href')
        url = 'https://www.jobplanet.co.kr' + pageNo
        if (pageNo != soup.find('a', {'class': 'btn_pglast'}).get('href')):
            return url
        else:
            return None

    def getLastPage(self):
        soup = bs(self.driver.page_source,'html.parser')
        pageNo = soup.find('a',{'class':'btn_pglast'}).get('href')
        url = 'https://www.jobplanet.co.kr' + pageNo
        # button = self.driver.find_element_by_xpath('//a[@class="btn_pgnext"]')
        # button.click()
        return url

    def getCompanyName(self):
        soup = bs(self.driver.page_source,'html.parser')
        tag = soup.find('h1',{'class':'name'})
        name = tag.find('a').text
        return name

    def getOverall(self):
        try :
            button = self.driver.find_element_by_xpath('//button[@class="btn_close_x_ty1"]')
            button.click()
        except Exception:
            pass

        time.sleep(2)
        soup = bs(self.driver.page_source,'html.parser')
        overall = soup.find('span',{'class':'alt_txt'})
        overallspecifics = list(overall)

        for i in soup.find_all('span',{'class':'txt_point'}):
            overallspecifics.append(i.text)

        df = pd.DataFrame(overallspecifics,
                index=['OverallRating','CareerOpportunity','Welfare','WorkLifeBalance','Culture','Management','Recommend%','Outlook%','CEOSuppot%'])
        df = df.transpose()

        return df

    def getData(self):
        soup = bs(self.driver.page_source,'html.parser')
        data=[]
        # id = soup.
        for sec in soup.find_all('section',{'data-content_type':'review'}):
            info=[]
            specifics=[]
            id = sec.get('data-content_id')
            rating = sec.find('div',{'class':'star_score'}).get('style')
            specifics.append(rating)
            date=sec.find('span',{'class':'txt2'}).text

            for i in sec.find_all('span',{'class':'txt1'}):
                info.append(i.text)

            for i in sec.find_all('div',{'class':'bl_score'}):
                specifics.append(i.get('style'))

            for i in range(6):
                rate = specifics[i]
                rate = rate.replace('width:','')
                rate = rate.replace('%;','')
                rate = str(int(rate) / 20)
                specifics[i]=rate

            comments=[]
            headline = sec.find('h2',{'class':'us_label'}).text
            headline = headline.replace('  ','')
            headline = headline.replace('\nBEST\n"','')
            headline = headline.replace('"\n','')
            headline = headline.replace('\n','.')

            for i in sec.find_all('dd',{'class':'df1'}):
                comment = i.find('span').text
                comment = comment.replace('\n','. ')
                comments.append(comment)

            while len(info) < 3:
                info.append('')

            p = sec.find('p',{'class':'etc_box'})
            if p.find('strong'):
                outlook = p.find('strong').text
            else :
                outlook = ''

            p = sec.find('p',{'class':'txt recommend etc_box'})
            if p.find('em') :
                recommend = p.find('em').text
            else:
                recommend = "비추천"

            thumbsup = sec.find('span',{'class':'notranslate'}).text

            review ={
                'id':id,
                'rating': specifics[0],
                'Career Opportunity' : specifics[1],
                'Compensation & Benefits' : specifics[2],
                'Work/Life Balance' : specifics[3],
                'Culture & Values' : specifics[4],
                'Senior Management' : specifics[5],
                'position': info[0],
                'status': info[1],
                'location' :info[2],
                'date': date,
                'headline': headline,
                'pros': comments[0],
                'cons': comments[1],
                'management_advice': comments[2],
                'outlook' : outlook,
                'recommend': recommend,
                'thumbsup': thumbsup
            }
            data.append(review)

        return data
