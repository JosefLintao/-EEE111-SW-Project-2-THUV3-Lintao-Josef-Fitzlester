import sqlite3

class LolDbSqlite:
    def __init__(self, dbName='Employees.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Champions (
                title TEXT PRIMARY KEY,
                name TEXT,
                role TEXT,
                gender TEXT,
                position TEXT)''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Champions (
                    title TEXT PRIMARY KEY,
                    name TEXT,
                    role TEXT,
                    gender TEXT,
                    position TEXT)''')
        self.commit_close()

    def fetch_champions(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Champions')
        employees =self.cursor.fetchall()
        self.conn.close()
        return employees

    def insert_champion(self, id, name, role, gender, status):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO Champions (id, name, role, gender, status) VALUES (?, ?, ?, ?, ?)',
                    (id, name, role, gender, status))
        self.commit_close()

    def delete_champion(self, id):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM Champions WHERE id = ?', (id,))
        self.commit_close()

    def update_champion(self, new_name, new_role, new_gender, new_status, id):
        self.connect_cursor()
        self.cursor.execute('UPDATE Champions SET name = ?, role = ?, gender = ?, status = ? WHERE id = ?',
                    (new_name, new_role, new_gender, new_status, id))
        self.commit_close()

    def id_exists(self, id):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM Champions WHERE id = ?', (id,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            dbEntries = self.fetch_champions()
            for entry in dbEntries:
                print(entry)
                filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]}\n")

def test_LolDb():
    iLolDb = LolDbSqlite(dbName='EmpDbSql.db')

    for entry in range(30):
        iLolDb.insert_champion(entry, f'Name{entry} Surname{entry}', f'SW Engineer {entry}', 'Male', 'On-Site')
        assert iLolDb.id_exists(entry)

    all_entries = iLolDb.fetch_champions()
    assert len(all_entries) == 30

    for entry in range(10, 20):
        iLolDb.update_champion(f'Name{entry} Surname{entry}', f'SW Engineer {entry}', 'Female', 'Remote', entry)
        assert iLolDb.id_exists(entry)

    all_entries = iLolDb.fetch_champions()
    assert len(all_entries) == 30

    for entry in range(10):
        iLolDb.delete_champion(entry)
        assert not iLolDb.id_exists(entry) 

    all_entries = iLolDb.fetch_champions()
    assert len(all_entries) == 20