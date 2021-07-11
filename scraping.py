# -*- coding: utf-8 -*-
"""
Sript para coleta de dados do projeto. Será coletado informaçoes de 20 livros 
de 5 categorias classificados como os melhores de 2020 pelo site goodreads.com.
"""

#Importando módulos
import requests
import time
from bs4 import BeautifulSoup
import re
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


  
#Extração dos links dos livro a partir da lista
def get_url_livros(url_list):
    livro_url_list=[]
    for url in url_list:
        source = requests.get(url).text
        page = BeautifulSoup(source,'lxml')
        livro_url_list.extend(page.find_all('a',class_="pollAnswer__bookLink"))
    return livro_url_list
    time.sleep(random.uniform(1,2))

#Extração dos livros
def get_livro(livro_url):
    
    get_livro.contador += 1
    gr_url = 'https://www.goodreads.com'
    livro_url = gr_url+livro_url['href']
    l_source=requests.get(livro_url).text
    l_page = BeautifulSoup(l_source,'lxml')
    #Coletando dos do livro
    titulo =l_page.find(id='bookTitle').text
    livro_id=re.search(r'[0-9]+\D',livro_url).group(0)[-1]
    serie =l_page.find(id='bookSeries').text
    autor = l_page.find('a',class_='authorName').text
    busca= l_page.find('a',class_='authorName')['href'] 
    autor_id = re.search(r'[0-9]+\D',busca).group(0)[:-1] if busca is not None\
        else None
    genero = l_page.find('a',class_='actionLinkLite bookPageGenreLink').text
    nota = l_page.find('span', itemprop='ratingValue').text
    num_notas = l_page.find('a',class_='gr-hyperlink',href='#other_reviews').text
    driver.get(livro_url)
    try:
        driver.find_element_by_xpath("//body").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@id='description']/a"))).click()
        sinopse = driver.find_element_by_xpath("//div[@id='description']").text
    except ElementClickInterceptedException:
        sinopse =''
    
    r_source = driver.page_source
    r_page = BeautifulSoup(r_source,'lxml')
    xpath="//a[@rel='next']"
    prox_page= True
    #Key = Reviewer id, valor= NOme reviewer 
    reviewer_dict={}
    while prox_page:
        r_source = driver.page_source
        r_page = BeautifulSoup(r_source,'lxml')
        todas_reviews = r_page.find_all('div',class_='reviewHeader uitext stacked')
        for review in todas_reviews:
            reviewer_user =review.find('a',class_='user')  
            busca=re.search(r'[0-9]+\D',reviewer_user['href'])
            user_id =busca.group(0)[:-1] if busca is not None else reviewer_user['href']
            reviewer_dict[user_id]= reviewer_user['name']
        try:
            prox_page=driver.find_element_by_xpath(xpath)
            prox_page.click()
        except NoSuchElementException:
            prox_page = None
        except ElementClickInterceptedException:
            prox_page = None
        except StaleElementReferenceException:
            prox_page = None
        time.sleep(random.uniform(1,3))
    print(get_livro.contador + ' livros coletados')
    livro_dict={'Titulo':titulo,'ID_Livro':livro_id,'Serie':serie,'Autor':autor,
           'ID_Autor':autor_id,'Genero':genero,'Nota':nota,'Sinopse':sinopse,
           'Numero_Avaliaçoes': num_notas,'Reviewer':reviewer_dict}
    return livro_dict
  
lista_url_scrape=[
    'https://www.goodreads.com/choiceawards/best-fantasy-books-2020',
    'https://www.goodreads.com/choiceawards/best-fantasy-books-2019',
    'https://www.goodreads.com/choiceawards/best-fantasy-books-2018',
    'https://www.goodreads.com/choiceawards/best-fantasy-books-2017',
    'https://www.goodreads.com/choiceawards/best-fantasy-books-2016',
    'https://www.goodreads.com/choiceawards/best-horror-books-2020',
    'https://www.goodreads.com/choiceawards/best-horror-books-2019',
    'https://www.goodreads.com/choiceawards/best-horror-books-2018',
    'https://www.goodreads.com/choiceawards/best-horror-books-2017',
    'https://www.goodreads.com/choiceawards/best-horror-books-2016',
    'https://www.goodreads.com/choiceawards/best-historical-fiction-books-2020',
    'https://www.goodreads.com/choiceawards/best-historical-fiction-books-2019',
    'https://www.goodreads.com/choiceawards/best-historical-fiction-books-2018',
    'https://www.goodreads.com/choiceawards/best-historical-fiction-books-2017',
    'https://www.goodreads.com/choiceawards/best-historical-fiction-books-2016',
    'https://www.goodreads.com/choiceawards/best-historical-fiction-books-2020',
    'https://www.goodreads.com/choiceawards/best-historical-fiction-books-2019',
    'https://www.goodreads.com/choiceawards/best-historical-fiction-books-2018',
    'https://www.goodreads.com/choiceawards/best-historical-fiction-books-2017',
    'https://www.goodreads.com/choiceawards/best-historical-fiction-books-2016',
    'https://www.goodreads.com/choiceawards/best-nonfiction-books-2020',
    'https://www.goodreads.com/choiceawards/best-nonfiction-books-2019',
    'https://www.goodreads.com/choiceawards/best-nonfiction-books-2018',
    'https://www.goodreads.com/choiceawards/best-nonfiction-books-2017',
    'https://www.goodreads.com/choiceawards/best-nonfiction-books-2016'
    ]


livro_url_list= get_url_livros(lista_url_scrape)
data=[]
option = webdriver.FirefoxOptions()
option.headless= True
driver = webdriver.Firefox(
    executable_path='C:\Webdrivers\geckodriver\geckodriver.exe',options=option)
verdade = True
get_livro.contador =0
# =============================================================================
# Devido ao funcionamento inconsistente do scraper em consegui localizar elementos
# devido a overlays aparecendo aleatoriamente, ou mesmo a página não carregando
# corretamente por qeustões de desempenho do computador e conexão. Coloquei a
# coelta de dados em um loop para que seja reexcutada quando ocorrer um erro.
# =============================================================================
while verdade:
    try:        
        livro_url = livro_url_list.pop(0)
        data.append(get_livro(livro_url))
    except KeyboardInterrupt:
        verdade = False
    except:
        if len(livro_url_list) ==0:
            verdade = False
        else:
            pass



driver.quit()
df = pd.DataFrame(data)
df.to_csv(r'C:\\Users\guilh\OneDrive\Documentos\Projetos\Analise_Review_de_Livros\livros_df.csv')


    
    
    
