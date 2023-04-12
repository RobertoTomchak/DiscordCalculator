# DiscordCalculator
Um bot de Discord que funciona como calculadora. Ele é capaz de resolver expressões matemáticas e equações usando diversos tipos de funções e variáveis, além de permitir conversas com o chat GPT.
Esse bot foi inspirado no vídeo do canal freeCodeCamp, disponível no seguinte link: https://youtu.be/SPTfmiYiuok.

## Arquivos
Esse repositório contém 2 arquivos em Python e 3 arquivos txt:
-main.py: possui a maioria das aplicações relevantes do bot;
-keep_alive.py: permite o bot continuar rodando;
-sufixes.txt: possui uma lista com os sufixos utilizados pelo bot. Caso queira adicionar um novo, simplesmente o adicione nesse arquivo numa nova linha;
-functions.txt: possui o nome das funções que o bot pode chamar, como save, solve, etc;
-variables.txt: salva as variáveis e seus respectivos valores para serem utilizadas nos cálculos.

## Como funciona
### Chamando funções
Qualquer mensagem que comece com um sufixo válido (por exemplo ".") seguido de uma função válida (por exemplo, "solve") será chamada e o bot tentará resolvê-la. Por exemplo, caso o usuário mande mensagem:
  .solve(1+2)
O bot irá retornar "= 3.0"
Não é necessário usar aspas dentro das funções, exceto por funções que estejam dentro delas (exemplo: a função derivative recebe uma função matemática como argumento, e esta deve estar entre aspas).

O bot também é capaz de resolver equações. Por exemplo, se o usuário mandar a seguinte mensagem:
  .solve(x^2=5)
O bot irá enviar como resposta "= 2.236068".
#OBS: note que a incógnita deve ser x para ser resolvida. Não é possível usar outras letras (e nem X maiúsculo) como incógnitas, e nem mais de uma incógnita ao mesmo tempo).

### Usando variáveis
O bot também permite o uso de variáveis representadas por nomes. Por exemplo, se o usuário digitar ".save(h=2)", o bot irá salvar esse valor em variables.txt. Assim, o usurário pode utilizá-la em outras expressões, contanto que ela esteja entre colchetes ([]). Por exemplo, caso o valor de h tenha sido salvado como 2, ao receber a seguinte mensagem:
  .solve([h]*x=3)
O bot irá retornar "= 1.5".

### Chat GPT
O bot também é capaz de conversar com o chat GPT. Para isso, é preciso digitar a sua API Key no campo indicado do código (na linha 13 do main.py). Para obtê-la, basta criar uma conta no site do OpenAI (https://openai.com/). Existe uma amostra grátis; entretanto, após alguns usos, será necessário pagar (se você utilizar bem pouco o bot, provavelmente não terá que se preocupar com isso).

### Outras questões
Questões sobre como o bot é integrado ao Discord e como mantê-lo rodando num servidor estão muito bem explicadas no vídeo mencionado o começo desse arquivo. Entretanto, infelizmente não há legenda em português no vídeo, apenas em inglês.

### Cuidados
De maneira geral, o bot é extremamente preciso para resolver equações/expressões simples. Entretanto, ele pode ter erros de precisão com equações mais complexas (que envolvam exponenciais e derivadas, por exemplo) e com valores muito altos (devido às limitações da própria linguagem Python). Sendo assim, verifique as tolerâncias de erro e as limitações das funções antes de utilizá-las.
Além disso, obviamente, o próprio chatGPT não é uma fonte confiável de informações, então não considere todas suas respostas como verdade.


