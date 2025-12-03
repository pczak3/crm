# Simple CRM - Flask

This is a ready-to-run simple CRM built with Flask and SQLite.

## Quick start

1. Create a virtual environment and activate it.
2. `pip install -r requirements.txt`
3. (Optional) set environment variables from `.env` or edit `config.py`.
4. Initialize DB / migrations (if you want to use Flask-Migrate):
   - `flask db init` (already a migrations scaffold included)
   - `flask db migrate -m "initial"`
   - `flask db upgrade`
5. Or simply run the seeder to create the SQLite DB with sample data:
   - `python seed.py`
6. Run the app:
   - `python run.py`
7. Open http://127.0.0.1:5000/

Notes:
- The project includes placeholder local Bootstrap CSS/JS files in `app/static/` for offline usage.
- If you prefer the official Bootstrap distribution, replace `app/static/css/bootstrap.min.css` and `app/static/js/bootstrap.bundle.min.js` with the official files.
