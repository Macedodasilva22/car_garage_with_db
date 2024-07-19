import sqlite3

def get_car_db():
    return sqlite3.connect('cars.db')

def get_problem_db():
    return sqlite3.connect('problems.db')

def get_relationship_db():
    return sqlite3.connect('car_problems.db')

# Car actions
def add_car(name, img):
    try:
        with get_car_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO cars (name, img) VALUES (?, ?)', (name, img))
            conn.commit()
            print("Car added successfully.")
    except sqlite3.Error as e:
        print(f'Error adding car: {e}')

def delete_car(car_id):
    try:
        with get_car_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cars WHERE id = ?', (car_id,))
            conn.commit()
            print("Car deleted successfully.")
    except sqlite3.Error as e:
        print(f'Error deleting car: {e}')

def search_cars(name):
    try:
        with get_car_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cars WHERE name LIKE ?', (f'%{name}%',))
            cars = cursor.fetchall()
            return cars
    except sqlite3.Error as e:
        print(f'Error searching cars: {e}')
        return []

def modify_car(car_id, name, img):
    try:
        with get_car_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE cars SET name = ?, img = ? WHERE id = ?', (name, img, car_id))
            conn.commit()
            print("Car updated successfully.")
    except sqlite3.Error as e:
        print(f'Error modifying car: {e}')

# Problem actions
def add_problem(description, price):
    try:
        with get_problem_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO problems (description, price) VALUES (?, ?)', (description, price))
            conn.commit()
            print("Problem added successfully.")
    except sqlite3.Error as e:
        print(f'Error adding problem: {e}')

def update_problem_price(problem_id, new_price):
    try:
        with get_problem_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE problems SET price = ? WHERE id = ?', (new_price, problem_id))
            conn.commit()
            print("Problem price updated successfully.")
    except sqlite3.Error as e:
        print(f'Error updating problem price: {e}')

# Relationship actions
def add_car_problem(car_id, problem_id, cost, status='active'):
    try:
        with get_relationship_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO car_problems (car_id, problem_id, cost, status) VALUES (?, ?, ?, ?)',
                           (car_id, problem_id, cost, status))
            conn.commit()
            print("Car-problem relationship added successfully.")
    except sqlite3.Error as e:
        print(f'Error adding car-problem relationship: {e}')

def update_car_problem(car_problem_id, problem_id=None, cost=None, status=None):
    try:
        with get_relationship_db() as conn:
            cursor = conn.cursor()
            
            # Build the update statement
            updates = []
            params = []
            if problem_id is not None:
                updates.append('problem_id = ?')
                params.append(problem_id)
            if cost is not None:
                updates.append('cost = ?')
                params.append(cost)
            if status is not None:
                updates.append('status = ?')
                params.append(status)
            
            updates_str = ', '.join(updates)
            
            if updates_str:
                params.append(car_problem_id)
                cursor.execute(f'UPDATE car_problems SET {updates_str} WHERE id = ?', tuple(params))
                conn.commit()
            print("Car-problem relationship updated successfully.")
    except sqlite3.Error as e:
        print(f'Error updating car-problem relationship: {e}')

def get_car_problems(car_id):
    try:
        with get_relationship_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT cp.id, c.name, p.description, cp.cost, cp.status
            FROM car_problems cp
            JOIN cars c ON cp.car_id = c.id
            JOIN problems p ON cp.problem_id = p.id
            WHERE cp.car_id = ?
            ''', (car_id,))
            problems = cursor.fetchall()
            return problems
    except sqlite3.Error as e:
        print(f'Error fetching car problems: {e}')
        return []
