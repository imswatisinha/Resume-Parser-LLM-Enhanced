@echo off
echo Starting Resume Parser with PyTorch compatibility fix...
set STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
streamlit run app_new.py --server.port 8501 --server.headless false
pause