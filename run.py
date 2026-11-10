#!/usr/bin/env python3
"""Entry point — starts the full-stack app (backend + frontend)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
from app import app, init_db

if __name__ == "__main__":
    init_db()
    print("=" * 55)
    print("  App running at http://localhost:5000")
    print("  Press Ctrl+C to stop")
    print("=" * 55)
    app.run(debug=True, port=5000)
