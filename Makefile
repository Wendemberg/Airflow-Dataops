# Makefile - DataOps Pipeline
# Automação de tarefas comuns do projeto

.PHONY: help setup install docker-up docker-down docker-restart docker-logs clean-buckets pipeline dashboard test lint format

# Variáveis
PYTHON := python
CONDA_ENV := dataops
DOCKER_COMPOSE := docker-compose

# Comando padrão: mostrar ajuda
help:
	@echo "=========================================="
	@echo "  DataOps Pipeline - Comandos Disponíveis"
	@echo "=========================================="
	@echo ""
	@echo "Setup Inicial:"
	@echo "  make setup           - Criar ambiente conda + instalar dependências"
	@echo "  make install         - Instalar dependências (assume conda ativado)"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up       - Subir containers Docker"
	@echo "  make docker-down     - Parar e remover containers"
	@echo "  make docker-restart  - Reiniciar containers"
	@echo "  make docker-logs     - Ver logs de todos os containers"
	@echo "  make docker-status   - Ver status dos containers"
	@echo ""
	@echo "Pipeline:"
	@echo "  make clean-buckets   - Limpar buckets MinIO (Bronze/Silver/Gold)"
	@echo "  make pipeline        - Executar pipeline completo"
	@echo "  make bronze          - Inserir dados na camada Bronze"
	@echo "  make silver          - Processar camada Silver"
	@echo "  make gold            - Processar camada Gold"
	@echo "  make diagnose        - Diagnosticar fluxo de dados"
	@echo ""
	@echo "Dashboard:"
	@echo "  make dashboard       - Rodar dashboard Streamlit localmente"
	@echo ""
	@echo "Desenvolvimento:"
	@echo "  make test            - Rodar testes"
	@echo "  make lint            - Verificar código com ruff"
	@echo "  make format          - Formatar código com black"
	@echo ""
	@echo "Utilitários:"
	@echo "  make check-env       - Verificar variáveis de ambiente"
	@echo "  make first-run       - Setup completo (primeira vez)"
	@echo ""

# ==================== SETUP ====================

# Setup completo: criar ambiente conda + instalar dependências
setup:
	@echo "🔧 Criando ambiente conda '$(CONDA_ENV)' com Python 3.10..."
	conda create -n $(CONDA_ENV) python=3.10 -y
	@echo ""
	@echo "📦 Instalando dependências com UV..."
	conda run -n $(CONDA_ENV) pip install uv
	conda run -n $(CONDA_ENV) uv sync
	@echo ""
	@echo "✅ Ambiente criado com sucesso!"
	@echo ""
	@echo "👉 Próximos passos:"
	@echo "   1. Ative o ambiente: conda activate $(CONDA_ENV)"
	@echo "   2. Configure .env com suas credenciais"
	@echo "   3. Suba os containers: make docker-up"
	@echo ""

# Instalar dependências (assume conda já ativado)
install:
	@echo "📦 Instalando dependências com UV..."
	uv sync
	@echo "✅ Dependências instaladas!"

# ==================== DOCKER ====================

# Subir containers Docker
docker-up:
	@echo "🐳 Subindo containers Docker..."
	$(DOCKER_COMPOSE) up -d
	@echo ""
	@echo "⏳ Aguardando containers ficarem healthy (pode demorar 2-3 min)..."
	@sleep 10
	@$(DOCKER_COMPOSE) ps
	@echo ""
	@echo "✅ Containers iniciados!"
	@echo ""
	@echo "🌐 Serviços disponíveis:"
	@echo "   Airflow:      http://localhost:8080 (airflow/airflow)"
	@echo "   Label Studio: http://localhost:8001"
	@echo "   MinIO:        http://localhost:9001"
	@echo "   Streamlit:    http://localhost:8501"
	@echo ""

# Parar containers
docker-down:
	@echo "🛑 Parando containers Docker..."
	$(DOCKER_COMPOSE) down
	@echo "✅ Containers parados!"

# Reiniciar containers
docker-restart:
	@echo "🔄 Reiniciando containers..."
	$(DOCKER_COMPOSE) restart
	@echo "✅ Containers reiniciados!"

# Ver logs dos containers
docker-logs:
	@echo "📋 Logs dos containers (Ctrl+C para sair):"
	$(DOCKER_COMPOSE) logs -f

# Ver status dos containers
docker-status:
	@echo "📊 Status dos containers:"
	@$(DOCKER_COMPOSE) ps

# ==================== PIPELINE ====================

# Limpar buckets MinIO
clean-buckets:
	@echo "🧹 Limpando buckets MinIO..."
	$(PYTHON) -m scripts_pipeline.clean_buckets
	@echo "✅ Buckets limpos!"

# Executar pipeline completo
pipeline: bronze silver gold diagnose
	@echo ""
	@echo "✅ Pipeline completo executado com sucesso!"
	@echo ""

# Inserir dados em Bronze
bronze:
	@echo "📂 Inserindo dados na camada Bronze..."
	$(PYTHON) -m scripts_pipeline.insert_bronze

# Processar Silver
silver:
	@echo "✅ Processando camada Silver..."
	$(PYTHON) -m scripts_pipeline.transform_silver

# Processar Gold
gold:
	@echo "⭐ Processando camada Gold..."
	$(PYTHON) -m scripts_pipeline.aggregate_gold

# Diagnosticar fluxo de dados
diagnose:
	@echo "🔍 Diagnosticando fluxo de dados..."
	$(PYTHON) diagnose_data_flow.py

# ==================== DASHBOARD ====================

# Rodar dashboard Streamlit
dashboard:
	@echo "🎨 Iniciando dashboard Streamlit..."
	@echo "📊 Acesse: http://localhost:8501"
	@echo ""
	streamlit run streamlit/dashboard.py

# ==================== DESENVOLVIMENTO ====================

# Rodar testes
test:
	@echo "🧪 Rodando testes..."
	pytest tests/ -v

# Verificar código com ruff
lint:
	@echo "🔍 Verificando código com ruff..."
	ruff check .

# Formatar código com black
format:
	@echo "✨ Formatando código com black..."
	black .
	@echo "✅ Código formatado!"

# ==================== UTILITÁRIOS ====================

# Verificar variáveis de ambiente
check-env:
	@echo "🔍 Verificando variáveis de ambiente..."
	@if [ ! -f .env ]; then \
		echo "❌ Arquivo .env não encontrado!"; \
		echo "👉 Copie .env.example para .env e configure as credenciais"; \
		exit 1; \
	else \
		echo "✅ Arquivo .env encontrado"; \
		echo ""; \
		echo "Verificando variáveis obrigatórias..."; \
		grep -q "MINIO_ACCESS_KEY=" .env && echo "  ✅ MINIO_ACCESS_KEY configurada" || echo "  ❌ MINIO_ACCESS_KEY não configurada"; \
		grep -q "MINIO_SECRET_KEY=" .env && echo "  ✅ MINIO_SECRET_KEY configurada" || echo "  ❌ MINIO_SECRET_KEY não configurada"; \
		grep -q "LABELSTUDIO_TOKEN=" .env && echo "  ✅ LABELSTUDIO_TOKEN configurada" || echo "  ❌ LABELSTUDIO_TOKEN não configurada"; \
		grep -q "LABELSTUDIO_PROJECT=" .env && echo "  ✅ LABELSTUDIO_PROJECT configurada" || echo "  ❌ LABELSTUDIO_PROJECT não configurada"; \
	fi

# Setup completo para primeira execução
first-run: setup docker-up
	@echo ""
	@echo "=========================================="
	@echo "  🎉 Setup Completo Finalizado!"
	@echo "=========================================="
	@echo ""
	@echo "📋 Checklist:"
	@echo "  ✅ Ambiente conda criado"
	@echo "  ✅ Dependências instaladas"
	@echo "  ✅ Containers Docker iniciados"
	@echo ""
	@echo "👉 Próximos passos:"
	@echo "  1. Ative o ambiente: conda activate $(CONDA_ENV)"
	@echo "  2. Configure Label Studio token (ver README.md)"
	@echo "  3. Execute o pipeline: make pipeline"
	@echo "  4. Veja o dashboard: make dashboard"
	@echo ""
