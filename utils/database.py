import sqlite3
import aiosqlite
import asyncio
from datetime import datetime
import os

class Database:
    def __init__(self, db_path='bot.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER UNIQUE,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    file_url TEXT,
                    file_name TEXT,
                    file_size INTEGER,
                    download_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'completed'
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY,
                    max_file_size INTEGER DEFAULT 2147483648,
                    allowed_users TEXT DEFAULT 'all'
                )
            ''')
            
            # Insert default settings if not exists
            conn.execute('INSERT OR IGNORE INTO settings (id) VALUES (1)')
            conn.commit()

    async def add_user(self, user_id, username, first_name, last_name):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'INSERT OR REPLACE INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)',
                (user_id, username, first_name, last_name)
            )
            await db.commit()

    async def add_download(self, user_id, file_url, file_name, file_size, status='completed'):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'INSERT INTO downloads (user_id, file_url, file_name, file_size, status) VALUES (?, ?, ?, ?, ?)',
                (user_id, file_url, file_name, file_size, status)
            )
            await db.commit()

    async def get_user_stats(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                'SELECT COUNT(*), SUM(file_size) FROM downloads WHERE user_id = ?',
                (user_id,)
            )
            result = await cursor.fetchone()
            return result or (0, 0)