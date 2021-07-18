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
from sklearn.metrics.pairwise import cosine_similarity


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

def busca_idf(corpus,busca):
    #Criando corpus juntando a busca à base
    corpus_df = pd.concat([busca,corpus]).reset_index(drop=True)
    #Calculando IDF e vetorizando
    vetorizador =TfidfVectorizer(lowercase=False,tokenizer=lambda i:i) 
    tf_idf_matriz =  vetorizador.fit_transform(corpus_df['Sinopse_Processada'])
    #calculo da similiradidade
    similaridade = cosine_similarity(tf_idf_matriz)[0]    
    corpus_df['Similaridade'] = similaridade
    simi_df = corpus_df.sort_values(by=['Similaridade'],ascending=False)
    #trazendo os 5 primeiros resultados
    return simi_df[['Titulo','Sinopse','Genero','Similaridade']][1:6]


# =============================================================================
# Calculo do ICF,divisão do corpus por categorias e calculo do IDF para cad
# novo corpus
# =============================================================================
def busca_icf(corpus,busca):
    simi_lst=[]
    generos = corpus['Genero'].unique()[::-1]
    #O mesmo processo de busca_idf aplicado a cada corpus de cada genero
    for genero in generos:
        corpus= corpus[corpus['Genero']==genero]
        corpus_df = pd.concat([busca,corpus]).reset_index(drop=True)
        vetorizador =TfidfVectorizer(lowercase=False,tokenizer=lambda i:i)
        tf_icf_matriz = vetorizador.fit_transform(
            corpus_df['Sinopse_Processada'])
        similaridade = cosine_similarity(tf_icf_matriz)[0]    
        corpus_df['Similaridade'] = similaridade
        simi_lst.append(corpus_df)
    #Juntando o resultado de similaridade de cada genero para pegar os melhores
    #resultados
    simi_df = pd.concat(simi_lst)  
    simi_df = simi_df.sort_values(by=['Similaridade'],ascending=False)
    #trazendo os 5 primeiros resultados
    return simi_df[['Titulo','Sinopse','Genero','Similaridade']][4:9]                         


def recomendador(busca):
    #Pre-processando a busca
    busca_df = pd.DataFrame([{'Sinopse':busca}],columns=['Sinopse'])
    busca_df['Sinopse_Processada'] = busca_df['Sinopse'].apply(pre_processamento)
    #Realizando buscas por cada metodo
    recomendacao_idf = busca_idf(livros_df,busca_df)
    recomendacao_icf = busca_icf(livros_df,busca_df)
    return recomendacao_idf,recomendacao_icf        
        
#Aplicando pre-processamento à base    
livros_df=pd.read_csv('livros_df.csv',index_col=0)    
livros_df['Sinopse_Processada'] = livros_df['Sinopse'].apply(pre_processamento)

#Supondo que o usuário gostou de Lord of The Rings, colocarei como busca a sinopse
# do Fellowship of The Ring
with open('LOTR.txt','r') as file:
    busca = file.read()
recomendacao1 = recomendador(busca)#IDF melhor

#Supondo que o usuário gostou de It do Stephen King
with open('It.txt','r') as file:
    busca = file.read()
recomendacao2 = recomendador(busca)#IDF melhor

#Supondo que o usuário gostou de 7 Habits of Higly Effective People
with open('7habits.txt','r') as file:
    busca = file.read()
recomendacao3 = recomendador(busca)#ICF melhor

#Simulando um usuario buscando por algum livro
busca = 'Organization fighting against monsters that are murdering animal'
recomendacao4 = recomendador(busca) #IDf melhor

#Simulando outra busca
busca = 'Overcoming challenges and conquering yourself'
recomendacao5 = recomendador(busca) #ICF melhor

#Exportando os resultados das recomendações para csv
recomendacoes = [recomendacao1,recomendacao2,recomendacao3,recomendacao4,
                 recomendacao5]
for i,rec in enumerate(recomendacoes):
    idf = 'recomendacao_idf'+str(i+1)+'.csv'
    icf = 'recomendacao_icf'+str(i+1)+'.csv'
    rec[0].to_csv(idf)
    rec[1].to_csv(icf)





    


