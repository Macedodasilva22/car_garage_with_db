import sqlite3

def connect_db(db_name):
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as e:
        print(f'Error connecting to {db_name}: {e}')
        return None

def create_table(conn, create_table_sql):
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except sqlite3.Error as e:
        print(f'Error creating table: {e}')

def insert_initial_data(conn, insert_sql, data):
    try:
        cursor = conn.cursor()
        cursor.executemany(insert_sql, data)
    except sqlite3.IntegrityError:
        print("Initial data already exists.")
    except sqlite3.Error as e:
        print(f'Error inserting initial data: {e}')

def init_car_db():
    conn = connect_db('cars.db')
    if conn:
        create_table(conn, '''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            img TEXT NOT NULL
        )
        ''')
        insert_initial_data(conn, 
            "INSERT INTO cars (name, img) VALUES (?, ?)", 
            [('Toyota Corolla', 'toyota_corolla.jpg'),
             ('Honda Civic', 'honda_civic.jpg')]
        )
        conn.commit()
        conn.close()

def init_problem_db():
    conn = connect_db('problems.db')
    if conn:
        create_table(conn, '''
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            price REAL NOT NULL
        )
        ''')
        insert_initial_data(conn,
            "INSERT INTO problems (description, price) VALUES (?, ?)",
            [('Engine issue', 300.00),
             ('Brake replacement', 150.00)]
        )
        conn.commit()
        conn.close()

def init_relationship_db():
    conn = connect_db('car_problems.db')
    if conn:
        create_table(conn, '''
        CREATE TABLE IF NOT EXISTS car_problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id INTEGER NOT NULL,
            problem_id INTEGER NOT NULL,
            cost REAL NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (car_id) REFERENCES cars (id),
            FOREIGN KEY (problem_id) REFERENCES problems (id)
        )
        ''')
        conn.commit()
        conn.close()
        print("Car-problems relationship table initialized.")

if __name__ == '__main__':
    init_car_db()
    init_problem_db()
    init_relationship_db()
