@echo off
set PYTHONOPTIMIZE=1
set PYTHONUNBUFFERED=1
set STREAMLIT_SERVER_PORT=8501
set STREAMLIT_SERVER_ADDRESS=127.0.0.1
set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
set PYTHONMALLOC=malloc

REM Increase memory limits
set PYTHONMALLOCSTATS=1
set PYTHONTRACEMALLOC=1

python -O -m streamlit run quick_app.py --server.port 8501 --server.address 127.0.0.1 