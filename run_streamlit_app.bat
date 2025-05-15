@echo off

:: Install required Python packages
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

:: Run the Streamlit app
streamlit run app.py

echo.
echo If your browser did not open automatically, open http://localhost:8501 manually.
pause 