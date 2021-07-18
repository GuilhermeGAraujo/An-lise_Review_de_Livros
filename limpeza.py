# -*- coding: utf-8 -*-
import pandas as pd

df=pd.read_csv(
    r'C:\Users\guilh\OneDrive\Documentos\Projetos\Analise_Review_de_Livros\livros_df.csv',
    index_col=0)
print(df.groupby('Genero').count()['Titulo'])
"""Genero
Audiobook          1
Business           8
Crime              5
Dark               1
Economics          2
Education          1
Fantasy          214
Fiction           47
Historical       160
Horror           134
Mystery            7
Nonfiction       153
Paranormal         2
Parenting          2
Philosophy         1
Politics           2
Religion           2
Science            5
Science Fiction    2
Short Stories      3
Sports             2
Thriller          13
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

#Dark,Thriller,Mystery,Paranormal = Horror
generos =['Dark','Thriller','Mystery','Paranormal']
df.loc[df['Genero'].isin(generos),'Genero']='Horror'
#Historical, Fiction = Historical Fiction
generos = ['Historical', 'Fiction']
df.loc[df['Genero'].isin(generos),'Genero']='Historical Fiction'

#Audiobook, Business,Crime,Economics, Education,Parenting,Philosophy, Politcs,
#Religion,Science,Sports = Non Fiction
generos = ['Audiobook','Business', 'Crime','Economics','Education', 'Parenting',
           'Philosophy','Politics','Religion','Science','Sports','Nonfiction']
df.loc[df['Genero'].isin(generos),'Genero']='Non Fiction'
# =============================================================================
# As 3 short stories e 2 ficções científicas são:
# The Paper Menagerie and Other Stories - Fantasia
# The Merry Spinster: Tales of Everyday Horror - Horror
# Stay Awake - Horror
# The Last Town - Horror
# White Horse
# =============================================================================
df.loc[87,'Genero']='Fantasy'
df.loc[145,'Genero'] = 'Horror'
df.loc[544,'Genero'] ='Horror'
df.loc[510,'Genero'] ='Horror'
df.loc[545,'Genero'] ='Horror'

# Todas as sinopses terminam com (less), também há sinopses nulas
df =df.dropna(subset=['Sinopse'])
df['Sinopse']=df['Sinopse'].apply(lambda x: x[:-6])
df.to_csv(
    r'C:\Users\guilh\OneDrive\Documentos\Projetos\Analise_Review_de_Livros\livros_df.csv')




