#!/usr/bin/env python3

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():
    Exercise.query.delete()
    Workout.query.delete()
    WorkoutExercise.query.delete()
    
    pushup = Exercise(name="Push-Up", category="Arms", equipment_needed=False)
    squat = Exercise(name="Squat", category="Legs", equipment_needed=False)
    bench_press = Exercise(name="Bench Press", category="Arms", equipment_needed=True)

    db.session.add_all([pushup, squat, bench_press])
    db.session.commit()

    arm_workout = Workout(date=date(2025, 8, 21), duration_minutes=60,notes="Arm Workout")
    leg_workout = Workout(date=date(2025, 8, 22), duration_minutes=45,notes="Leg Workout")
    db.session.add_all([arm_workout, leg_workout])
    db.session.commit()

    we1 = WorkoutExercise(workout=arm_workout, exercise=pushup, reps=10, sets=3, duration_seconds=60)
    we2 = WorkoutExercise(workout=arm_workout, exercise=bench_press, reps=15, sets=1, duration_seconds=120)
    we3 = WorkoutExercise(workout=leg_workout, exercise=squat, reps=10, sets=3, duration_seconds=90)
    db.session.add_all([we1, we2, we3])
    db.session.commit()