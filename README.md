# AI Safety Learning Hub

A full-stack, interactive learning platform for AI safety and alignment fundamentals. Self-paced curriculum with 8 modules, 25+ lessons, auto-graded quizzes, and server-side progress tracking.

## Tech Stack
- **Backend:** Python Flask + SQLite (built-in, no database server needed)
- **Frontend:** Vanilla JavaScript (ES6+), CSS3 custom properties, responsive design
- **Zero external services** — runs entirely locally

## Features
- 8 progressive modules (AI basics → alignment → interpretability → governance → forecasting → capstone)
- Interactive quiz engine with instant feedback and 70% pass threshold
- Server-side progress tracking (SQLite) with progress dashboard
- Fully responsive (mobile + desktop)
- RESTful JSON API (`/api/modules`, `/api/progress`, `/api/stats`)

## Project Structure
```
aisafety-learning-hub/
├── README.md
├── requirements.txt
├── run.py                  # Entry point — starts everything
├── backend/
│   ├── app.py              # Flask API + serves frontend
│   ├── seed.py             # Curriculum seed data
│   └── database.db         # Created on first run
└── frontend/
    ├── index.html
    ├── css/style.css
    └── js/
        ├── helpers.js      # API client + UI utilities
        └── app.js          # App logic
```

## How to Run
```bash
pip install -r requirements.txt
python run.py
# Open http://localhost:5000
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/modules` | List all modules |
| GET | `/api/modules/:id/lessons` | Lessons for a module |
| GET | `/api/modules/:id/quiz` | Quiz questions |
| GET/POST | `/api/progress` | View / save quiz progress |
| GET | `/api/stats` | Platform statistics |

## Why This Project
AI safety talent is concentrated in a handful of countries. A free, structured, interactive curriculum lowers barriers for developers worldwide — especially in underrepresented regions — to enter the field.

## License
MIT
