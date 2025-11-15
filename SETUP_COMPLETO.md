# 🚀 Setup Completo - Guia Passo a Passo

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- ✅ **Docker** (versão 20.10 ou superior)
- ✅ **Docker Compose** (versão 1.29 ou superior)
- ✅ **Git** (para clonar o repositório)
- ✅ **Python 3.9+** (apenas se for executar scripts localmente)

### Verificar Instalação

```bash
# Verificar Docker
docker --version
# Esperado: Docker version 20.10.x ou superior

# Verificar Docker Compose
docker-compose --version
# Esperado: docker-compose version 1.29.x ou superior

# Verificar Python (opcional)
python --version
# Esperado: Python 3.9.x ou superior
```

---

## 📥 Passo 1: Clonar o Repositório

```bash
# Clone o projeto
git clone <URL_DO_REPOSITORIO>

# Entre no diretório
cd Dataops
```

---

## 🔐 Passo 2: Configurar Variáveis de Ambiente

### 2.1 Criar arquivo .env

```bash
# Copiar o template
cp .env.example .env
```

### 2.2 Editar o arquivo .env

Abra o arquivo `.env` com seu editor favorito:

```bash
# Windows
notepad .env

# Linux/Mac
nano .env
# ou
vim .env
```

### 2.3 Preencher as credenciais

**IMPORTANTE**: Preencha com valores SEGUROS, não use os exemplos abaixo em produção!

```env
# ========================================
# MinIO Configuration
# ========================================
MINIO_ACCESS_KEY=admin_dataops
MINIO_SECRET_KEY=SenhaSegura123!MinIO

# ========================================
# Label Studio Configuration
# ========================================
LABELSTUDIO_TOKEN=seu_token_aqui  # ⬅️ Você vai obter isso no Passo 4
LABELSTUDIO_PROJECT=4

# ========================================
# Airflow Configuration
# ========================================
AIRFLOW_UID=50000
```

> **💡 IMPORTANTE**: Deixe `LABELSTUDIO_TOKEN` vazio por enquanto. Você vai preencher no Passo 4.

---

## 🐳 Passo 3: Iniciar os Containers Docker

### 3.1 Build das imagens

```bash
# Build de todas as imagens
docker-compose build

# Isso pode demorar 5-10 minutos na primeira vez
```

### 3.2 Iniciar os serviços

```bash
# Iniciar todos os containers em background
docker-compose up -d

# Acompanhar logs (opcional)
docker-compose logs -f
```

### 3.3 Verificar status dos containers

```bash
# Verificar se todos estão rodando
docker-compose ps
```

**Esperado**:
```
NAME                    STATUS              PORTS
airflow-webserver       Up (healthy)        0.0.0.0:8080->8080/tcp
airflow-scheduler       Up (healthy)
airflow-triggerer       Up (healthy)
minio                   Up (healthy)        0.0.0.0:9000->9000/tcp, 0.0.0.0:9001->9001/tcp
label-studio            Up (healthy)        0.0.0.0:8001->8080/tcp
streamlit-dashboard     Up (healthy)        0.0.0.0:8501->8501/tcp
```

> **⏱️ Aguarde**: Pode demorar 2-3 minutos até todos os containers ficarem "healthy"

---

## 🏷️ Passo 4: Configurar Label Studio e Obter Token LEGACY

### 4.1 Acessar Label Studio

Abra seu navegador e acesse:
```
http://localhost:8001
```

### 4.2 Criar Conta no Primeiro Acesso

**⚠️ IMPORTANTE**: No primeiro acesso, você precisa criar uma conta.

#### Passo a passo:

1. **Acesse**: http://localhost:8001
2. **Clique em "Sign Up"** (se aparecer tela de login)
3. **Preencha o formulário de cadastro**:
   - **Email**: `label_ops@gmail.com`
   - **Password**: `dataops@123`
   - **Confirm Password**: `dataops@123`
4. **Clique em "Create Account"**

> **💡 NOTA**: Se o Label Studio já tiver sido inicializado anteriormente e você vir uma tela de login, use as credenciais padrão:
> - **Email**: `admin@localhost.com`
> - **Senha**: `123456`
>
> Ou use as credenciais que você criou: `label_ops@gmail.com` / `dataops@123`

### 4.3 Configurar Legacy Token (IMPORTANTE!)

**⚠️ ATENÇÃO**: O pipeline precisa do **LEGACY TOKEN**, não do Access Token normal!

#### Passo a passo para configurar e obter o Legacy Token:

**Parte A: Habilitar Legacy Tokens (evitar expiração)**

1. **No Label Studio, clique em "Organization"** (menu lateral esquerdo)
2. **Clique em "API Tokens Settings"**
3. **Desmarque todas as flags EXCETO "Legacy tokens"**
   - ✅ Deixe APENAS "Legacy tokens" marcado
   - ❌ Desmarque as outras opções (isso evita que o token expire)
4. **Clique em "Save"**

**Parte B: Gerar/Copiar o Legacy Token**

1. **Clique no ícone do usuário** (canto superior direito)
2. **Clique em "Account & Settings"**
3. **Role até a seção "Access Token"**
4. **Procure por "Legacy API Token"** ou **"API Token (Legacy)"**
5. **Copie o token** (algo como: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0`)

> **💡 IMPORTANTE**:
> - A configuração em "Organization > API Tokens Settings" garante que o token não expire
> - Deixar SOMENTE a flag "Legacy tokens" ativa é FUNDAMENTAL
> - Não use o "Access Token" (JWT) - ele não funciona com este pipeline
> - O Legacy Token tem formato: 40 caracteres hexadecimais

#### Imagem de referência:
```
┌────────────────────────────────────────┐
│ Account & Settings                     │
├────────────────────────────────────────┤
│ ...                                    │
│                                        │
│ 🔑 Access Token                        │
│ ┌────────────────────────────────────┐ │
│ │ Legacy API Token (deprecated)      │ │
│ │ a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6... │ │ ⬅️ COPIE ESTE!
│ │ [Copy]                             │ │
│ └────────────────────────────────────┘ │
│                                        │
└────────────────────────────────────────┘
```

### 4.4 Atualizar .env com o Token

Edite o arquivo `.env` e cole o token:

```bash
# Editar .env
notepad .env  # Windows
nano .env     # Linux/Mac
```

Atualize a linha:
```env
LABELSTUDIO_TOKEN=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0  # ⬅️ Cole seu token aqui
```

Salve o arquivo.

### 4.5 Reiniciar containers para aplicar o token

```bash
# Reiniciar para ler novo .env
docker-compose restart airflow-scheduler
docker-compose restart airflow-webserver
docker-compose restart streamlit
```

---

## 📊 Passo 5: Criar Projeto no Label Studio (se necessário)

Se você não tiver o projeto ID 4, crie um novo:

### 5.1 Criar novo projeto

1. No Label Studio, clique em **"Create Project"**
2. Nome: `DataOps NER Pipeline`
3. Em **"Labeling Setup"**, escolha **"Named Entity Recognition"**
4. Configure os labels:
   - `cliente`
   - `produto`
   - `quantidade`
   - `valor`
   - `canal`
   - `forma_pagamento`
   - `status`
   - `cidade`
   - `avaliacao`
   - `data`
   - `sentimento`

5. Clique em **"Save"**

### 5.2 Obter ID do projeto

1. Acesse o projeto criado
2. Veja a URL no navegador:
   ```
   http://localhost:8001/projects/4/data
                                    ↑
                              Este é o ID
   ```
3. Atualize o `.env`:
   ```env
   LABELSTUDIO_PROJECT=4  # ⬅️ Coloque o ID correto
   ```

### 5.3 Importar Dataset do Projeto

**📊 Dataset disponível em**:
```
https://drive.google.com/drive/folders/1WFkw54HojR1y_Io26_cNV5ni3888I2FZ?usp=sharing
```

**Como importar**:

1. **Baixe o dataset** do Google Drive
2. **No Label Studio**, abra o projeto (ID 4)
3. **Clique em "Import"**
4. **Selecione os arquivos JSON** baixados
5. **Clique em "Import"**

**Conteúdo do dataset**:
- Transações comerciais com dados estruturados
- Anotações NER já realizadas (cliente, produto, valor, quantidade, etc.)
- 950+ registros prontos para processamento

> **💡 NOTA**: Após importar, o dataset estará pronto para ser processado pelo pipeline Airflow.

---

## ✅ Passo 6: Verificar Serviços

Acesse cada serviço para verificar se está funcionando:

### 6.1 Airflow
```
URL: http://localhost:8080
Login: airflow
Senha: airflow
```

**O que verificar**:
- [ ] Interface do Airflow carrega
- [ ] DAGs aparecem na lista
- [ ] Nenhum erro nos logs

### 6.2 MinIO Console
```
URL: http://localhost:9001
Login: <seu MINIO_ACCESS_KEY do .env>
Senha: <seu MINIO_SECRET_KEY do .env>
```

**O que verificar**:
- [ ] Interface do MinIO carrega
- [ ] Buckets `bronze`, `silver`, `gold` e `inbox` existem

### 6.3 Label Studio
```
URL: http://localhost:8001
Login: label_ops@gmail.com
Senha: dataops@123
```

> **Ou se usou as credenciais padrão**: admin@localhost.com / 123456

**O que verificar**:
- [ ] Interface carrega
- [ ] Projeto aparece
- [ ] Token foi copiado corretamente

### 6.4 Streamlit Dashboard
```
URL: http://localhost:8501
(sem autenticação)
```

**O que verificar**:
- [ ] Dashboard carrega
- [ ] Pode estar vazio se ainda não houver dados (normal!)

---

## 🎯 Passo 7: Executar Pipeline pela Primeira Vez

### Opção A: Executar via Airflow (Recomendado)

1. **Acesse Airflow**: http://localhost:8080

2. **Ative as DAGs**:
   - Localize `00_event_driven_ingestion`
   - Clique no toggle para ativar (fica azul)

3. **Trigger manual**:
   - Clique no ícone de "play" ▶️ na DAG
   - Clique em "Trigger DAG"

4. **Acompanhe execução**:
   - Clique na DAG para ver detalhes
   - Veja as tasks sendo executadas em tempo real

### Opção B: Executar Scripts Manualmente (para teste)

Se quiser testar localmente (fora do Docker):

```bash
# Instalar dependências Python localmente
pip install -r requirements.txt

# Executar pipeline passo a passo
python -m scripts_pipeline.clean_buckets       # Limpar buckets
python -m scripts_pipeline.insert_bronze       # Inserir dados
python -m scripts_pipeline.transform_silver    # Transformar
python -m scripts_pipeline.aggregate_gold      # Agregar

# Ver diagnóstico
python diagnose_data_flow.py
```

**Saída esperada no transform_silver.py**:
```
ℹ️  Detectado execução local. Usando endpoint: localhost:9000

🏷️  Extraindo labels NER e padronizando...

REGISTRO 0:
   [DEBUG] Processando 1 anotação(ões)
   [DEBUG] Anotação 0 tem 5 resultado(s)
      [EXTRAÍDO] cliente: 'joão silva'
      [EXTRAÍDO] valor: '150.50'

📊 Resumo de dados extraídos da API do Label Studio:

   🏷️  Estatísticas de Extração NER:
      • Registros com algum NER: 950
      • Registros com 'cliente': 950
      • Registros com 'produto': 950
```

---

## 📊 Passo 8: Visualizar Dados no Dashboard

### Opção A: Via Docker (Automático)

Se estiver usando Docker, o dashboard já está rodando. Acesse:
```
http://localhost:8501
```

### Opção B: Execução Local (Manual)

Se executou o pipeline localmente, após os dados subirem para a camada Gold, execute:

```bash
# Ativar ambiente (se necessário)
conda activate dataops

# Executar dashboard
streamlit run streamlit\dashboard.py
```

**Acesse**: http://localhost:8501

**Você deve ver**:
- ✅ KPIs agregados (se houver dados)
- ✅ Tabelas com registros
- ✅ Gráficos Plotly
- ✅ Dados em tempo real

> **💡 Se o dashboard estiver vazio**: Execute o pipeline primeiro (Passo 7)
>
> **⚠️ IMPORTANTE**: O dashboard requer que o MinIO esteja rodando para acessar os dados da camada Gold

---

## 🐛 Troubleshooting - Problemas Comuns

### Problema 1: Container não inicia

**Sintoma**: `docker-compose ps` mostra container com status "Exited"

**Solução**:
```bash
# Ver logs do container com problema
docker-compose logs <nome_do_container>

# Exemplo:
docker-compose logs label-studio
docker-compose logs minio
```

### Problema 2: "Failed to resolve 'minio'"

**Sintoma**: Erro ao executar scripts localmente

**Solução**:
- ✅ Já está corrigido! O sistema detecta automaticamente se está rodando local ou Docker
- Se ainda ocorrer, certifique que Docker está rodando: `docker ps`

### Problema 3: Label Studio não aceita token

**Sintoma**: Erro 401 Unauthorized

**Solução**:
1. Certifique que está usando **Legacy Token**, não Access Token
2. Verifique se copiou o token completo (40 caracteres)
3. Não deixe espaços antes/depois do token no `.env`
4. Reinicie os containers: `docker-compose restart`

### Problema 4: Buckets MinIO não existem

**Sintoma**: Erro "Bucket 'bronze' does not exist"

**Solução**:
```bash
# Reexecutar inicialização do MinIO
docker-compose restart minio-init

# Ver logs da inicialização
docker-compose logs minio-init
```

### Problema 5: Port já em uso

**Sintoma**: "Port 8080 is already allocated"

**Solução**:
```bash
# Parar processo que está usando a porta
# Windows:
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :8080
kill -9 <PID>

# Ou mudar porta no docker-compose.yml
```

### Problema 6: Credenciais incorretas

**Sintoma**: "Authentication failed"

**Solução**:
```bash
# Verificar se .env foi lido corretamente
docker-compose config | grep MINIO_ACCESS_KEY

# Se vazio, o .env não foi lido
# Certifique que:
# 1. .env está na raiz do projeto
# 2. Não tem espaços antes/depois do =
# 3. Reiniciou os containers
```

---

## 📚 Comandos Úteis

### Gerenciamento de Containers

```bash
# Ver logs em tempo real
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f streamlit

# Parar todos os containers
docker-compose stop

# Parar e remover containers
docker-compose down

# Reiniciar um serviço
docker-compose restart airflow-scheduler

# Executar comando dentro de um container
docker-compose exec streamlit bash
```

### Limpeza e Reset

```bash
# Parar e remover tudo (CUIDADO: deleta dados!)
docker-compose down -v

# Rebuild completo
docker-compose build --no-cache
docker-compose up -d
```

### Monitoramento

```bash
# Ver uso de recursos
docker stats

# Ver status de saúde
docker-compose ps

# Ver networks
docker network ls
docker network inspect dataops_dataops-network
```

---

## ✅ Checklist Final

Antes de considerar o setup completo, verifique:

**Containers**:
- [ ] Todos containers estão "Up (healthy)"
- [ ] Nenhum container em status "Exited"

**Configuração**:
- [ ] .env criado com credenciais preenchidas
- [ ] LABELSTUDIO_TOKEN é o Legacy Token (40 caracteres)
- [ ] LABELSTUDIO_PROJECT corresponde ao ID correto

**Acesso aos Serviços**:
- [ ] Airflow acessível em http://localhost:8080
- [ ] MinIO acessível em http://localhost:9001
- [ ] Label Studio acessível em http://localhost:8001
- [ ] Streamlit acessível em http://localhost:8501

**Funcionalidade**:
- [ ] DAG aparece no Airflow
- [ ] Buckets existem no MinIO (bronze, silver, gold, inbox)
- [ ] Projeto existe no Label Studio
- [ ] Pipeline executa sem erros

**Testes**:
- [ ] Executou pipeline manualmente (Passo 7)
- [ ] Dados aparecem no dashboard
- [ ] Logs não mostram erros críticos

---

## 🎓 Próximos Passos

Agora que o setup está completo:

1. **Adicione dados** ao Label Studio (projeto 4)
2. **Anote os dados** com as labels NER
3. **Execute o pipeline** via Airflow
4. **Visualize resultados** no dashboard

Para mais informações:
- **[COMECE_AQUI.md](COMECE_AQUI.md)** - Quick start
- **[DOCKER_COMPOSE_SETUP.md](DOCKER_COMPOSE_SETUP.md)** - Docker detalhado
- **[PROXIMO_TESTE.md](PROXIMO_TESTE.md)** - Testes completos

---

## 📞 Suporte

Se encontrar problemas:

1. Consulte a seção **Troubleshooting** acima
2. Verifique os logs: `docker-compose logs -f`
3. Veja documentação específica em `docs/`

---

**Pronto!** 🎉 Seu ambiente DataOps está configurado e funcionando!
