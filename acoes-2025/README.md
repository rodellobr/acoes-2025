# Dashboard de Ações Brasileiras 2025

App web em Python para visualizar e analisar a performance das ações **PETR4** (Petrobras), **ITUB4** (Itaú) e **VALE3** (Vale) ao longo de 2025.

## Pré-requisitos

- Python 3.8 ou superior
- Conexão com a internet (dados buscados em tempo real via Yahoo Finance)

## Instalação

```powershell
# Entre na pasta do projeto
cd acoes-2025

# Instale as dependências
pip install -r requirements.txt
```

## Como rodar

```powershell
streamlit run app.py
```

O app abre automaticamente no navegador em `http://localhost:8501`.

## Funcionalidades

- **Preço de Fechamento** — evolução diária das 3 ações no período
- **Performance Acumulada (%)** — comparação de rendimento desde o início do período
- **Retorno Diário (%)** — variação percentual dia a dia
- **Volume Negociado** — volume diário de cada ação
- **Métricas resumo** — retorno total, máximo, mínimo e volatilidade
- **Filtro de datas** — selecione qualquer intervalo dentro de 2025
- **Tabela de dados brutos** — exportável (opcional)
