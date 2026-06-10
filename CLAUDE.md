# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Brazilian stock market dashboard — a Streamlit web app that visualizes performance of PETR4.SA (Petrobras), ITUB4.SA (Itaú), and VALE3.SA (Vale) throughout 2025.

## Commands

```powershell
# Install dependencies
cd acoes-2025
pip install -r requirements.txt

# Run the app (opens browser at http://localhost:8501)
streamlit run app.py
```

No build step, no test suite, no linter configured.

## Architecture

Single-file app: `acoes-2025/app.py`.

**Data flow:**
1. Sidebar date inputs (default Jan 2 – Dec 31, 2025) set the fetch window.
2. `carregar_dados(inicio, fim)` downloads OHLCV data from Yahoo Finance via `yfinance`, cached with `@st.cache_data(ttl=3600)`.
3. Metrics (return %, max, min, volatility) are computed from the cached DataFrame.
4. Four tabs render Plotly charts: closing price, cumulative return, daily return (bar), and volume (bar).
5. An optional checkbox exposes the raw DataFrame.

**Key constants** defined at the top of `app.py`:
- `ACOES` — dict mapping display name → ticker symbol
- `CORES` — dict mapping ticker → hex brand color (shared across all charts)
