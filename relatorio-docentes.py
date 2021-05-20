import pandas as pd
import numpy as np
import streamlit as st
import PIL

data = pd.read_pickle('dados-relatorio-alunos/data.pkl')

st.title('Relatório Docentes')

st.write('Olá Docente! Este é o seu **relatório do Simulinho 2021**.')
st.write("Ele é dividido em **duas seções principais**. A primeira delas, apresenta dados gerais sobre toda a prova, estas informações são padronizadas para todas as disciplinas. A seção 2 apresenta dados **específicos para cada matéria**. Para selecionar qual matéria você deseja analisar os dados, basta selecioná-la na barra lateral esquerda.")
st.write("Façam bom uso!")

# ! dados gerais !

st.header("**1. Dados sobre a Prova Geral**")

# número de inscritos
# total_presentes = data.Index(['nome'])
# print(total_presentes.value_counts())
total_presentes = 92

# media de pontuação total e porcentagem de acerto
pontuacao_total = pd.read_pickle('dados-relatorio-alunos/pontuacao_total.pkl')

media_pontuacao_total = round(pontuacao_total['Nota total'].mean(),1)


media_porcem_total = str(round(media_pontuacao_total / 1500, 3)*100) + '%'

dados = {
    'Total de Inscritos': [total_presentes],
    'Média de Pontuação Total':[media_pontuacao_total],
    'Média da Porcentagem de Acerto': [media_porcem_total]
}
#st.table(data=dados)
#st.write(pd.DataFrame(dados))


st.subheader("**1.1 Dados sobre as Questões Objetivas**")

# media e % das objetivas 
media_acerto_materia = pd.read_pickle('dados-relatorio-docentes/media_acerto_materia.pkl')
media_acertos_obj = media_acerto_materia['Correção'].mean()

st.write("A média geral de acertos da prova objetiva foi ", str(round(media_acertos_obj, 3)*100)+'%')


# media geral de acertos por materia

def get_media_a_m():
    path = 'dados-relatorio-docentes/media_acerto_materia.pkl'
    return pd.read_pickle(path)
    

st.markdown("**Média de acertos por matéria (em %)**")

media_acerto_materia = get_media_a_m()
media_acerto_materia = media_acerto_materia.reset_index()

# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
media_acerto_materia.set_index('Matéria',inplace=True)

st.write(pd.DataFrame({
   'Média de acertos': media_acerto_materia['Correção']*100
}))

media_acerto_materia = get_media_a_m()

# gráfico com a média de acerto de cada matéria

# o grafico fica com os rotulos na horizontal com as duas linhas a seguir, mas, quando o codigo é upado no servidor do streamlit ele sai todo desconfigurado. 
# caso queira testar para ver se não dá mais o bug, é so "descomentar" as duas linhas a seguir

media_acerto_materia = media_acerto_materia.reset_index()
media_acerto_materia = media_acerto_materia.set_index('Correção')

st.markdown("**Gráfico da porcentagem média de acerto em cada matéria**")
st.bar_chart(data=media_acerto_materia)
st.write("Passando o mouse por cima do gráfico você pode identificar qual é a matéria e nota referentes a cada barra.")

# media e % da redação

media_redacao = pd.read_pickle('dados-relatorio-docentes/media_redacao.pkl')

# tabela com os dados coletados acima
st.subheader("**1.2 Dados sobre a Redação**")
st.write(pd.DataFrame({
    'Nota Média': round(media_redacao,2)
}))


# tabela com a colocação dos alunos

colocacao = pd.read_pickle('dados-relatorio-alunos/colocacao.pkl')
st.subheader("**1.3   Colocação dos alunos do Einstein**")
colocacao.set_index('Colocação',inplace=True)
st.write(pd.DataFrame({
    'Nome': colocacao['Nome'],
    'Pontos': colocacao['Total Acertos'],
    "Porcentagem de Acerto": colocacao['% de acerto']
}))


#  ! dados específicos por matéria  ! 

# questões separadas por materia e por assunto
# # tem o total de acertos, total de alunos que responderam e média de acerto


media_acerto_materia = get_media_a_m()
media_acerto_materia = media_acerto_materia.reset_index()

materia_escolhida = st.sidebar.selectbox("Escolha a matéria", media_acerto_materia['Matéria'])

dados_materia_escolhida = media_acerto_materia[(media_acerto_materia['Matéria'] == materia_escolhida)]

# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
dados_materia_escolhida.set_index('Matéria',inplace=True)

st.header("**2. Dados sobre a Matéria Selecionada**")

st.write("Aqui você encontra dados sobre a matéria que foi selecionada na caixa localizada na aba lateral.")
# st.write("A média em ", str(dados_materia_escolhida.index), " foi ", dados_materia_escolhida['correcao'])
st.write(pd.DataFrame({
    "Média Acertos(em %)": dados_materia_escolhida['Correção']*100
}))



# todas as questões separadas por matéria
# #  tem o total de acertos, total de alunos que responderam e média de acerto
media_acerto_questao = pd.read_pickle('dados-relatorio-docentes/media_acerto_questao.pkl')

st.subheader("**2.1   Média de acertos por questao**")
st.write("Nesta seção são discretizados os acertos por questão")
media_acerto_questao = media_acerto_questao.reset_index()
questao_materia_escolhida = media_acerto_questao[(media_acerto_questao['Matéria'] == materia_escolhida)]


# questao_materia_escolhida["Questão"] = questao_materia_escolhida["Questão"].astype(int)
# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
questao_materia_escolhida.set_index('Questão',inplace=True)


# print(questao_materia_escolhida)
# st.table(data=questao_materia_escolhida[['assunto','dificuldade', 'Média']])


st.write(pd.DataFrame({
    "Assunto": questao_materia_escolhida['Assunto'],
    "Dificuldade": questao_materia_escolhida['Dificuldade'],
    "Total Acertos": questao_materia_escolhida['Total Acertos'],
    # 'Média (em %)': round(questao_materia_escolhida['Média']*100, 1),
    "Tempo Médio(minutos)": questao_materia_escolhida["Tempo"]/60
}))

grafico_questoes = questao_materia_escolhida['Correção','Média']
grafico_questoes = grafico_questoes.reset_index()
grafico_questoes['questao'] = grafico_questoes['Questão'].astype(str)
grafico_questoes["media"] = grafico_questoes['Correção','Média']
# grafico_questoes = grafico.drop(columns=('correcao','Média'))
grafico_questoes.set_index('questao',inplace=True)

st.bar_chart(data=grafico_questoes['media'])
st.write("Dependendo das pontuações das questões, pode ser que o gráfico apresente **escalas diferentes para cada matéria**. Lembre de sempre olhar os valores do eixo vertical.")

# questões separadas por materia e por assunto
# #  tem o total de acertos, total de alunos que responderam e média de acerto

def get_media_p_a():
    path = 'dados-relatorio-docentes/media_por_assunto.pkl'
    return pd.read_pickle(path)
media_por_assunto = get_media_p_a()
# print(media_por_assunto)

media_por_assunto = media_por_assunto.reset_index()
assuntos_materia_escolhida = media_por_assunto[(media_por_assunto['Matéria'] == materia_escolhida)]

# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
assuntos_materia_escolhida.set_index('Assunto',inplace=True)

st.subheader("**2.2   Média de acertos por assunto**")

st.write(pd.DataFrame({
    "Total Acertos": assuntos_materia_escolhida['Correção','Total Acertos'],
    'Total Respostas': assuntos_materia_escolhida['Correção','Total Respostas'],
    'Média (em %)': round(assuntos_materia_escolhida['Correção','Média']*100,3)
}))



# analise dos acertos por dificuldade
media_por_dificuldade = pd.read_pickle('dados-relatorio-docentes/media_por_dificuldade.pkl')

st.subheader("**2.3   Média de acertos por dificuldade**")

media_por_dificuldade = media_por_dificuldade.reset_index()
dificuldade_materia_escolhida = media_por_dificuldade[(media_por_dificuldade['Matéria'] == materia_escolhida)]

# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
dificuldade_materia_escolhida.set_index('Dificuldade',inplace=True)


st.write(pd.DataFrame({
    "Total Acertos": dificuldade_materia_escolhida['Correção','Total Acertos'],
    'Total Respostas': dificuldade_materia_escolhida['Correção','Total Respostas'],
    'Média (em %)': round(dificuldade_materia_escolhida['Correção','Média']*100,3)		
}))