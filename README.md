# Hooki
🪝 Executor de tarefas por web triggers


# 🔌 Setup
- Clone o repositório
- Crie um ambiente virtual e instale as dependências: 
    - Com Poetry: 
      - ```sh
        poetry install
        ```
    - Com pip
      - ```sh
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        ```
- Configurando variáveis de ambiente:
  - Clone o `local.env` para `.env`
    - ```sh
      cp local.env .env
      ```
    - add uma `SECRET_KEY` e um `URL_PREFIX`
    (Obs: `URL_PREFIX` define em que endpoit a aplicacao vai rodar,
    Ex: seu dominio e `https://forbar.com/` e seu `URL_PREFIX=/hooki` a aplicao estara disponivel em `https://forbar.com/hooki/` )
- Iniciando o banco local:
  - ```sh
    flask db upgrade
    ```
    (Obs: Nesse estágio de desenvolvimento, estamos usando sqlite3. Mas sinta-se avontade para usar o banco de sua preferencia, configurando em `app.py`)
- Criando o usuário `root`:
  - ```sh
    flask auth create-user <USERNAME>
    ```
- Rodando a aplicação:
  - ```sh
    gunicorn --bind 0.0.0.0:5000 'app:create_app()'
    ```
    A aplicação estará rodando no `localhost:5000` 
- Apontando o Nginx:
    ```sh
    server {

        listen 80;

        location / {
            ...
        }

        location <URL_PREFIX> {
            proxy_pass http://localhost:5000;
        }
    }
    ```
