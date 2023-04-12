#Importando as bibliotecas ncessárias
import openai
import os
import discord
import requests
import json
import random 
import emoji
from keep_alive import keep_alive
from math import *

# chatgpt AI Key  
openai.api_key = "INSERT YOUR KEY"


# Algumas funções úteis para os cálculos

# Calcula a média dos números entregues
# Recebe uma sequência de números. Retorna a média deles
def avg(*numeros):
  return sum(numeros) / len(numeros)


# Calcula a integral definida da função dada em um determinado intervalo, com base na regra do trapézio
# Recebe uma string com a função, e os extremos "a" e "b" do intervalo. Retorna o valor da integral
def integral(function, a, b):
  n = 10000
  h = (b-a)/n
  X = []
  for i in range (0, n+1):
    X.append(a + i * h)
  
  x = X[0]
  soma = eval(function)
  x = X[n]
  soma += eval(function)
  for i in range (1, n):
    x = X[i]
    soma += 2 * eval(function)
  return h / 2 * soma


# Calcula a derivada da função num determinado ponto, usando definição de limite
# Recebe uma string com a função e o ponto desejado. Retorna o valor da derivada
def derivative(function, p):
  h = 10 ** (-13)

  x = p
  f1 = eval(function)

  x = p + h
  f2 = eval(function)

  d = (f2-f1) / (h)
  return d


# Função utilizada pela função solver para resolver uma equação com o Método da Secante
# Recebe uma equação. Retorna o valor adequado de x caso exista. Caso contrário, retorna um texto dizendo que não há soluções
def secant_solver(equation):
  #Divide a equação em lado esquerdo e lado direito, depois manda o lado     direito para o lado esquerdo com o sinal trocado, assim, o objetivo é      encontrar a raíz da equação
  index = equation.find("=")
  f_esq=equation[:index]
  f_dir=equation[index+1:]

  def esq(x):
    f = eval(f_esq)
    return f
    

  def dir(x):
    f = eval(f_dir)
    return f
    

  def function(x):
    f = esq(x)-dir(x)
    return f
    

  # Usando o Método da Secante
  # Altere esses dados para aumentar ou diminuir a precisão do programa
  x0=1
  x1=2
  erro = 1e-06
  iteracoes = 100

  if function(x0) == function(x1):
    k = iteracoes
    x2 = x1
  else:
    x2 = x1-(x1-x0) * function(x1) / (function(x1) - function(x0))
    k = 0

  while abs(function(x2)-function(x1)) > erro and k < iteracoes:
    x0 = x1
    x1 = x2
    x2 = x1 - (x1 - x0) * function(x1) / (function(x1) - function(x0))
    k = k + 1

  if k < iteracoes:
    return round(x2, 6)
  else:
    return "Soluções não encontradas"
  

# Realiza uma conversa com o chatgpt
# Recebe a pergunta a ser feita. Retorna a resposta do chat gpt
def chatgpt(question):
  print('Chamou funcao')
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": question},
        ]
  )
  result = ''
  for choice in response.choices:
    result += choice.message.content
  print(result)
  return result


# Salva uma variável no arquivo variables.txt
# Recebe uma string no formato "variável=valor". Retorna um texto confirmando o registro da variável
def save(variable):
  variable = variable.replace(" ", "")
      
  with open("variables.txt", "a") as file:
    file.write(f"{variable}\n")
  return f"Variable {variable} successfully saved"


# Deleta uma variável do arquivo variables.txt
# Recebe o nome da variável. Retorna uma mensagem confirmando se foi possível deletar a mensagem ou não
def delete(var):
  var = var.replace(" ", "")
  with open("variables.txt", "r") as file:
    lines = file.readlines()

  deleted = False
  with open("variables.txt", "w") as file:
    for line in lines:
      if f"{var}=" not in line:
        file.write(line)
      else:
        msg = "Variable " + line.strip("\n") + " successfully deleted"
        deleted = True
  if not deleted:
    msg = f"Variable {var} not found"
  return msg


# Deleta todas as variáveis do arquivo variables.txt
# Não recebe um input valioso. Retorna uma mensagem confirmando a deleção
def delete_all(_):
  with open("variables.txt", "w") as file:
    file.truncate(0)
  return f"All variables sucessfully deleted"


# Mostra todos as variáveis e seus valores do arquivo variables.txt
# Não recebe um input valioso. Retorna o conteúdo do arquivo variables.txt
def show(_):
  with open("variables.txt", "r") as file:
    return file.read()


# Resolve uma equação (com =) ou uma expressão matemática (sem =)
# Recebe uma string com a equação/expressão. Retorna o resultado dela
def solve(equation):
  with open("variables.txt") as file:
    variables = file.readlines()
    for variable in variables:
      variable = variable.strip("\n")
      if ("[" + (variable.split("="))[0] + "]") in equation:
        equation = equation.replace(("[" + (variable.split("="))[0] + "]"), (variable.split("="))[1])
  if "=" not in equation:
    answer = round(float(eval(equation)),6)
  else:
    answer = secant_solver(equation)
  return f"= {answer}"


# Começando o bot
TOKEN = os.environ['SENHA']
client = discord.Client()


@client.event
# Anuncia que o bot iniciou
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  #Para que o bot não se responda
  if message.author == client.user:
    return


  #Transferindo a linguagem matemática utilizada para a linguagem do python
  msg = message.content
  msg = msg.replace("^", "**")


  # Caso mensagem comece com um dos sufixos, é um comando
  # Caso contrário, ignorar mensagem
  with open("sufixes.txt") as file:
    sufixes = file.read().splitlines()
  if msg[0] in sufixes:
    msg = msg[1:]
  else:
    return

  # Procura função utilizada
  # Se não é uma função válida, ignorar mensagem
  with open("functions.txt") as file:
    functions = file.read().splitlines()
    found = False
    for function in functions:
      if msg.find(function) != -1:
        found = True
        break
  if not found:
    return

  # Coloca os " necessários para rodar as funções
  first = msg.find("(") 
  last = msg.rfind(")")
  msg = msg[0:first+1] + '"' + msg[first+1:last] + '")'


  # Chama a função desejada e mostra a mensagem
  answer = eval(msg)
  await message.channel.send(answer)

#Faz o bot continuar rodando
keep_alive()
client.run(TOKEN)


