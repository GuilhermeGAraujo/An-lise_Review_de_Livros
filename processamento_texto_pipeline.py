# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 20:43:43 2021

@author: guilh
"""
import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import re
from sklearn.feature_extraction.text import TfidfVectorizer

livros_df=pd.read_csv('livros_df.csv',index_col=0)
#%%


def pre_processamento(texto):    
    
    texto = texto.lower()
    #remover número
    texto = re.sub(r'[0-9]','',texto)
    #remover pontuação
    pontuacao = string.punctuation
    texto = ''.join([p for p in texto if p not in pontuacao])
    #Separando palavras
    texto = word_tokenize(texto)
    
    #Remoação de  stopwords e stemming
    stop_words = set(stopwords.words('english'))
    stemmer = SnowballStemmer('english')
    texto = [stemmer.stem(p) for p in texto if p not in stop_words and 
             len(p) > 1]
    return texto


livros_df['Sinopse_Processada'] = livros_df['Sinopse'].apply(pre_processamento)
vetorizador =TfidfVectorizer(lowercase=False,tokenizer=lambda i:i) 
tf_idf_matriz =  vetorizador.fit_transform(livros_df['Sinopse_Processada']) 
#%%
tf_idf_matriz.idf_ 

