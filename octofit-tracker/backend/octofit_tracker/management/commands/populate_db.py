from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email
        db.users.create_index({'email': 1}, unique=True)

        # Sample users
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'Marvel'},
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': 'Marvel'},
            {'name': 'Superman', 'email': 'superman@dc.com', 'team': 'DC'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'DC'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'DC'},
        ]
        db.users.insert_many(users)

        # Teams
        teams = [
            {'name': 'Marvel', 'members': ['ironman@marvel.com', 'cap@marvel.com', 'spiderman@marvel.com']},
            {'name': 'DC', 'members': ['superman@dc.com', 'batman@dc.com', 'wonderwoman@dc.com']},
        ]
        db.teams.insert_many(teams)

        # Activities
        activities = [
            {'user': 'ironman@marvel.com', 'activity': 'Running', 'duration': 30},
            {'user': 'superman@dc.com', 'activity': 'Flying', 'duration': 60},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'team': 'Marvel', 'points': 300},
            {'team': 'DC', 'points': 250},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'user': 'batman@dc.com', 'workout': 'Strength', 'reps': 50},
            {'user': 'spiderman@marvel.com', 'workout': 'Agility', 'reps': 40},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
