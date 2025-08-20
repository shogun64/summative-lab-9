from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

# Define Models here

class Exercise(db.Model):
  __tablename__ = 'exercises'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False, unique=True)
  category = db.Column(db.String, nullable=False)
  equipment_needed = db.Column(db.Boolean, nullable=False)

  def __repr__(self):
    return f"<Exercise {self.name}>"