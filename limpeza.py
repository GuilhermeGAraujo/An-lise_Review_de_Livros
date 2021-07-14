# -*- coding: utf-8 -*-
import pandas as pd

df=pd.read_csv(
    r'C:\Users\guilh\OneDrive\Documentos\Projetos\Analise_Review_de_Livros\livros_df.csv',
    index_col=0)

print(df.groupby('Genero').count()['Titulo'])
"""Genero
Audiobook          1
Business           1
Christian          1
Crime              3
Dark               1
Economics          1
Fantasy          107
Fiction           23
Historical        80
Horror            72
Mystery            2
Nonfiction        81
Politics           1
Religion           2
Short Stories      2
Sports             1
Thriller           6
"""
# =============================================================================
# Podemos ver que temos muito mais gêneros dos que os cinco correspondentes da 
# lista de melhroes por genero. Isso é devido ao fato dos generos como  
# "Não Ficção" ser mais uma categoria que pode conter livros sobre vários gêneros
# como política, religião, esportes; e também pelo fato de que o gênero coletado 
# pelo scraper é definido pelos leitores(users) enquanto a categorização das 
# listas é feita pelo site.
# 
# Isso também levou a gêneros terem mais livros do que deveria, como cada lista 
# continha 20 livros e foram usadas 5 linhas para cada, o máximo deveria ser 100, 
# mas fantasia possui 107. Suspetito que é devido ao fato de tanto histórias como
# de Terror e Ficção histórica podem possuir elementos de Fantasia levando a mais
# usuarios classificando como fantasia.
# 
# Eu vou classificar manualmente cada gênero de forma a diminuir a quantidade 
# pra visualizações futuras. É bem provavel que haverá classificações errôneas
# =============================================================================

#Dark,Thriller,Mystery = Horror
generos =['Dark','Thriller','Mystery']
df.loc[df['Genero'].isin(generos),'Genero']='Horror'
#Historical, Fiction = Historical Fiction
generos = ['Historical', 'Fiction']
df.loc[df['Genero'].isin(generos),'Genero']='Historical Fiction'

#Audiobook, Business,Christian, Crime,Economics,Politcs,Religion,Sports = 
#Non Fiction
generos = ['Audiobook','Business','Christian', 'Crime','Economics','Politics',
           'Religion','Sports','Nonfiction']
df.loc[df['Genero'].isin(generos),'Genero']='Non Fiction'
# =============================================================================
# As duas short stories são:
# The Paper Menagerie and Other Stories - Fantasia
# The Merry Spinster: Tales of Everyday Horror - Horror
# =============================================================================
df.loc[87,'Genero']='Fantasy'
df.loc[145,'Genero'] = 'Horror'

# Todas as sinopses terminam com (less), tabmém a uma sinopse nula
df =df.dropna(subset=['Sinopse'])
df['Sinopse']=df['Sinopse'].apply(lambda x: x[:-6])

df.to_csv(
    r'C:\Users\guilh\OneDrive\Documentos\Projetos\Analise_Review_de_Livros\livros_df.csv')