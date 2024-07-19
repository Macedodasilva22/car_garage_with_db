from flask import request, jsonify, render_template, abort
from app import app, get_car_db, get_problem_db, get_relationship_db
from scripts.actions import (
    add_car, delete_car, search_cars, modify_car, 
    add_problem, update_problem_price, 
    add_car_problem, update_car_problem, 
    get_car_problems
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_car', methods=['POST'])
def add_car_route():
    data = request.form
    name = data.get('name')
    img = data.get('img')
    if not name or not img:
        abort(400, description="Name and image are required.")
    add_car(name, img)
    return 'Car added successfully', 201

@app.route('/delete_car/<int:car_id>', methods=['DELETE'])
def delete_car_route(car_id):
    delete_car(car_id)
    return 'Car deleted successfully', 200

@app.route('/search_cars', methods=['GET'])
def search_cars_route():
    name = request.args.get('name', '')
    cars = search_cars(name)
    cars_list = [{'id': car[0], 'name': car[1], 'img': car[2]} for car in cars]
    return jsonify(cars_list)

@app.route('/modify_car/<int:car_id>', methods=['PUT'])
def modify_car_route(car_id):
    data = request.form
    name = data.get('name')
    img = data.get('img')
    if not name or not img:
        abort(400, description="Name and image are required.")
    modify_car(car_id, name, img)
    return 'Car updated successfully', 200

@app.route('/add_problem', methods=['POST'])
def add_problem_route():
    data = request.form
    description = data.get('description')
    try:
        price = float(data.get('price'))
    except ValueError:
        abort(400, description="Price must be a valid number.")
    if not description:
        abort(400, description="Description is required.")
    add_problem(description, price)
    return 'Problem added successfully', 201

@app.route('/update_problem_price/<int:problem_id>', methods=['PUT'])
def update_problem_price_route(problem_id):
    data = request.form
    try:
        new_price = float(data.get('price'))
    except ValueError:
        abort(400, description="Price must be a valid number.")
    update_problem_price(problem_id, new_price)
    return 'Problem price updated successfully', 200

@app.route('/add_car_problem', methods=['POST'])
def add_car_problem_route():
    data = request.form
    try:
        car_id = int(data.get('car_id'))
        problem_id = int(data.get('problem_id'))
        cost = float(data.get('cost'))
    except (ValueError, TypeError):
        abort(400, description="Invalid data format.")
    status = data.get('status', 'active')
    add_car_problem(car_id, problem_id, cost, status)
    return 'Car-problem relationship added successfully', 201

@app.route('/update_car_problem/<int:car_problem_id>', methods=['PUT'])
def update_car_problem_route(car_problem_id):
    data = request.form
    try:
        problem_id = int(data.get('problem_id', 0))
        cost = float(data.get('cost', 0))
    except (ValueError, TypeError):
        abort(400, description="Invalid data format.")
    status = data.get('status')
    update_car_problem(car_problem_id, problem_id, cost, status)
    return 'Car-problem relationship updated successfully', 200

@app.route('/car_problems/<int:car_id>', methods=['GET'])
def car_problems_route(car_id):
    problems = get_car_problems(car_id)
    problems_list = [{'id': problem[0], 'name': problem[1], 'description': problem[2], 'cost': problem[3], 'status': problem[4]} for problem in problems]
    return jsonify(problems_list)
