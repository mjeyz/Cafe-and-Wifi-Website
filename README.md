# Cafe and Wifi Website — local run instructions

This repository is a small Flask app that lists cafes and shows details. I fixed templates, routes, and CSS to improve responsiveness and behavior.

Quick start (Windows PowerShell):

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Run the app

```powershell
python main.py
```

Notes
- Database file `instance/cafes.db` is included in the `instance/` folder. Ensure it exists and has a `cafe` table with the expected columns.
- This is a demo site: register/login flows use flash messages only and don't persist users yet.
- To build out further: add user persistence, input validation, tests, and production configuration.

If you'd like, I can:
- Add full responsive styles and a modern UI (cards, hero, theme colors).
- Implement register/login with password hashing and DB storage.
- Add a simple admin UI to add/edit cafes.
- Improve accessibility and SEO meta tags.
