from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint
from marshmallow import Schema, fields
db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    workout_exercises = db.relationship("WorkoutExercise", backref="exercise", cascade="all, delete")
    workouts = db.relationship("Workout", secondary="workout_exercises", back_populates="exercises", viewonly=True)

    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name empty")
        return value

    def __repr__(self):
        return f"<Exercise {self.name}>"
  
class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship("WorkoutExercise", backref="workout", cascade="all, delete")
    exercises = db.relationship("Exercise", secondary="workout_exercises", back_populates="workouts", viewonly=True)

    __table_args__ = (
        CheckConstraint("duration_minutes >= 0"),
    )

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Duration must be positive")
        return value

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

    __table_args__ = (
        CheckConstraint('reps >= 0'),
        CheckConstraint('sets >= 0'),
        CheckConstraint('duration_seconds >= 0'),
    )

    @validates('reps', 'sets', 'duration_seconds')
    def validate_positive(self, key, value):
        if value < 0:
            raise ValueError(f"{key} must be positive")
        return value

    def __repr__(self):
        return f"<Workout:{self.workout_id}, Exercise:{self.exercise_id}>"
    
class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(required=True)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str()
    workout_exercises = fields.Nested(lambda: WorkoutExerciseSchema, many=True)

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()