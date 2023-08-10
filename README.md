# Documentação das APIs de Atendimento ao Cliente

Este documento descreve as APIs de atendimento ao cliente fornecidas pelo serviço Segurozinho. Essas APIs permitem que os clientes interajam com os agentes de atendimento de maneira eficiente e obtenham respostas para suas perguntas.

# Escopo

O projeto tem como objetivo desenvolver uma solução abrangente para melhorar o atendimento ao cliente em um ambiente de Serviço de Atendimento ao Cliente (SAC) online. A solução abordará o desafio de identificar a demanda do cliente e automatizar o processo de correspondência com scripts de atendimento apropriados. Além disso, será implementado um bot de conversação alimentado por um modelo de linguagem livre (LLM) capaz de interagir naturalmente com os clientes para coletar informações relevantes.

O escopo abrange os seguintes aspectos:

  1. Correspondência Automática de Scripts:
      - Desenvolver um sistema de correspondência automática que identifica a demanda do cliente com base nas mensagens iniciais.
      - Realizar um match entre a demanda identificada e os scripts de atendimento pré-definidos.

  2. Bot de Conversação:
      - Implementar um bot de conversação alimentado por um modelo de linguagem livre (LLM), como o GPT-3.5.
      - Configurar o bot para interagir de forma natural e contextual com os clientes, respondendo a perguntas e coletando informações.

  3. Integração com Atendentes Humanos:
      - Permitir que os atendentes revisem, escolham ou ajustem o script correspondente, se necessário.

  4. Gerenciamento de Scripts:
      - Criar uma estrutura para armazenar scripts de atendimento, incluindo perguntas e diretrizes apropriadas.
      - Possibilitar a adição, edição e remoção de scripts por administradores.

  5. Plataforma de Atendimento (CHAT):
      - Integrar a solução com a Interface de Usuário desenvolvida, garantindo uma experiência de usuário contínua.

  6. Implantação e Monitoramento:
      - Implantar a solução em um ambiente de produção, usando contêineres Docker e hospedagem em nuvem.


O resultado final será uma aplicação eficiente e automatizada que melhora a interação entre os atendentes, o bot de conversação e os clientes, aprimorando significativamente o processo de atendimento ao cliente no contexto de um chat de SAC online.

# Problema a ser resolvido

No contexto em que um usuário acessa um chat de atendimento em um site, a tarefa do atendente é compreender a demanda do cliente e selecionar o script de atendimento apropriado para orientar a conversa. Esse script contém uma série de perguntas e diretrizes para conduzir o atendimento de forma eficaz, além de informar o cliente sobre as informações necessárias para a resolução do problema.

O desafio reside em automatizar o processo de identificação da demanda do cliente e realizar um match automático com o script de atendimento correto. Após a identificação, o projeto busca implementar um bot de conversação que interage com o cliente usando linguagem natural. Esse bot, baseado em um modelo de linguagem livre (LLM), tem como objetivo capturar informações importantes do cliente de maneira natural e fluida, melhorando a experiência do atendimento.

A solução proposta visa otimizar a eficiência e a qualidade do atendimento ao cliente, automatizando a correspondência com scripts de atendimento e tornando a interação com o bot de conversação mais próxima da comunicação humana.

# Tecnologias utilizadas

O projeto utiliza:

  - FastAPI: Criação eficiente de APIs.
  - MongoDB: Armazenamento flexível de dados.
  - MongoDB Atlas: Banco de dados gerenciado em nuvem.
  - Docker e DockerHub: Empacotamento consistente.
  - GitHub Actions: Automação de integração e entrega.
  - Google Cloud Run: Implantação escalável em nuvem.
  - LangChain: O LangChain da OpenAI enriquece a geração de texto e interação com os usuários, permitindo direcionar conversas com tópicos específicos e instruções detalhadas.

Essas tecnologias são combinadas para criar uma aplicação escalável e eficiente que lida com scripts e mensagens.

# Executar projeto

Completar com a sua **OPENAI KEY** no arquivo **docker-compose.yml**

```yaml
  backend:
    container_name: backend 
    build: 
      context: .
      dockerfile: Dockerfile.backend
    environment:
      - OPENAI_API_KEY= # Your OPENAI KEY
      - DB_HOST_DEV=mongo
      - DB_PASSWORD_DEV=example
      - DB_DATABASE_DEV=customer-care-db
      - DB_PORT_DEV=27017
      - DB_USER=localhost
      - ENV=dev
    ports: 
      - 8000:8080 
    restart: always
```

Para Executar todo o projeto em containers, execute o comando abaixo no terminal para subir o compose.

```bash
docker-compose -f docker-compose.yml up -d
```
Depois para inserir os scripts na base de dados.

```bash
python3 start_db.py
```

Acessar o frontend.

`http://localhost:8080`

# Frontend

## Base URL

`http://localhost:8080`

## Recursos Disponíveis

### Iniciar Conversa

Inicia uma nova conversa com um agente de atendimento.

- **URL:** `/initial-message`
- **Método:** POST

#### Parâmetros da Solicitação

Nenhum

#### Corpo da Solicitação

```json
{
    "message": "Nome do Cliente"
}
```
Resposta de Sucesso

Código de status: 200 OK


```json
{
    "answer": "Por favor, informe em poucas palavras como posso ser útil para você hoje.",
    "Name": "Nome do Cliente",
    "Session": "ID da Sessão"
}
```

Resposta de Erro

Código de status: 400 Bad Request

```json
{
    "status": "Error",
    "message": "Mensagem de erro"
}
```

## Enviar Mensagem de Chat

Envia uma mensagem do cliente para o agente de atendimento.

- **URL:** `/chat`
- **Método:** POST

Parâmetros da Solicitação

Nenhum

**Corpo da Solicitação**

```json
{
    "message": "Mensagem do Cliente"
}
```

Resposta de Sucesso

Código de status: 200 OK

```json
{
    "answer": "Resposta do Bot",
    "steps": "Passos realizados",
    "is_final_step": "True/False"
}
```

Resposta de Erro

Código de status: 400 Bad Request

```json
{
    "status": "Error",
    "message": "Mensagem de erro"
}
```

Enviar Mensagem de Chat com IA

Envia uma mensagem do cliente para o agente de atendimento com processamento de IA.

- **URL:** `/chat_ai`
- **Método:** POST

**Parâmetros da Solicitação**

- Nenhum

**Corpo da Solicitação**

```json
{
    "message": "Mensagem do Cliente"
}
```

Resposta de Sucesso

Código de status: 200 OK

```json
{
    "answer": "Resposta da IA"
}
```

Resposta de Erro

Código de status: 400 Bad Request

```json
{
    "status": "Error",
    "message": "Mensagem de erro"
}
```

Página Inicial

Exibe a página inicial do sistema de atendimento ao cliente.

- **URL:** `/`
- **Método:** GET

Parâmetros da Solicitação

Nenhum
Resposta

Renderiza o arquivo de template "index.html" para exibir a página inicial.
Observações

- As APIs requerem autenticação via cookie, usando o ID da sessão.
- Certifique-se de tratar adequadamente os erros retornados pelas APIs.
- As URLs mencionadas nas APIs são exemplos e devem ser substituídas pela URL real da API.

# Backend

## **Chat**



## **CRUD**

## Scripts

### Get All Scripts

Get a list of all scripts.

**Request:**

- Method: GET
- Endpoint: `/api/v1/script`

**Response:**

- Status Code: 200 OK
- Content:
  ```json
  {
    "scripts": "Serialized scripts data"
  }
  ```

### Insert Script

Insert a script.

**Request:**

- Method: POST
- Endpoint: `/api/v1/script`
- Body:
  ```json
    {
        "args": "Script data"
    }
    ```
