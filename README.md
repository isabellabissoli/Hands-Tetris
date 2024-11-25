# Jogar o jogo
Quando o código é executado, ele já começa a se comunicar com o teclado, sendo assim, bastar inicia o código utilizando o comando 
```ruby
python AIPlayGame.py
```
e depois iniciar o jogo, ele já estará funcionando apenas com os gestos

# Terminar com o código
Para encerar o código, basta clicar nas teclas Crtl + C

# Biblioteca utilizada para acessar o teclado - Pynput
Essa biblioteca é capaz de controlar tanto mouse quanto o teclado, inicializando isso através da inicialização do Controller de dentro da bibliioteca

Como iremos apenas trabalhar com o teclado, os comendos de dentro da biblioteca que podemos usar são

**.press('Tecla')**: preciona a tecla
**.release('Tecla')**: solta a tecla
(Antes do ponto sempre colocar o nome que deu para o Controller)

## Curiosodade
Se quiser que digite o código sozinho basta usar **.type("Frase da sua escolha")**

Como iremos usar as setas, temos que usar o Key antes (Toda vez que não for alguma tecla numerica ou alguma letra)
exemplo: **.press(Key.left)** - seta pra esquerda

É possivel usar uma junção de teclas também, utilizando o .**pressed()**
