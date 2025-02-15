# ProcessoSeletivoStract2025

Uma API local, desenvolvida em Python+Flask, que transforma dados brutos de contas de anúncios em relatórios organizados e fáceis serem consumido por um frontend. 🚀

## Introdução

O **ProcessoSeletivoStract2025** é um projeto desenvolvido como parte de um desafio técnico de processo seletivo.

A proposta foi criar uma API local capaz de consumir dados de "plataformas de anúncios", gerar novos endpoints e integrá-los com um frontend.

Utilizando **Python** e **Flask** no backend e **React** no frontend, o projeto permite uma análise eficiente e organizada de dados de anúncios. 🚀

## Requisitos

Este projeto utiliza dependências específicas para o backend (Python + Flask) e o frontend (React). Antes de começar, certifique-se de ter os seguintes requisitos instalados:

### Requisitos Gerais

-   **Python** (versão 3.8 ou superior)
-   **Node.js** (versão 16 ou superior)
-   **npm** (ou **yarn**, dependendo do gerenciador de pacotes preferido)

### Backend

As dependências do backend estão listadas no arquivo `requirements.txt`. Elas incluem:

-   Flask==3.1.0
-   Flask-Cors==5.0.0
-   pandas==2.2.3
-   requests==2.32.3
-   python-dotenv==1.0.1
-   E outras necessárias para o funcionamento do servidor. Consulte o arquivo completo.

### Frontend

As dependências do frontend estão especificadas no arquivo `package.json`. Algumas das principais incluem:

-   **React**: ^19.0.0
-   **React Router DOM**: ^7.1.5
-   **Axios**: ^1.7.9
-   **React Scripts**: 5.0.1

### Observação

Certifique-se de instalar as dependências corretamente utilizando os comandos descritos na seção [Instalação](#instalação).

## Instalação

Para instalar as dependências do projeto, você pode escolher entre usar o script automatizado `run_project.sh` ou realizar os passos manualmente. Siga uma das opções abaixo:

### 1. Usando o Script

O script `run_project.sh` automatiza o processo de instalação das dependências do backend e frontend. Certifique-se de ter o Bash instalado e execute os comandos abaixo no terminal:

1. Dê permissão de execução ao script (se ainda não tiver feito isso):
   chmod +x run_project.sh

2. Execute o script com a opção `install` para instalar todas as dependências:
   ./run_project.sh install

3. (Opcional) Para instalar as dependências e iniciar o projeto imediatamente, use:
   ./run_project.sh all

### 2. Manualmente

Se preferir instalar as dependências manualmente, siga os passos abaixo:

#### Backend

1. Navegue até o diretório do backend:
   cd backend

2. Crie um ambiente virtual:
   python -m venv venv

3. Ative o ambiente virtual:

    - **Linux/macOS**:
      source venv/bin/activate
    - **Windows** (Git Bash ou Prompt de Comando):
      source venv/Scripts/activate

4. Instale as dependências listadas no `requirements.txt`:
   pip install -r requirements.txt

5. Volte ao diretório raiz:
   cd ..

#### Frontend

1. Navegue até o diretório do frontend:
   cd frontend

2. Instale as dependências usando npm:
   npm install

3. Volte ao diretório raiz:
   cd ..

Agora o projeto está pronto para ser executado! Consulte a próxima seção [Uso](#uso) para mais detalhes.

## Uso

Após instalar as dependências, o projeto pode ser executado de duas formas: utilizando o script `run_project.sh` ou iniciando manualmente os servidores do backend e frontend.

### 1. Iniciar usando o script

Para iniciar o backend e o frontend simultaneamente, utilize o seguinte comando:
./run_project.sh start

Esse comando irá iniciar:

-   O backend no endereço: **http://localhost:5000**
-   O frontend no endereço: **http://localhost:3000**

Caso prefira iniciar apenas um dos serviços manualmente, siga os passos abaixo:

-   **Para o backend**:

    1. Navegue até o diretório `backend`:
       cd backend
    2. Ative o ambiente virtual:
        - **Linux/macOS**:
          source venv/bin/activate
        - **Windows** (Git Bash ou Prompt de Comando):
          source venv/Scripts/activate
    3. Inicie o servidor Flask:
       flask --app main run
       O backend estará disponível em: **http://localhost:5000**

-   **Para o frontend**:
    1. Navegue até o diretório `frontend`:
       cd frontend
    2. Inicie o servidor React:
       npm start
       O frontend estará disponível em: **http://localhost:3000**

### 2. Como acessar os endpoints principais

O backend do projeto está disponível em **http://localhost:5000** e fornece os seguintes endpoints:

#### **1. `/`**

-   **Descrição**: Retorna meus dados pessoais.
-   **Resposta esperada**: Um JSON com seu nome, email e link para o LinkedIn.

#### **2. `/{{plataforma}}`**

-   **Descrição**: Retorna um JSON onde cada linha representa um anúncio veiculado na plataforma especificada.
-   **Exemplo de uso**:
    -   Para a plataforma "Facebook Ads":
        http://localhost:5000/meta_ads
    -   Para a plataforma "Google Analytics":
        http://localhost:5000/ga4
    -   Para a plataforma "TikTok":
        http://localhost:5000/tiktok_insights

#### **3. `/{{plataforma}}/resumo`**

-   **Descrição**: Retorna um JSON, colapsando todas as linhas relacionadas à mesma conta em uma única linha.
    -   Os dados numéricos são somados, enquanto os campos de texto ficam vazios (exceto o nome da conta).
-   **Exemplo de uso**:
    -   Para a plataforma "Facebook Ads":
        http://localhost:5000/meta_ads/resumo
    -   Para a plataforma "Google Analytics":
        http://localhost:5000/ga4/resumo
    -   Para a plataforma "TikTok":
        http://localhost:5000/tiktok_insights/resumo

#### **4. `/geral`**

-   **Descrição**: Retorna todos os anúncios de todas as plataformas em um JSON.
-   **Informação adicional**:
    -   Adiciona uma coluna para identificar o nome da plataforma.
    -   Calcula o "Cost per Click" para o Google Analytics (dividindo `spend` por `clicks`).

#### **5. `/geral/resumo`**

-   **Descrição**: Retorna um JSON com todos os anúncios de todas as plataformas, mas agrupando todas as linhas da mesma plataforma em uma única linha.
    -   Os dados numéricos são somados, e os campos de texto ficam vazios (exceto o nome da plataforma).

### Plataformas Suportadas

Os valores aceitos para o parâmetro `{{plataforma}}` são:

-   **Facebook Ads**: `meta_ads`
-   **Google Analytics**: `ga4`
-   **TikTok**: `tiktok_insights`

-   **Para o frontend**:

O frontend do projeto está disponível em **http://localhost:3000** e oferece uma interface interativa para acessar os dados gerados pelo backend.

#### Funcionalidades do Frontend

-   **Seleção de plataforma via dropdown**:
    -   Escolha entre as plataformas suportadas:
        -   **Facebook Ads**: `meta_ads`
        -   **Google Analytics**: `ga4`
        -   **TikTok**: `tiktok_insights`
-   O frontend se comunica diretamente com os endpoints do backend para buscar e exibir os dados em tempo real.

#### Endpoints acessados pelo frontend

Os seguintes endpoints são consumidos dinamicamente pelo frontend:

-   **`http://localhost:5000/`**: Retorna meus dados pessoais.
-   **`http://localhost:5000/plataforma`**: Exibe os anúncios da plataforma selecionada.
-   **`http://localhost:5000/plataforma/resumo`**: Exibe os dados agregados por conta da plataforma selecionada.
-   **`http://localhost:5000/geral`**: Exibe todos os anúncios de todas as plataformas.
-   **`http://localhost:5000/geral/resumo`**: Exibe os dados agregados de todas as plataformas.

#### Como usar o frontend

1. Navegue até **http://localhost:3000** no navegador.
2. Selecione uma plataforma no dropdown.
3. O frontend exibirá os dados correspondentes consumindo o backend.

> **Nota:** O frontend é ideal para quem deseja uma experiência mais visual e amigável ao invés de interagir diretamente com o backend.

## Estrutura do Projeto

Abaixo está a estrutura de diretórios e arquivos do projeto:

### Descrição dos Diretórios e Arquivos

```console
.
├── backend
│   ├── main.py
│   ├── requirements.txt
│   └── ...         # Outros arquivos do backend
├── frontend
│   ├── package.json
│   └── ...         # Outros arquivos do frontend
├── run_project.sh  # Script para instalar e iniciar o projeto
└── README.md       # Este arquivo
```

-   **`backend/`**: Contém o código do servidor backend, implementado com Python e Flask.

    -   **`main.py`**: Arquivo principal do backend, onde os endpoints da API são definidos.
    -   **`requirements.txt`**: Lista de todas as bibliotecas e dependências necessárias para o backend.

-   **`frontend/`**: Contém o código do aplicativo frontend, implementado com React.

    -   **`package.json`**: Lista de dependências do frontend e scripts para gerenciar o projeto.

-   **`run_project.sh`**: Script Bash para instalar as dependências e iniciar os servidores do backend e frontend.

-   **`README.md`**: Este arquivo, contendo a documentação do projeto.

Essa organização facilita o gerenciamento e a navegação pelo projeto. Cada parte está separada para manter o código backend e frontend modular e organizado.
