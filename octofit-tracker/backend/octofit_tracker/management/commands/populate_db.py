from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Users
        users = [
            {"name": "Superman", "email": "superman@dc.com", "team": "dc"},
            {"name": "Batman", "email": "batman@dc.com", "team": "dc"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "dc"},
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "marvel"},
            {"name": "Black Widow", "email": "widow@marvel.com", "team": "marvel"},
        ]
        db.users.insert_many(users)
        db.users.create_index([("email", 1)], unique=True)

        # Teams
        teams = [
            {"name": "marvel", "members": ["Iron Man", "Captain America", "Black Widow"]},
            {"name": "dc", "members": ["Superman", "Batman", "Wonder Woman"]},
        ]
        db.teams.insert_many(teams)

        # Activities
        activities = [
            {"user": "Superman", "activity": "Flight", "duration": 60},
            {"user": "Batman", "activity": "Martial Arts", "duration": 45},
            {"user": "Wonder Woman", "activity": "Lasso Training", "duration": 30},
            {"user": "Iron Man", "activity": "Suit Test", "duration": 50},
            {"user": "Captain America", "activity": "Shield Practice", "duration": 40},
            {"user": "Black Widow", "activity": "Espionage", "duration": 35},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {"team": "marvel", "points": 125},
            {"team": "dc", "points": 135},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {"name": "Strength Training", "suggested_for": ["Superman", "Iron Man"]},
            {"name": "Agility Drills", "suggested_for": ["Batman", "Black Widow"]},
            {"name": "Endurance Run", "suggested_for": ["Wonder Woman", "Captain America"]},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
