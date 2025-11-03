# Fix for Streamlit + PyTorch RuntimeError

## Problem
The error occurs because of a conflict between PyTorch's `__path__` attribute and Streamlit's module watcher. This is a known compatibility issue.

## Solution Options

### Option 1: Environment Variable Fix (Recommended)
Set the following environment variable before running Streamlit:

**Windows (Command Prompt):**
```cmd
set STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
streamlit run app_new.py
```

**Windows (PowerShell):**
```powershell
$env:STREAMLIT_SERVER_FILE_WATCHER_TYPE="none"
streamlit run app_new.py
```

**Linux/Mac:**
```bash
export STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
streamlit run app_new.py
```

### Option 2: Streamlit Config File
Create or update `.streamlit/config.toml`:

```toml
[server]
fileWatcherType = "none"
```

### Option 3: Command Line Override
Run Streamlit with the file watcher disabled:

```bash
streamlit run app_new.py --server.fileWatcherType=none
```

## Quick Fix Script
Create this batch file to run the app easily:

**run_app.bat (Windows):**
```batch
@echo off
set STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
streamlit run app_new.py
```

**run_app.sh (Linux/Mac):**
```bash
#!/bin/bash
export STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
streamlit run app_new.py
```

## Why This Happens
- PyTorch registers custom C++ classes that don't have traditional Python `__path__` attributes
- Streamlit's file watcher tries to examine all loaded modules including PyTorch
- The conflict occurs when Streamlit tries to access `torch.classes.__path__._path`
- Disabling the file watcher resolves this without affecting functionality

## Alternative: Use Polling Watcher
If you need file watching for development:

```toml
[server]
fileWatcherType = "poll"
```

This uses polling instead of the problematic path examination.