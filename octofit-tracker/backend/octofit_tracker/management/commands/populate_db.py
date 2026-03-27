from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models

from django.contrib.auth.models import User

from pymongo import MongoClient

# Sample data
USERS = [
    {"name": "Tony Stark", "email": "tony@marvel.com", "team": "Marvel"},
    {"name": "Steve Rogers", "email": "steve@marvel.com", "team": "Marvel"},
    {"name": "Bruce Wayne", "email": "bruce@dc.com", "team": "DC"},
    {"name": "Clark Kent", "email": "clark@dc.com", "team": "DC"},
]

TEAMS = [
    {"name": "Marvel", "members": ["Tony Stark", "Steve Rogers"]},
    {"name": "DC", "members": ["Bruce Wayne", "Clark Kent"]},
]

ACTIVITIES = [
    {"user": "Tony Stark", "activity": "Running", "duration": 30},
    {"user": "Steve Rogers", "activity": "Cycling", "duration": 45},
    {"user": "Bruce Wayne", "activity": "Swimming", "duration": 60},
    {"user": "Clark Kent", "activity": "Flying", "duration": 120},
]

LEADERBOARD = [
    {"user": "Tony Stark", "points": 100},
    {"user": "Steve Rogers", "points": 90},
    {"user": "Bruce Wayne", "points": 110},
    {"user": "Clark Kent", "points": 120},
]

WORKOUTS = [
    {"name": "Super Strength", "suggested_for": "Clark Kent"},
    {"name": "Genius Tech", "suggested_for": "Tony Stark"},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient("mongodb://localhost:27017")
        db = client["octofit_db"]

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Insert data
        db.users.insert_many(USERS)
        db.teams.insert_many(TEAMS)
        db.activities.insert_many(ACTIVITIES)
        db.leaderboard.insert_many(LEADERBOARD)
        db.workouts.insert_many(WORKOUTS)

        # Ensure unique index on email
        db.users.create_index([("email", 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
