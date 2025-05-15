@echo off
set PYTHONOPTIMIZE=1
set PYTHONUNBUFFERED=1
set STREAMLIT_SERVER_PORT=8501
set STREAMLIT_SERVER_ADDRESS=127.0.0.1
set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

REM Set environment variables
set PYTHONPATH=%PYTHONPATH%;%CD%

REM Install required packages if not already installed
python -m pip install -r requirements.txt

REM Run the app
python -O -m streamlit run app.py --server.port 8501 --server.address 127.0.0.1 