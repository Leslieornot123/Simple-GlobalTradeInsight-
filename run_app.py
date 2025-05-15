import os
import sys
import subprocess
import time

def main():
    print("Setting up environment...")
    
    # Set environment variables
    os.environ['PYTHONOPTIMIZE'] = '1'
    os.environ['PYTHONUNBUFFERED'] = '1'
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = '127.0.0.1'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError:
        print("Warning: Could not install requirements. Continuing anyway...")
    
    print("Starting Streamlit app...")
    try:
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "streamlit", 
            "run", 
            "app.py",
            "--server.port", "8501",
            "--server.address", "127.0.0.1"
        ])
    except KeyboardInterrupt:
        print("\nApp stopped by user")
    except Exception as e:
        print(f"Error running app: {e}")

if __name__ == "__main__":
    main() 