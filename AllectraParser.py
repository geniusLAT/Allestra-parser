# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 01:50:55 2020

@author: Леонид
"""
# -*- coding: cp1251 -*-

"""
Created on Tue Jul 21 20:46:47 2020

@author: Леонид
"""


import requests
from bs4 import BeautifulSoup
import csv
import os
from selenium import webdriver
import tkinter as tk
import threading
import time

URL='https://shop.allectra.com/products/210-d15-k50'
HEADERS={'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 YaBrowser/20.7.2.124 Yowser/2.5 Safari/537.36', 'accept':'*/*'}

FILE='Table.csv'
Records=[]


def Mes(message):
    print(message)
    label['text']=message
    time.sleep(1)
    #window.mainloop()
    #e2.delete(0,last=len(e2.get()))
    #e2.insert(0,text)

def get_html(url,params=None):
    r=requests.get(url,headers=HEADERS,params=params)
    return r

def get_pages_count(html):
    
    soup=BeautifulSoup(html,'html.parser')
    pagination=soup.find_all('a')
    for item in pagination:
        print(item.get('href'))
    Mes("A")
    
def rec(html,linkToParse):
    
    
    
    soup=BeautifulSoup(html,'html.parser')
    h1=soup.find_all('td')#Парсим спецификацию
    name=soup.find('h3')#Парсим имя
    
  
    textview=str(soup)
   
    items=h1
    
    #Вытягиваем из скрипта цену актуальную для региона
    U=textview.find('price = ')
    textview=textview[U+1:U+300]
    U=textview.find('price = ')
    textview=textview[U+1:U+100]
    U=textview.find('price = ')
    textview=textview[U+9:U+20]
    U=textview.find(';')
    textview=textview[0:U-1]
    
    Record=[name.text,textview,linkToParse]
   
    
    #Создаём тестовую запись
   
    for item in items:      
      Record.append(item.text)
    
    
    Records.append(Record)
    
    #Этот код используется в другой версии
    #if (len(Records)<1000):
    #    forwardlink=soup.find('a',class_="forward-link")#Парсим ссылку на следующую шняжку
    #    link=forwardlink.get('href')
    #    Mes(link)
    #    parse(link)

def get_content(html):
    soup=BeautifulSoup(html,'html.parser')
    items=soup.find_all('div',class_='snippet-horizontal')
    i=0;#Счётчик элементов
    products=[]
    for item in items:
        i=i+1
        
        wrapper=item.find_next('div',class_='item_table-wrapper')
        if wrapper:
            #print(wrapper,end='\n\n')
            HOST=''
            link=HOST+item.find_next('a',class_='snippet-link').get('href')
            title=item.find_next('a',class_='snippet-link').find('span').get_text()
            address=wrapper.find_next('span',class_='item-address__string').get_text()
            price=wrapper.find_next('meta',itemprop='price').get('content')
            products.append({'Title':title,'Address':address,'price':price,'link':link})
        else:
            print('fail')
    return(products)
    

def save_file(items,path):
          with open(path,'w',newline='', encoding="utf-8") as file:
              writer=csv.writer(file,delimiter=';')
              Header=['Number','Name','Price','Link']
              for z in range(1,25):
                  Header.append('Something '+str(z))
              writer.writerow(Header)
              N=0
              for item in items:
                  N=N+1
                  #G=[N,   item['Title'].replace('\n','').replace('м²','м2'),item['Address'].replace('\n',''),item['price'],item['link'] ]
                  #print(item['Title'].replace('\n',''))
                  G=[N]
                  #print(N)
                  for i in item:
                      G.append(i)
                      #print(i)
                  writer.writerow(G)

# def save_file(items,path):
#           with open(path,'w',newline='', encoding="utf-8") as file:
#               writer=csv.writer(file,delimiter=';')
#               writer.writerow(['Номер','Тайтл','Адресс','Цена','ссылка'])
#               N=0
#               for item in items:
#                   N=N+1
#                   writer.writerow([N,item['Title'],item['Address'],item['price'],item['link'] ])

def open_saved_file(path):
    with open(path,'r', encoding="utf-8") as file:
        #s = get_content(file.read())
        s=file.readline()
        Mes(len(file.read()))
        return s
    
def parse(linkToParse):
    
    html=get_html(linkToParse)
    if 200==html.status_code:
        #print('Соединение установлено')
        #print(html.text)
        N=len(Records)
        Mes("Парсинг ссылки номер "+str(N))
        try:
            rec(html.text,linkToParse)
        except:
            Mes("Возникла ошибка")
        
    else:
        Mes('Соединение не установлено')
        Mes(html.status_code)
        
def ParseAndSave(URLs):
    for urk in URLs:
       parse(urk)
    save_file(Records,e2.get())
#s=open_saved_file('y.txt')
#one= open('1.txt',encoding="utf-8")
#print(get_content(one.read()))
#ParseAndSave()
    
def GetLinks():
    URLs=[]
    browser=webdriver.Chrome()
    page=1
    while(True):
        browser.get("https://shop.allectra.com/products?page="+str(page))
        links=browser.find_elements_by_class_name("title-link")
        for link in links:
           URLs.append(link.get_attribute("href"))
        if(len(links)==0):
            Mes("На странице "+str(page)+" найдено "+str(len(links))+" ссылок. Вероятно это последняя страница")
            break
            
        else:
            Mes("На странице "+str(page)+" найдено "+str(len(links))+" ссылок")
            page=page+1
    return URLs
    #print(URLs)
    #browser.find_element_by_class_name("ais-Pagination-item ais-Pagination-item--nextPage").click()
    browser.quit()

def Start():
    label['text']="message"
    Mes("Запущено")
    #Эта штука запустится в два потока, чтобы не отпал интерфейс, пока работает основной код
    t=threading.Thread(target=ParseAndSave(GetLinks()  ))
    t.start()
    print("Запуск потока")
    
def UUU():
    label['text']="messageT" 
    
window = tk.Tk()
label2 = tk.Label(text="Введите название файла, куда будет произведено сохранение")
e2=tk.Entry(width=50)
label3 = tk.Label(text="Пример: table.csv")
Button=tk.Button(text="Начать парсинг",command=Start)
label = tk.Label(text="Не запущено")


label2.pack()
label3.pack()
e2.pack()
Button.pack()    
label.pack()
window.mainloop()


    
    
    
    
