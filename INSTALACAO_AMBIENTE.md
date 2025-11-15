# Instalação Completa do Ambiente - Do Zero ao Pipeline Funcionando

Este guia cobre desde a instalação do Conda até a execução completa do pipeline.

## Pré-requisitos

- **Sistema Operacional**: Windows 10/11, Linux ou macOS
- **RAM**: Mínimo 8GB (recomendado 16GB)
- **Espaço em Disco**: Mínimo 10GB livres
- **Conexão com Internet**: Para download de dependências

---

## Parte 1: Instalar Conda (se não tiver)

### Opção A: Instalar Miniconda (Recomendado - Mais leve)

#### Windows:
1. **Baixe o instalador**:
   - Acesse: https://docs.conda.io/en/latest/miniconda.html
   - Baixe: `Miniconda3 Windows 64-bit`

2. **Execute o instalador**:
   - Duplo clique no arquivo `.exe` baixado
   - Aceite os termos
   - Escolha "Just Me" (recomendado)
   - Deixe o caminho padrão: `C:\Users\<seu_usuario>\miniconda3`
   - **IMPORTANTE**: Marque "Add Miniconda3 to my PATH environment variable"
   - Clique em "Install"

3. **Verifique a instalação**:
   ```bash
   # Abra um novo terminal (PowerShell ou CMD)
   conda --version
   # Esperado: conda 23.x.x ou superior
   ```

#### Linux/Mac:
```bash
# Baixar instalador
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Executar instalador
bash Miniconda3-latest-Linux-x86_64.sh

# Seguir instruções no terminal
# Aceitar licença: yes
# Confirmar localização: Enter
# Inicializar conda: yes

# Recarregar shell
source ~/.bashrc

# Verificar
conda --version
```

### Opção B: Instalar Anaconda (Completo - Mais pesado)

1. Acesse: https://www.anaconda.com/products/distribution
2. Baixe o instalador para seu sistema operacional
3. Execute e siga as instruções
4. Verifique: `conda --version`

---

## Parte 2: Criar Ambiente Conda

### 2.1 Criar ambiente com Python 3.10

```bash
# Criar ambiente conda chamado "dataops" com Python 3.10
conda create -n dataops python=3.10 -y

# Aguarde o download e instalação (pode demorar 2-5 minutos)
```

### 2.2 Ativar o ambiente

```bash
# Windows (CMD ou PowerShell)
conda activate dataops

# Linux/Mac
conda activate dataops
```

**Você saberá que funcionou quando ver**:
```
(dataops) C:\Users\seu_usuario>
          ↑
    Ambiente ativado!
```

### 2.3 Verificar Python instalado

```bash
python --version
# Esperado: Python 3.10.x
```

---

## Parte 3: Instalar UV (Gerenciador de Dependências)

UV é um gerenciador de pacotes Python extremamente rápido, escrito em Rust.

### 3.1 Instalar UV

#### Windows (PowerShell):
```bash
# Método 1: Via pip
pip install uv

# OU Método 2: Via instalador oficial
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Linux/Mac:
```bash
# Método 1: Via pip
pip install uv

# OU Método 2: Via curl
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3.2 Verificar instalação

```bash
uv --version
# Esperado: uv 0.x.x ou superior
```

---

## Parte 4: Instalar Dependências do Projeto

### 4.1 Navegar até o diretório do projeto

```bash
cd d:\Projetos\Dataops
```

### 4.2 Instalar dependências com UV

```bash
# Sincronizar ambiente com as dependências do pyproject.toml
uv sync --directory enviroments

# OU se preferir usar pip tradicional (mais lento)
cd enviroments
pip install -e .
cd ..
```

**O que acontece**:
- UV lê `enviroments/pyproject.toml`
- Baixa e instala todas as dependências listadas:
  - pandas, numpy, sqlalchemy
  - Apache Airflow + providers
  - MinIO, boto3
  - Streamlit, Plotly
  - Label Studio SDK
  - E muitas outras...

**Tempo estimado**: 3-10 minutos (dependendo da conexão)

### 4.3 Verificar instalação das dependências principais

```bash
# Verificar Airflow
python -c "import airflow; print(f'Airflow {airflow.__version__}')"

# Verificar Pandas
python -c "import pandas; print(f'Pandas {pandas.__version__}')"

# Verificar MinIO
python -c "import minio; print('MinIO SDK instalado!')"

# Verificar Streamlit
streamlit --version
```

---

## Parte 5: Instalar Docker e Docker Compose

### 5.1 Instalar Docker Desktop

#### Windows/Mac:
1. **Baixe Docker Desktop**:
   - Windows: https://www.docker.com/products/docker-desktop
   - Mac: https://www.docker.com/products/docker-desktop

2. **Execute o instalador**:
   - Duplo clique no arquivo baixado
   - Siga as instruções padrão
   - **Windows**: Certifique-se de habilitar WSL 2 se solicitado

3. **Inicie o Docker Desktop**:
   - Abra o aplicativo Docker Desktop
   - Aguarde aparecer "Docker is running"

#### Linux:
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adicionar seu usuário ao grupo docker
sudo usermod -aG docker $USER

# Reiniciar sessão ou executar
newgrp docker

# Instalar Docker Compose
sudo apt-get install docker-compose-plugin
```

### 5.2 Verificar instalação

```bash
# Verificar Docker
docker --version
# Esperado: Docker version 20.10.x ou superior

# Verificar Docker Compose
docker-compose --version
# Esperado: Docker Compose version v2.x.x ou superior

# Teste básico
docker run hello-world
# Esperado: mensagem "Hello from Docker!"
```

---

## Parte 6: Configurar Variáveis de Ambiente

### 6.1 Criar arquivo .env

```bash
# Copiar template
cp .env.example .env
```

### 6.2 Editar .env

Abra o arquivo `.env` e preencha com suas credenciais:

```bash
# Windows
notepad .env

# Linux/Mac
nano .env
```

**Conteúdo mínimo do .env**:
```env
# ========================================
# MinIO Configuration
# ========================================
MINIO_ACCESS_KEY=admin_dataops
MINIO_SECRET_KEY=SenhaSegura123!MinIO

# ========================================
# Label Studio Configuration
# ========================================
LABELSTUDIO_TOKEN=  # Você vai preencher isso no Passo 8
LABELSTUDIO_PROJECT=4

# ========================================
# Airflow Configuration
# ========================================
AIRFLOW_UID=50000
```

**Salve o arquivo** (Ctrl+S no Notepad, Ctrl+X no nano)

---

## Parte 7: Iniciar Containers Docker

### 7.1 Build das imagens

```bash
# Certifique-se de estar no diretório do projeto
cd d:\Projetos\Dataops

# Build de todas as imagens
docker-compose build

# Tempo estimado: 5-15 minutos na primeira vez
```

### 7.2 Iniciar todos os serviços

```bash
# Iniciar em background
docker-compose up -d

# Acompanhar logs (opcional)
docker-compose logs -f
```

### 7.3 Verificar status

```bash
# Verificar containers
docker-compose ps
```

**Esperado**:
```
NAME                    STATUS
airflow-webserver       Up (healthy)
airflow-scheduler       Up (healthy)
airflow-triggerer       Up (healthy)
minio                   Up (healthy)
label-studio            Up (healthy)
streamlit-dashboard     Up (healthy)
```

> **Aguarde**: Pode demorar 2-3 minutos até todos ficarem "healthy"

---

## Parte 8: Configurar Label Studio e Obter Token

### 8.1 Acessar Label Studio

```
http://localhost:8001
```

### 8.2 Criar conta (primeiro acesso)

1. **Clique em "Sign Up"**
2. **Preencha**:
   - Email: `label_ops@gmail.com`
   - Password: `dataops@123`
   - Confirm Password: `dataops@123`
3. **Clique em "Create Account"**

### 8.3 Configurar e Obter Legacy Token

**Passo A: Habilitar Legacy Tokens (evitar expiração)**

1. **No Label Studio, clique em "Organization"** (menu lateral esquerdo)
2. **Clique em "API Tokens Settings"**
3. **Desmarque todas as flags EXCETO "Legacy tokens"**
   - Deixe APENAS "Legacy tokens" marcado
   - Desmarque as outras opções (isso evita que o token expire)
4. **Clique em "Save"**

**Passo B: Copiar o Legacy Token**

1. **Clique no ícone do usuário** (canto superior direito)
2. **Clique em "Account & Settings"**
3. **Procure "Legacy API Token"**
4. **Copie o token** (40 caracteres hexadecimais)

> ** IMPORTANTE**: A configuração em "Organization > API Tokens Settings" garante que o token não expire automaticamente.

### 8.4 Atualizar .env com token

```bash
# Editar .env novamente
notepad .env  # Windows
nano .env     # Linux/Mac
```

Cole o token:
```env
LABELSTUDIO_TOKEN=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
```

### 8.5 Reiniciar containers

```bash
docker-compose restart airflow-scheduler
docker-compose restart airflow-webserver
docker-compose restart streamlit
```

### 8.6 Importar Dataset do Projeto

O projeto utiliza um dataset de transações comerciais já anotado com entidades NER.

**Dataset disponível em**:
```
https://drive.google.com/drive/folders/1WFkw54HojR1y_Io26_cNV5ni3888I2FZ?usp=sharing
```

**Como importar**:

1. **Baixe o dataset** do Google Drive
2. **Acesse Label Studio**: http://localhost:8001
3. **Abra o projeto** (ID 4)
4. **Clique em "Import"**
5. **Selecione os arquivos JSON** baixados
6. **Clique em "Import"**

**O que contém o dataset**:
- Transações comerciais com dados de clientes, produtos e valores
- Anotações NER já realizadas (cliente, produto, valor, etc.)
- Dados prontos para processamento pelo pipeline

> **IMPORTANTE**: Após importar o dataset, você pode executar o pipeline para processar esses dados através das camadas Bronze → Silver → Gold.

---

## Parte 9: Verificar Instalação Completa

### 9.1 Verificar ambiente Python

```bash
# Ambiente ativado?
conda env list
# Deve mostrar * ao lado de "dataops"

# Pacotes instalados?
conda list | grep airflow
conda list | grep pandas
```

### 9.2 Verificar Docker

```bash
# Todos os containers rodando?
docker-compose ps

# Ver logs se algum estiver com problema
docker-compose logs <nome_do_container>
```

### 9.3 Acessar cada serviço

<<<<<<< HEAD
- **Airflow**: http://localhost:8080 (airflow/airflow)
- **Label Studio**: http://localhost:8001 (label_ops@gmail.com/dataops@123)
- **MinIO**: http://localhost:9001 (seu MINIO_ACCESS_KEY / MINIO_SECRET_KEY)
- **Streamlit**: http://localhost:8501
=======
**Airflow**: http://localhost:8080 (airflow/airflow)
**Label Studio**: http://localhost:8001 (label_ops@gmail.com/dataops@123)
**MinIO**: http://localhost:9001 (seu MINIO_ACCESS_KEY / MINIO_SECRET_KEY)
**Streamlit**: http://localhost:8501
>>>>>>> 56eb96e4472ccab668005a192013d8ec6fe394e8

---

## Parte 10: Executar Pipeline Pela Primeira Vez

### Opção A: Via Airflow (Recomendado)

1. **Acesse Airflow**: http://localhost:8080
2. **Login**: airflow / airflow
3. **Ative a DAG**: `00_event_driven_ingestion`
4. **Trigger manualmente**: Clique no ▶️
5. **Acompanhe execução**: Veja tasks sendo executadas

### Opção B: Executar Scripts Localmente

```bash
# Certifique-se de que o ambiente conda está ativado
conda activate dataops

# Executar pipeline completo
python -m scripts_pipeline.clean_buckets
python -m scripts_pipeline.insert_bronze
python -m scripts_pipeline.transform_silver
python -m scripts_pipeline.aggregate_gold

# Verificar diagnóstico
python diagnose_data_flow.py

# Executar dashboard para visualizar os dados
streamlit run streamlit\dashboard.py
```

**Saída esperada do pipeline**:
```
  Detectado execução local. Usando endpoint: localhost:9000

  Extraindo labels NER...

   [EXTRAÍDO] cliente: 'joão silva'
   [EXTRAÍDO] valor: '150.50'

Pipeline executado com sucesso!


**Saída esperada do Streamlit**:
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
```

> **IMPORTANTE**: O comando `streamlit run` deve ser executado APÓS os dados subirem para a camada Gold. O dashboard ficará rodando continuamente - pressione Ctrl+C para parar.

---

## Parte 11: Visualizar no Dashboard

### Opção A: Dashboard no Docker (Automático)

Se você está usando Docker, o dashboard já está rodando automaticamente:
```
http://localhost:8501
```

### Opção B: Dashboard Local (Execução Manual)

Se você executou o pipeline localmente (fora do Docker), após os dados subirem para a camada Gold, execute:

```bash
# Certifique-se de que o ambiente conda está ativado
conda activate dataops

# Execute o dashboard Streamlit
streamlit run streamlit\dashboard.py
```

**Saída esperada**:
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

**Acesse**: http://localhost:8501

**Você deve ver**:
- KPIs agregados
- Tabelas com dados
- Gráficos Plotly
- Dados em tempo real

> **IMPORTANTE**: O dashboard se conecta ao MinIO para ler os dados da camada Gold. Certifique-se de que o MinIO está rodando (via Docker ou localmente).

---

## Troubleshooting

### Problema 1: Conda não reconhecido

**Sintoma**: `conda: command not found`

**Solução**:
```bash
# Windows: Adicionar ao PATH manualmente
# Painel de Controle > Sistema > Variáveis de Ambiente
# Adicionar: C:\Users\<usuario>\miniconda3\Scripts

# Ou reabrir terminal após instalação
```

### Problema 2: UV não instala dependências

**Sintoma**: Erro ao executar `uv sync`

**Solução**:
```bash
# Usar pip tradicional
cd enviroments
pip install -e .
```

### Problema 3: Docker não inicia

**Sintoma**: Containers ficam em "Exited"

**Solução**:
```bash
# Ver logs
docker-compose logs <container_name>

# Reiniciar Docker Desktop
# Reexecutar
docker-compose down
docker-compose up -d
```

### Problema 4: Python 3.10 não disponível

**Sintoma**: `PackageNotFoundError: python=3.10`

**Solução**:
```bash
# Atualizar conda
conda update conda

# Ou usar Python 3.11 (também funciona)
conda create -n dataops python=3.11 -y
```

---

## Comandos Úteis

### Gerenciar Ambiente Conda

```bash
# Ativar ambiente
conda activate dataops

# Desativar ambiente
conda deactivate

# Listar ambientes
conda env list

# Remover ambiente
conda env remove -n dataops

# Exportar ambiente
conda env export > environment.yml

# Criar ambiente de um arquivo
conda env create -f environment.yml
```

### Gerenciar Dependências com UV

```bash
# Adicionar nova dependência
cd enviroments
uv add nome_do_pacote

# Remover dependência
uv remove nome_do_pacote

# Atualizar todas as dependências
uv sync --upgrade

# Ver dependências instaladas
uv pip list
```

### Gerenciar Docker

```bash
# Parar containers
docker-compose stop

# Parar e remover containers
docker-compose down

# Ver logs
docker-compose logs -f

# Reiniciar um serviço
docker-compose restart <service_name>

# Rebuild completo
docker-compose build --no-cache
docker-compose up -d
```

---

## Checklist Final

**Instalação Base**:
- Conda instalado e funcionando
- Ambiente `dataops` criado com Python 3.10
- UV instalado e funcionando
- Docker + Docker Compose instalados

**Dependências**:
- Dependências do Python instaladas (via uv sync)
- Airflow, Pandas, MinIO SDK verificados
- Streamlit funcionando

**Configuração**:
- .env criado e preenchido
- Legacy Token do Label Studio obtido
- Containers Docker todos "healthy"

**Funcionalidade**:
- Todos os serviços acessíveis
- Pipeline executa sem erros
- Dashboard mostra dados

---

## Próximos Passos

Agora que seu ambiente está completo:

1. **Leia a documentação completa**: [SETUP_COMPLETO.md](SETUP_COMPLETO.md)
2. **Execute o pipeline via Airflow** ou scripts locais
3. **Importe o dataset** no Label Studio

---

## Referências

- **Conda**: https://docs.conda.io/
- **UV**: https://github.com/astral-sh/uv
- **Docker**: https://docs.docker.com/
- **Airflow**: https://airflow.apache.org/docs/
- **Label Studio**: https://labelstud.io/guide/

---

**Pronto!** Seu ambiente está 100% configurado e pronto para uso!
