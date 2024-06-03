# init_db.py
import os
from app import create_app, db

app = create_app()

# Specify absolute path for database file
db_path = os.path.join(app.root_path, 'site.db')

with app.app_context():
    db.create_all()
    print("Database tables created.")
