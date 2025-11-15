# DataOps Pipeline - Bronze, Silver, Gold

Pipeline completo de dados com arquitetura em camadas, orquestração Airflow e dashboard em tempo real.

## Arquitetura

```
Label Studio (NER Annotations)
         ↓
    Bronze Layer (Raw JSON)
         ↓
    Silver Layer (Clean + NER Extraction)
         ↓
    Gold Layer (Aggregations + KPIs)
         ↓
    Streamlit Dashboard
```

## Stack Tecnológica

- **Orquestração**: Apache Airflow (event-driven com sensores deferráveis)
- **Storage**: MinIO (S3-compatible, 3 camadas)
- **Transformação**: Python + Pandas
- **Anotação**: Label Studio (NER)
- **Visualização**: Streamlit
- **Infraestrutura**: Docker + Docker Compose
- **Banco de Dados**: PostgreSQL

## Quick Start

> **Primeira vez usando?** Veja [INSTALACAO_AMBIENTE.md](INSTALACAO_AMBIENTE.md) para instalação completa do zero (Conda + UV + Docker)

### 1. Clone o repositório
```bash
git clone <URL>
cd Dataops
```

### 2. Configure o ambiente Python (opcional - local)
```bash
# Criar ambiente conda
conda create -n dataops python=3.10 -y
conda activate dataops

# Instalar dependências com UV
uv sync --directory enviroments
```

### 3. Configure as credenciais
```bash
cp .env.example .env
# Edite .env com suas credenciais
```

### 4. Inicie o ambiente Docker
```bash
docker-compose up -d
```

### 5. Acesse os serviços
- **Airflow**: http://localhost:8080 (airflow/airflow)
- **Label Studio**: http://localhost:8001 (label_ops@gmail.com/dataops@123)
- **MinIO**: http://localhost:9001 (veja .env)
- **Dashboard**: http://localhost:8501

## Documentação Completa

### Para Começar
- **[INSTALACAO_AMBIENTE.md](INSTALACAO_AMBIENTE.md)** - Instalação completa do ambiente do zero
  - Instalar Conda/Miniconda
  - Criar ambiente Python 3.10
  - Instalar UV (gerenciador de dependências)
  - Instalar Docker + Docker Compose
  - Configurar e executar todo o pipeline

- **[SETUP_COMPLETO.md](SETUP_COMPLETO.md)** - Guia rápido (se já tem ambiente)
  - Pré-requisitos
  - Instalação
  - Configuração do Legacy Token do Label Studio
  - Execução do pipeline
  - Troubleshooting

## IMPORTANTE: Label Studio Legacy Token e Project ID

Este pipeline requer o **Legacy Token** do Label Studio, não o Access Token (JWT).

**Tutorial em vídeo**:
- Como criar o Legacy Token: https://drive.google.com/file/d/11teN7OjPgbhWD17H0z4XPJ5pYhE3D4_j/view?usp=sharing
- Como criar o projeto: https://drive.google.com/file/d/1sC-S7fQ0PFElqM8oX01OP-f2IsGlSrx_/view?usp=sharing

**Como configurar e obter**:

1. **Acesse Label Studio**: http://localhost:8001
2. **Primeiro acesso**: Crie conta com `label_ops@gmail.com` / `dataops@123`
   - Ou use credenciais padrão: `admin@localhost.com` / `123456`

3. **Habilitar Legacy Tokens (evitar expiração)**:
   - Clique em **"Organization"** (menu lateral)
   - Clique em **"API Tokens Settings"**
   - Deixe APENAS a flag **"Legacy tokens"** marcada
   - Desmarque as outras opções
   - Clique em **"Save"**

4. **Copiar o token**:
   - Clique no ícone do usuário (canto superior direito)
   - **Account & Settings**
   - Procure por **"Legacy API Token"**
   - Copie o token (40 caracteres hexadecimais)

5. **Obter ID do Projeto**:
   - Acesse o projeto no Label Studio
   - Veja a URL do navegador: `http://localhost:8001/projects/3/data?tab=3`
   - O número após `/projects/` é o ID do projeto (neste exemplo: `3`)

6. **Inserir no arquivo .env**:
   ```env
   LABELSTUDIO_TOKEN=seu_token_aqui_40_caracteres
   LABELSTUDIO_PROJECT=3  # ID do seu projeto
   ```

Ver detalhes completos em **[SETUP_COMPLETO.md](SETUP_COMPLETO.md) - Passo 4.3**

## Dataset do Projeto

O projeto utiliza um dataset de transações comerciais com anotações NER.

**Baixar dataset**:
```
https://drive.google.com/drive/folders/1WFkw54HojR1y_Io26_cNV5ni3888I2FZ?usp=sharing
```

**Conteúdo**:
- 500 registros de transações comerciais (cliente, produto, valor, etc.)
- Anotações NER já realizadas
- Pronto para importação no Label Studio

**Como usar**:
1. Baixe o dataset do Google Drive
2. Importe no Label Studio (Project ID 4)
3. Execute o pipeline via Airflow
4. Visualize resultados no Dashboard

Ver instruções completas em **[INSTALACAO_AMBIENTE.md](INSTALACAO_AMBIENTE.md) - Parte 8.6**

## Principais Features

- **Event-Driven Architecture** - Airflow detecta novos arquivos automaticamente
- **3 Camadas (Bronze/Silver/Gold)** - Arquitetura Medallion
- **NER Extraction** - Named Entity Recognition via Label Studio
- **Debug Automático** - Logs detalhados de extração
- **Segurança** - Credenciais em variáveis de ambiente
- **Auto-detecção de Ambiente** - Funciona local e Docker
- **Dashboard Real-time** - Streamlit com atualização automática

## Métricas

- **500 registros** no dataset
- **8 KPIs** pré-calculados
- **3 camadas** de storage
- **0 credenciais** hardcoded
- **100% containerizado**

## Desenvolvimento

### Executar localmente (fora do Docker)

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar pipeline
python -m scripts_pipeline.clean_buckets
python -m scripts_pipeline.insert_bronze
python -m scripts_pipeline.transform_silver
python -m scripts_pipeline.aggregate_gold

# Ver diagnóstico
python diagnose_data_flow.py

# Visualizar dashboard (após dados subirem para camada Gold)
streamlit run streamlit\dashboard.py
```

> **NOTA**: Se estiver usando Docker, o dashboard já está rodando automaticamente em http://localhost:8501

### Estrutura de Diretórios

```
Dataops/
├── dags/                    # Airflow DAGs
│   ├── sensors/            # Sensores customizados
│   └── env_config.py       # Configuração segura
├── scripts_pipeline/        # Scripts de transformação
│   ├── insert_bronze.py    # Ingestão
│   ├── transform_silver.py # Limpeza + NER
│   └── aggregate_gold.py   # Agregações
├── streamlit/              # Dashboard
│   └── dashboard.py
├── docker-compose.yml      # Orquestração
├── .env.example           # Template de configuração
└── docs/                   # Documentação completa
```

## Troubleshooting

### Container não inicia
```bash
docker-compose logs <container_name>
```

### Erro "Failed to resolve 'minio'"
Já corrigido! O sistema detecta automaticamente o ambiente.

### Label Studio - 401 Unauthorized
Certifique que está usando **Legacy Token**, não Access Token.

Ver mais em **[SETUP_COMPLETO.md](SETUP_COMPLETO.md) - Troubleshooting**

## Fluxo de Dados

1. **Ingestão**: Label Studio API → JSON estruturado → MinIO Bronze
2. **Transformação**: Bronze → Limpeza + NER extraction → MinIO Silver
3. **Agregação**: Silver → KPIs + Agregações → MinIO Gold
4. **Visualização**: Gold → Streamlit Dashboard

## Conceitos Aplicados

- **DataOps**: Orquestração, monitoramento, versionamento
- **Medallion Architecture**: Bronze (raw) → Silver (clean) → Gold (curated)
- **Event-Driven**: Processamento reativo a eventos
- **NER (Named Entity Recognition)**: Extração de entidades nomeadas
- **Containerização**: Docker, isolamento, portabilidade
- **Security**: Credenciais em variáveis de ambiente

## Licença

Este projeto foi desenvolvido como trabalho de conclusão de disciplina.

## Contribuindo

Contribuições são bem-vindas! Por favor:
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Suporte

- **Documentação**: Ver arquivos `.md` na raiz do projeto
- **Issues**: Abra uma issue no GitHub

---

**Desenvolvido usando Python, Airflow, Docker**
