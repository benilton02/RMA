# Descrição do Projeto
A aplicação é projetada para gerenciar um **sistema de RMA (Return Material Authorization)**, que é uma plataforma utilizada para gerenciar devoluções e reparos de produtos defeituosos. O sistema organiza o processo desde a solicitação de devolução, aprovação, triagem e avaliação do item, até a decisão final de reparo, substituição ou reembolso. Ele ajuda as empresas a monitorar cada etapa do retorno de um produto, garantindo a rastreabilidade e a eficiência do processo, além de melhorar a comunicação com os clientes e o controle de estoque.


Este projeto é uma API RESTful desenvolvida com **FastAPI**, que utiliza **JWT** para autenticação e autorização de usuários. O gerenciamento de migrações de banco de dados é feito com **Alembic**, garantindo que o esquema do banco de dados esteja sempre atualizado.

A aplicação usa **PostgreSQL** como banco de dados relacional e **Redis** para caching, melhorando a performance em leituras frequentes e otimizando o tempo de resposta da API.

Além disso, o projeto é containerizado com **Docker** e orquestrado via **Docker Compose**, permitindo fácil implementação e escalabilidade em ambientes de produção e desenvolvimento.

Tecnologias principais:
- **FastAPI** para a construção de APIs rápidas e eficientes.
- **JWT** para autenticação e segurança.
- **Alembic** para migrações de banco de dados.
- **PostgreSQL** como banco de dados relacional.
- **Redis** para caching e gerenciamento de sessões.
- **Docker** e **Docker Compose** para containerização e orquestração.

Este projeto visa fornecer uma base sólida e escalável para construção de APIs seguras e performáticas, otimizando o processo de devoluções e reparos de produtos.


## Configuração do ambiente virtual
- Criar um ambiente virtual para instalação de dependências
 `python3 -v venv venv_project`
- Ativar o ambiente virtual que foi criado
` source venv_project/bin/activate`


## Configuração das variáveis de ambiente
- Criar um arquivo .env e adicionar os seguintes valores
`JWT_SECRET_KEY=secret`
`REDIS_HOST=127.0.0.1`
`REDIS_PORT=6379`
`POSTGRES_HOST=localhost`
`POSTGRES_PORT=5432`
`POSTGRES_USER=postgres`
`POSTGRES_PASSWORD=postgres`
`POSTGRES_HOST=172.17.0.1`
`POSTGRES_DB=postgres`


## Docker-compose.yml
`docker compose up --build -d --remove-orphans`


## Migrações com alembic
- Usar o comando para aplicar as migrações
`alembic upgrade heads`

- Gerar uma nova migração com alembic:
`alembic revision --autogenerate -m '<nome da migração>'` 

## Execução do Backend
- Comando para executar a API
`uvicorn main:app` 
