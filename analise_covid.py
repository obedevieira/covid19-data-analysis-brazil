
# EDA COVID-19 Brasil - Projeto de Portfólio
# Autor: Obede Vieira dos Santos

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Configurações
sns.set(style='whitegrid')
plt.rcParams['figure.figsize'] = (14, 6)

# Carregando os dados
url = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv"
df = pd.read_csv(url, parse_dates=['date'])

# Limpeza
df = df[(df['newCases'] >= 0) & (df['newDeaths'] >= 0)]
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

# Análise Descritiva
print(df.info())
print(df.describe())
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.title('Mapa de Calor dos Valores Ausentes')
plt.show()

# Histogramas
df[['newCases', 'newDeaths']].hist(bins=30)
plt.suptitle('Distribuição de Novos Casos e Mortes')
plt.show()

# Estatísticas básicas
print("Média de novos casos:", df['newCases'].mean())
print("Mediana:", df['newCases'].median())
print("Desvio padrão:", df['newCases'].std())

# Outliers
sns.boxplot(x=df['newCases'])
plt.title('Boxplot de Novos Casos')
plt.show()

# Tendência Nacional
brasil = df.groupby('date')[['newCases', 'newDeaths']].sum().reset_index()
sns.lineplot(data=brasil, x='date', y='newCases', label='Novos Casos')
sns.lineplot(data=brasil, x='date', y='newDeaths', label='Novas Mortes')
plt.title('Evolução de Casos e Mortes no Brasil')
plt.show()

# Estados com mais casos
top5 = df[df['date'] == df['date'].max()].nlargest(5, 'totalCases')['state']
df_top = df[df['state'].isin(top5)]
sns.lineplot(data=df_top, x='date', y='newCases', hue='state')
plt.title('Evolução dos Novos Casos - Top 5 Estados')
plt.show()

# Correlação
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
plt.title('Correlação entre Variáveis')
plt.show()

# Visualização Interativa
latest = df[df['date'] == df['date'].max()]
fig = px.scatter(latest, x='totalCases', y='deaths', color='state',
                 size='population', hover_name='state',
                 title='Casos x Mortes por Estado')
fig.show()
