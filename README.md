# Lista Todo + CRUD com PyQt5 e <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/SQLite370.svg/1200px-SQLite370.svg.png" alt="SQLite" width="90">

Interface gráfica em Python utilizando a biblioteca PyQt5 para a construção de uma lista todo com as operações CRUD (Create, Read, Update, Delete). 
Além de permitir que o usuário adicione, visualize, edite e remova atividades, a aplicação possui um banco de dados integrado utilizando a lib sqlite3 do Python. 

> Status do Projeto: ✔️ (concluído)

## 🔧 Tecnologias utilizadas
Python V.: 3.11.1 || PyQt5 V.: 5.15.9

## ⚙️ Configurando o ambiente virtual
* No seu terminal, navegue até a pasta raiz do projeto e execute o seguinte comando para criar um ambiente virtual:

  ```bash
  python -m venv nome_da_virtualenv
  ```

* Rode o comando de acordo com seu sistema para ativar seu ambiente virtual:

  Windows
  ```bash
  .\nome_da_virtualenv\Scripts\activate
  ```

  Linux ou macOS
  ```bash
  source nome_da_virtualenv/bin/activate
  ``` 

## 🧑‍🔬 Instalando as dependências
* Com o ambiente virtual **ativado**, instale as dependências do projeto com o seguinte comando:

  ```bash
  pip install -r requirements.txt
  ```

## 🚀 Executando o projeto
* Execute o arquivo principal da lista conforme abaixo:

  ```bash
  python main.py
  ```

## 🗄️ Sobre o banco de dados
* Basta adicionar uma tarefa na aplicação e um banco de dados <code>tasks.db</code> é gerado automaticamente com as tarefas inclusas nele.

  **Obs.:** Para cada alteração na aplicação, lembre-se de atualizar o arquivo fechando-o e abrindo-o novamente. Caso esteja com algum gerenciador de banco de dados, apenas aperte F5 para atualizá-lo.
