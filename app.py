#!/usr/bin/env python3
"""
AI Safety Learning Hub — Flask API Backend
Run: python run.py  (serves both API and frontend on http://localhost:5000)
"""
import os, sqlite3, json
from datetime import datetime, timezone
from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
DB_PATH = os.path.join(BASE_DIR, "database.db")

app = Flask(__name__, static_folder=None)

# ------------------------------------------------------------
# Database helpers
# ------------------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS modules (
        id INTEGER PRIMARY KEY, title TEXT NOT NULL, level TEXT, duration TEXT,
        summary TEXT, sort_order INTEGER
    );
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY, module_id INTEGER, title TEXT, body TEXT,
        FOREIGN KEY(module_id) REFERENCES modules(id)
    );
    CREATE TABLE IF NOT EXISTS quiz_questions (
        id INTEGER PRIMARY KEY, module_id INTEGER, question TEXT,
        options TEXT, correct_index INTEGER,
        FOREIGN KEY(module_id) REFERENCES modules(id)
    );
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY, user_name TEXT, module_id INTEGER,
        score INTEGER, total INTEGER, completed_at TEXT,
        FOREIGN KEY(module_id) REFERENCES modules(id)
    );
    """)
    # Seed if empty
    cur = conn.execute("SELECT COUNT(*) FROM modules")
    if cur.fetchone()[0] == 0:
        from seed import seed_data
        seed_data(conn)
    conn.commit()
    conn.close()

# ------------------------------------------------------------
# API Routes
# ------------------------------------------------------------
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "AI Safety Learning Hub", "time": datetime.now(timezone.utc).isoformat()})

@app.route("/api/modules")
def get_modules():
    conn = get_db()
    rows = conn.execute("SELECT * FROM modules ORDER BY sort_order").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/modules/<int:mid>/lessons")
def get_lessons(mid):
    conn = get_db()
    rows = conn.execute("SELECT * FROM lessons WHERE module_id=?", (mid,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/modules/<int:mid>/quiz")
def get_quiz(mid):
    conn = get_db()
    rows = conn.execute("SELECT * FROM quiz_questions WHERE module_id=?", (mid,)).fetchall()
    conn.close()
    out = []
    for r in rows:
        d = dict(r)
        d["options"] = json.loads(d["options"])
        out.append(d)
    return jsonify(out)

@app.route("/api/progress", methods=["GET", "POST"])
def progress():
    conn = get_db()
    if request.method == "POST":
        data = request.json
        conn.execute(
            "INSERT INTO progress (user_name, module_id, score, total, completed_at) VALUES (?,?,?,?,?)",
            (data.get("user_name", "anonymous"), data["module_id"], data["score"],
             data["total"], datetime.now(timezone.utc).isoformat())
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "saved"})
    rows = conn.execute("SELECT p.*, m.title as module_title FROM progress p JOIN modules m ON p.module_id=m.id ORDER BY p.completed_at DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/stats")
def stats():
    conn = get_db()
    mods = conn.execute("SELECT COUNT(*) FROM modules").fetchone()[0]
    lessons = conn.execute("SELECT COUNT(*) FROM lessons").fetchone()[0]
    completed = conn.execute("SELECT COUNT(*) FROM progress").fetchone()[0]
    conn.close()
    return jsonify({"modules": mods, "lessons": lessons, "completed": completed})


# ------------------------------------------------------------
# Serve frontend (single-page app)
# ------------------------------------------------------------
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_DIR, path)

if __name__ == "__main__":
    init_db()
    print("  AI Safety Learning Hub running at http://localhost:5000")
    app.run(debug=True, port=5000)
