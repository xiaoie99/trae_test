#!/usr/bin/env python3
# -*- coding=utf-8 -*-

# This file is kept for backward compatibility.
# Please use run.py to start the application with the new package structure.

import os
import sys
from pathlib import Path
import importlib.util

def main():
    # Get the current file path
    current_file_path = Path(__file__).resolve()
    current_dir = current_file_path.parent
    parent_dir = current_dir.parent
    sys.path.append(str(current_dir))
    sys.path.append(str(parent_dir))
    
    # Load and run the new entry point
    run_path = current_dir / 'run.py'
    spec = importlib.util.spec_from_file_location("run", run_path)
    run_module = importlib.util.module_from_spec(spec)
    sys.modules["run"] = run_module
    spec.loader.exec_module(run_module)
    
    if hasattr(run_module, "app"):
        app = run_module.app
        db_session = run_module.db_session
        return app, db_session

# For backward compatibility
app, db_session = main()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)