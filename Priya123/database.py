import sqlite3

def init_db():
    conn = sqlite3.connect('metadata.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            title TEXT,
            description TEXT,
            keywords TEXT,
            og_title TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_metadata(data):
    conn = sqlite3.connect('metadata.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO metadata (url, title, description, keywords, og_title)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['url'], data['title'], data['description'], data['keywords'], data['og_title']))
    conn.commit()
    conn.close()

def fetch_all_metadata():
    conn = sqlite3.connect('metadata.db')
    c = conn.cursor()
    c.execute('SELECT * FROM metadata')
    rows = c.fetchall()
    conn.close()
    return rows
