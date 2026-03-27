import sqlite3
from datetime import datetime

class JobDatabase:
    def __init__(self, db_name="jobs.db"):
        self.db_name = db_name
        self.create_table()

    def _connect(self):
        return sqlite3.connect(self.db_name)
    
    def create_table(self):
        with self._connect() as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    company TEXT,
                    job_title TEXT,
                    status TEXT DEFAULT 'Applied',
                    date_added TEXT               
                )
            ''')
            conn.commit()
    
    def add_job(self, url, company="Pending Scrape", job_title="Pending Scrape"):
        date_added = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO applications (url, company, job_title, status, date_added)
                VALUES (?, ?, ?, 'Applied', ?)
            ''', (url, company, job_title, date_added))
        conn.commit()
        return cursor.lastrowid

    def get_all_jobs(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, company, job_title, status, date_added
                FROM applications
                ORDER BY id DESC
            ''')
            return cursor.fetchall()
        
    def update_status(self, job_id, new_status):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE applications SET status = ? WHERE id == ?
            ''', (new_status, job_id))
            conn.commit()

    def delete_job(self, job_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM applications WHERE id = ?', (job_id,))
            
            cursor.execute('SELECT COUNT(*) FROM applications')
            count = cursor.fetchone()[0]

            if count == 0:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='applications'")
            
            conn.commit()