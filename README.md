# Running the API
```bash
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555
flask run
```

# URLS
```bash
http://localhost:5555/workouts
[Put in browser to see workouts]
http://localhost:5555/workouts/1
[Put in browser to see an individual workout]
http://localhost:5555/exercises
[Put in browser to see exercises]
http://localhost:5555/exercises/1
[Put in browser to see an individual exercise]
```
# Commands
```bash
curl -X POST http://localhost:5555/workouts -H "Content-Type: application/json" -d '{"date":"2025-08-22","duration_minutes":1,"notes":"Test workout"}'
[Add a workout to the database]
curl -X DELETE http://localhost:5555/workouts/1
[Delete a workout]
curl -X POST http://localhost:5555/exercises -H "Content-Type: application/json" -d '{"name":"Test","category":"Testing","equipment_needed":false}'
[Add an exercise to the database]
curl -X DELETE http://localhost:5555/exercises/1
[Delete an exercise]
curl -X POST http://localhost:5555/workouts/1/exercises/1/workout_exercises -H "Content-Type: application/json" -d '{"sets":1,"reps":1,"duration_seconds":0}'
[Add an exercise to a workout]
```