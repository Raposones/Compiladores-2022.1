# Conversor NFA -> DFA + Analisador Léxico para Linguagem C
##  Trabalho de Compiladores - 2022.1

<br>

* Aluno: Raphael Carvalho Garcia
* Matrícula: 412557

<br>

### **1. Conteúdo**
Estão presentes cinco arquivos, sendo eles:
* Um arquivo de texto *Tokens_ERs.txt* contendo 
os tokens da linguagem C, e suas respectivas ERs - **questão 1**;

* Um arquivo *C_nfa.jff* contendo o automato da linguagem C - **questão 2** (deve ser aberto com o programa JFLAP);

* Um arquivo *JFLAP.jar* contendo o programa JFLAP (para analisar e rodar o automato);

* Dois arquivos em Python: *NFAtoDFA.py* e *DFAreader.py*, contendo, respectivamente, códigos auxiliares e o programa principal.

<br>

### **2. Instruções**
Deve-se fornecer um código da linguagem C, para que seja feita sua análise léxica. Apenas o arquivo *DFAreader* precisa ser executado, já que ele fornece a análise sintática de um código dado.
<br>
O código em C é fornecido por meio de um input **infinito**. O input é parado ao apertar **CTRL + D**.
<p>
É retornado ao usuário, em uma única linha, cada token do código dado, em ordem.

<br>

### **3. Métodos/Funções**
#### **-> NFAtoDFA.py**

~~~ python
bold(str)
underline(str)
~~~

Funções que recebem uma string e retornam a mesma string, em negrito (bold) ou sublinhada (underline). Servem apenas para deixar o output mais bonitinho :)

<br>

~~~python
isNondeter(state) 
~~~

Função que recebe um estado de um automato. Retorna *True* caso o estado seja não-deterministico, e *False* caso contrário.

<br>

~~~python
toDfa(nfa)
~~~

Função que recebe um automato NFA, e retorna um automato DFA.

<br>

~~~python
printAutom(auto)
~~~

Método que recebe um automato, e retorna o mesmo automato em um formato de fácil leitura

<br>

~~~python
returnDFA(nfa)
~~~

Função auxiliadora que recebe um automato NFA e retorna o mesmo automato em DFA, utilizando a função *toDFA*

<br>

#### **-> DFAreader.py**

~~~ python
get_string()
~~~

Função que recebe uma string infinitamente por meio de um input, a cada ENTER, e para ao ser teclado CTRL + D. 
Retorna a string convertida em uma lista contendo cada sub-string separadamente (para facilitar a análise léxica)

<br>

### **4. Info. Adicional**
* **Importante:** Após cada linha, deve-se apertar ENTER para que cada linha seja inserida na análise.

* Para terminar de ler o código, aperte **CTRL + D**!

* O automato NFA já é fornecido dentro do código por meio de um dicionário.

* A função *isNondeter(state)* do arquivo *NFAtoDFA.py* considera apenas casos onde há ligações com ε (épsilon), já que é o único caso existente no automato NFA dado.