from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

# Define Models here

class Exercise(db.Model):
  __tablename__ = "exercises"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False, unique=True)
  category = db.Column(db.String, nullable=False)
  equipment_needed = db.Column(db.Boolean, nullable=False)

  def __repr__(self):
    return f"<Exercise {self.name}>"
  
class Workout(db.Model):
  __tablename__ = "workouts"

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date, nullable=False)
  duration_minutes = db.Column(db.Integer, nullable=False)
  notes = db.Column(db.Text)

  def __repr__(self):
    return f"<Workout {self.id} ({self.date})>"
  
class WorkoutExercise(db.Model):
  __tablename__ = "workout_exercises"

  id = db.Column(db.Integer, primary_key=True)
  workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
  exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
  reps = db.Column(db.Integer)
  sets = db.Column(db.Integer)
  duration_seconds = db.Column(db.Integer)

  def __repr__(self):
    return f"<Workout:{self.workout_id}, Exercise:{self.exercise_id}>"