from jobClass import Scrapper
import time
import pandas as pd

url = 'https://www.jobplanet.co.kr/companies/30139/reviews/삼성전자?page=1' # 삼성전자(주)
# url='https://www.jobplanet.co.kr/companies/322493/reviews/%EC%A7%80%EC%97%90%EC%9D%B4%EC%B9%98%EC%94%A8%EC%A7%80' # (주)지에이치씨지

#우선적으로 크롤러가 잘 되는지 확인하기위해 비교적 리뷰수가 적은 기업인 (주)지에이치씨지의 리뷰를 이용해여 크롤한다.
result = []

print ('Starting Scrapper and logging in to {}...'.format(url.split('.')[1]))
sr = Scrapper()
print ('Getting reviews page 1...')
time.sleep(2)
print ('parsing of page 1...')
sr.getPage(url)
time.sleep(2)
overall = sr.getOverall()
data = sr.getData()
print (len(data), 'reviews found on this page. \n\n')
result.extend(data)

count = 2
Next_Page = True
while Next_Page:
    Next_Page = sr.getNextPage()
    if Next_Page:
        print ('Getting reviews of page %s...'%(count))
        sr.getPage(Next_Page)
        print ('parsing of page %s...'%(count))
        data = sr.getData()
        if len(data) > 1 :
            print (len(data), 'reviews found on this page. \n\n')
            result.extend(data)
            count +=1
    else:
        lastPage = sr.getLastPage()
        break

print ('Getting reviews page %s...'%(count))
time.sleep(2)
print ('parsing of page %s...'%(count))
sr.getPage(lastPage)
time.sleep(2)
data = sr.getData()
print (len(data), 'reviews found on this page. \n\n')
result.extend(data)
print ('Reviews crawling completed.\n End Task... \n\n')
print(overall,'\n\n')

df = pd.DataFrame(result[0],columns=['id','rating','Career Opportunity','Compensation & Benefits','Work/Life Balance','Culture & Values','Senior Management',
'position','status','location','date','headline','pros','cons','management_advice','outlook','recommend','thumbsup'],index=[0])

for i in result[1:len(result)-1] :
    df = df.append(i , ignore_index=True)
print(df)
#
filename = sr.getCompanyName() + 'Reviews.csv'
print ('Writing results to %s'%filename)
df.to_csv("D:\\PythonProgrammes\\InternStuffs\\" + filename,index=False, encoding='utf_8_sig') #파일 저장 경로, utf_8_sig은 한글 인식함.
