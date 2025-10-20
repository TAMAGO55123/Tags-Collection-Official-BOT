import sqlite3
class tag:
    def __init__(self) -> None:
        DB_FILE = 'database/new_tag.db'
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        # テーブルの作成
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tag (
                name TEXT PRIMARY KEY,
                invite TEXT,
                message_id TEXT
            )
        ''')
        self.conn.commit()
    
    def get_tag(self, name:str) -> int:
        self.cursor.execute('SELECT invite,message_id FROM tag WHERE name = ?', (name,))
        return self.cursor.fetchone()
    
    def update_invite(self, name:str, invite:str):
        self.cursor.execute('UPDATE tag SET invite = ? WHERE name = ?', (invite, name))
        self.conn.commit()
    
    def update_name(self, oldname:str, newname:str):
        self.cursor.execute('UPDATE tag SET name = ? WHERE name = ?', (newname, oldname))
        self.conn.commit()

    def create_tag(self, name:str, invite:str, message_id:str):
        self.cursor.execute('INSERT INTO tag (name, invite, message_id) VALUES (?, ?, ?)', (name, invite, message_id))
        self.conn.commit()
    
    def delete_tag(self, name:str):
        self.cursor.execute('DELETE FROM tag WHERE name = ?',(name,))
        self.conn.commit()
class tag2:
    def __init__(self) -> None:

        DB_FILE = 'database/new_tag.db'
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        # テーブルの作成
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tag (
                name TEXT PRIMARY KEY,
                invite TEXT,
                message_id TEXT
            )
        ''')
        self.conn.commit()
    
    def get_tag(self, name:str) -> int:
        self.cursor.execute('SELECT invite,message_id FROM tag WHERE name = ?', (name,))
        return self.cursor.fetchone()
    
    def update_invite(self, name:str, invite:str):
        self.cursor.execute('UPDATE tag SET invite = ? WHERE name = ?', (invite, name))
        self.conn.commit()
    
    def update_name(self, oldname:str, newname:str):
        self.cursor.execute('UPDATE tag SET name = ? WHERE name = ?', (newname, oldname))
        self.conn.commit()

    def create_tag(self, name:str, invite:str, message_id:str):
        self.cursor.execute('INSERT INTO tag (name, invite, message_id) VALUES (?, ?, ?)', (name, invite, message_id))
        self.conn.commit()
    
    def delete_tag(self, name:str):
        self.cursor.execute('DELETE FROM tag WHERE name = ?',(name,))
        self.conn.commit()