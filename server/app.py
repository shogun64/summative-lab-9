from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise, ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    return jsonify(workout_schema.dump(workout)), 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    try:
        schema = workout_schema.load(data)
        workout = Workout(**schema)
        db.session.add(workout)
        db.session.commit()
        return jsonify(workout_schema.dump(workout)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/workouts/<int:id>', methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": f"Workout {id} deleted"}), 200

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    return jsonify(exercise_schema.dump(exercise)), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    try:
        schema = exercise_schema.load(data)
        exercise = Exercise(**schema)
        db.session.add(exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(exercise)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": f"Exercise {id} deleted"}), 200

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    data = request.get_json()
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    elif not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    data["workout_id"] = workout_id
    data["exercise_id"] = exercise_id
    try:
        schema = workout_exercise_schema.load(data)
        workout_exercise = WorkoutExercise(**schema)
        db.session.add(workout_exercise)
        db.session.commit()
        return jsonify(workout_exercise_schema.dump(workout_exercise)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
