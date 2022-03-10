
from time import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as Soup
import time
import argparse



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Name(without .csv) of output .csv file")
    args = parser.parse_args()
    
    driverOptions = webdriver.ChromeOptions()
    driverOptions.add_argument("--disable-popup-blocking")
    driverOptions.add_argument("--incognito")  #incognito window
    #driverOptions.add_argument("--headless") #background execution
    driverOptions.add_argument("blink-settings=imagesEnabled=false") #wouldn't load image 
    driverOptions.add_argument("--no-sandbox") #privileged exec.
    driverOptions.add_argument("--disable-gpu")
    driverOptions.add_argument("--log-level=3")
    username = input('account/email: ')
    password = input('password: ')
    driver = webdriver.Chrome("./chromedriver", options=driverOptions)
    driver.get("https://www.facebook.com")
    WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID, "email")))
    element = driver.find_element_by_id("email")
    element.send_keys(username)
    element = driver.find_element_by_id("pass")
    element.send_keys(password)
    element.send_keys(Keys.RETURN)
    time.sleep(3)
    url = input("URL: ")
    driver.get(url)
    
    #detecting the cover photo to ensure that the browser has got into the right page
    classname_background = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of n00je7tq arfg74bv qs9ysxi8 k77z8yql l9j0dhe7 abiwlrkh p8dawk7l lzcic4wl a8c37x1j'
    classname_background = '.'.join(classname_background.split())
    WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, classname_background)))
    
    #crawling the page
    height = driver.execute_script('return window.document.documentElement.scrollHeight;')
    js = 'window.scrollTo(0, document.body.scrollHeight);'
    count_unmoved = 0 #for detecting the end of page
    MAX_NUM_SCROLL = 20 #due to the limit of memory, you need to set the maximum times of scrolling the page
    count_scroll = 0
    driver.execute_script(js)
    time.sleep(2)
    while count_unmoved < 3 and count_scroll < MAX_NUM_SCROLL:
        if height != driver.execute_script('return window.document.documentElement.scrollHeight;'):
            count_unmoved = 0
        else:
            count_unmoved += 1
        count_scroll += 1
        height = driver.execute_script('return window.document.documentElement.scrollHeight;')
        driver.execute_script(js)
        if count_scroll % 10 == 0:
            print(count_scroll)
        time.sleep(2)
    
    #parsing the page
    soup = Soup(driver.page_source, 'lxml')
    driver.quit()
    frames = soup.find_all(class_='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0')
    thumbs = []
    dates = []
    comments = []
    shares = []
    classname_date = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw'
    classname_comment = 'oajrlxb2 gs1a9yip mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 nhd2j8a9 mg4g778l pfnyh3mw p7hjln8o tgvbjcpo hpfvmrgz esuyzwwr f1sip0of n00je7tq arfg74bv qs9ysxi8 k77z8yql pq6dq46d btwxx1t3 abiwlrkh lzcic4wl dwo3fsh8 g5ia77u1 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv gmql0nx0 kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h du4w35lb gpro0wi8'
    for frame in frames:
        num_thumb = frame.find('span', class_='pcp91wgn')
        if num_thumb == None:
            thumbs.append(0)
        else:
            thumbs.append(num_thumb.text)
        date = frame.find(attrs={'aria-label': True}, class_=classname_date)
        if date.parent.name != 'object':
            dates.append(date.text.strip('='))
        num_comment = frame.find('div', attrs={'aria-expanded': True}, class_=classname_comment)
        if num_comment == None:
            comments.append(0)
        else:
            comments.append(num_comment.text)
        num_share = frame.find('div', attrs={'aria-expanded': False}, class_=classname_comment)
        if num_share == None:
            shares.append(0)
        else:
            shares.append(num_share.text)
    
    #write to file
    file = open("{a}.csv".format(a=args.filename), "w")
    for index in range(len(thumbs)):
        file.write("{a}, {b}, {c}, {d}\n".format(a=thumbs[index], b=dates[index],
                                                 c=comments[index], d=shares[index]))
    file.close()


        


        


    