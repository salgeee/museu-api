# API do Museu da Computação

## Descrição

Esta é a API para o sistema do Museu da Computação, desenvolvida com FastAPI. Ela fornece endpoints para autenticação, gerenciamento de usuários e gerenciamento de notícias.

## Tecnologias Utilizadas

* **Backend:** Python, FastAPI
* **Banco de Dados:** SQLAlchemy (com suporte para SQLite e PostgreSQL)
* **Validação de Dados:** Pydantic
* **Autenticação:** JWT (JSON Web Tokens) com `python-jose` e `passlib`
* **Servidor ASGI:** Uvicorn

## Funcionalidades

* Autenticação de usuários com OAuth2.
* CRUD (Criar, Ler, Atualizar, Deletar) completo para Usuários (apenas administradores).
* CRUD completo para Notícias (apenas administradores).
* Documentação de API interativa e automática com Swagger UI e ReDoc.

## Pré-requisitos

Antes de começar, você precisará ter o seguinte instalado em sua máquina:
* Python 3.10 ou superior
* pip (gerenciador de pacotes do Python)

## Como Rodar o Projeto

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### 1. Clone o Repositório

Primeiro, clone o repositório para a sua máquina local (se o código estiver em um repositório git) ou simplesmente descompacte os arquivos em uma pasta de sua preferência.

```bash
git clone https://github.com/salgeee/museu-api.git
cd museu-api
````

### 2\. Crie e Ative um Ambiente Virtual

É uma boa prática usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```

### 3\. Instale as Dependências

Com o ambiente virtual ativado, instale todas as dependências listadas no arquivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4\. Configure as Variáveis de Ambiente

O projeto utiliza um arquivo `.env` para gerenciar as configurações. Você pode copiar o arquivo de exemplo `.env.example` e renomeá-lo para `.env`.

```bash
# Copie o arquivo de exemplo
cp .env.example .env
```

Para uma configuração inicial rápida, o projeto pode rodar com um banco de dados **SQLite** sem a necessidade do Docker. Para isso, você pode deixar a variável `DATABASE_URL` no arquivo `.env` comentada ou removê-la, pois o sistema usará o valor padrão definido no código.

Para um ambiente mais robusto, veja a seção sobre Docker abaixo.

### 5\. Execute a Aplicação

Agora você pode iniciar a API. O projeto inclui um arquivo `run.py` para facilitar.

```bash
python run.py
```

O servidor será iniciado e estará acessível em `http://127.0.0.1:8000`.

Ao iniciar, a aplicação criará o banco de dados e um usuário administrador padrão. As credenciais para este usuário são definidas no arquivo de configuração `app/core/config.py`.

**É altamente recomendável que você altere essas credenciais padrão, especialmente se a aplicação for exposta de alguma forma.** Você pode fazer isso alterando os valores diretamente no arquivo de configuração ou, preferencialmente, através de variáveis de ambiente no seu arquivo `.env`.

-----

### (Opcional) Rodando o Banco de Dados com Docker e PostgreSQL

Para um ambiente de desenvolvimento mais robusto e similar a um ambiente de produção, é recomendado utilizar um banco de dados PostgreSQL rodando em um contêiner Docker. O projeto já está preparado para essa configuração.

**Pré-requisitos:**

  * Docker e Docker Compose instalados.

**1. Crie um arquivo `docker-compose.yml`**
Na raiz do projeto, crie um arquivo `docker-compose.yml` com o seguinte conteúdo:

```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    container_name: museu_db_postgres
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=docker
      - POSTGRES_DB=museu_db
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data/

volumes:
  postgres_data:
```

**2. Inicie o Contêiner**
No seu terminal, na raiz do projeto, execute:

```bash
docker-compose up -d
```

Este comando iniciará o contêiner do PostgreSQL em segundo plano.

**3. Verifique o arquivo `.env`**
Garanta que o seu arquivo `.env` está configurado para usar o PostgreSQL, utilizando a variável `DATABASE_URL`:

```
DATABASE_URL=postgresql://postgres:docker@localhost:5433/museu_db?client_encoding=utf8
```

**4. Rode a API**
Com o contêiner do banco de dados rodando, inicie a API normalmente:

```bash
python run.py
```

A aplicação irá se conectar ao banco de dados PostgreSQL dentro do contêiner Docker.

-----

## Acessando a Documentação da API

Após iniciar a aplicação, você pode acessar a documentação interativa da API (Swagger UI) no seu navegador:

[http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)

Você também pode ver uma documentação alternativa (ReDoc) em:

[http://127.0.0.1:8000/redoc](https://www.google.com/search?q=http://127.0.0.1:8000/redoc)

Nessas páginas, você pode visualizar todos os endpoints disponíveis, seus parâmetros e respostas, além de testá-los diretamente.

## Estrutura do Projeto

```
/app
|-- /api
|   |-- /endpoints
|   |   |-- auth.py
|   |   |-- news.py
|   |   `-- users.py
|   `-- api.py
|-- /core
|   |-- config.py
|   |-- dependencies.py
|   `-- security.py
|-- /db
|   |-- database.py
|   `-- init_db.py
|-- /models
|   |-- news.py
|   `-- user.py
|-- /schemas
|   |-- news.py
|   |-- token.py
|   `-- user.py
`-- main.py
/requirements.txt
/run.py
```

```
```
