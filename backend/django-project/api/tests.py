from datetime import timedelta

from django.test import override_settings
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from accounts.models import User, Friendship
from hackathons.models import Hackathon, Team, TeamMembership, HackathonTeam


@override_settings(
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
)
class AuthViewsTests(APITestCase):
    def test_signup_sets_cookie_and_returns_payload(self):
        resp = self.client.post(
            "/api/signup/",
            {
                "email": "newuser@example.edu",
                "password": "pass123",
                "username": "newbie",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", resp.data)
        self.assertIn("auth_token", resp.cookies)

    def test_login_returns_payload(self):
        user = User.objects.create_user(
            email="login@example.edu", username="login", password="pass123"
        )
        resp = self.client.post(
            "/api/login/",
            {"email": "login@example.edu", "password": "pass123"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("auth_token", resp.cookies)
        self.assertEqual(resp.data["user"]["uuid"], str(user.id))


@override_settings(
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
)
class InitAndListingTests(APITestCase):
    def setUp(self):
        self.client: APIClient
        self.user = User.objects.create_user(
            email="u1@example.edu", username="u1", password="pass123"
        )
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.cookies["auth_token"] = self.token.key

        future = timezone.now() + timedelta(days=2)
        self.hackathon = Hackathon.objects.create(
            name="Future Hack",
            description="desc",
            start_date=future,
            end_date=future + timedelta(days=1),
        )
        self.team = Team.objects.create(name="Team A")
        TeamMembership.objects.create(user=self.user, team=self.team)
        HackathonTeam.objects.create(hackathon=self.hackathon, team=self.team, placement=None)

    def test_init_returns_bootstrap(self):
        resp = self.client.get("/api/init/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("user", resp.data)
        self.assertIn("hackathons", resp.data)
        self.assertIn("friends", resp.data)

    def test_user_hackathons_lists_upcoming(self):
        resp = self.client.get("/api/user/hackathons?offset=0&limit=5")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data["hackathons"]), 1)
        self.assertEqual(resp.data["hackathons"][0]["uuid"], str(self.hackathon.id))

    def test_user_past_hackathons_lists_completed(self):
        past_start = timezone.now() - timedelta(days=5)
        past_h = Hackathon.objects.create(
            name="Past Hack",
            description="old",
            start_date=past_start,
            end_date=past_start + timedelta(days=1),
        )
        HackathonTeam.objects.create(hackathon=past_h, team=self.team, placement=2)

        resp = self.client.get("/api/user/past-hackathons?offset=0&limit=5")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data["hackathons"]), 1)
        self.assertEqual(resp.data["hackathons"][0]["placement"], 2)

    def test_user_friends_lists_friendships(self):
        other = User.objects.create_user(
            email="friend@example.edu", username="friend", password="pass123"
        )
        Friendship.objects.create(user=self.user, friend=other)
        resp = self.client.get("/api/user/friends?offset=0&limit=5")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data["friends"]), 1)
        self.assertEqual(resp.data["friends"][0]["uuid"], str(other.id))


@override_settings(
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
)
class HackathonViewsTests(APITestCase):
    def setUp(self):
        self.client: APIClient
        self.user = User.objects.create_user(
            email="searcher@example.edu", username="searcher", password="pass123"
        )
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.cookies["auth_token"] = self.token.key

        now = timezone.now()
        self.hack = Hackathon.objects.create(
            name="Searchable Hack",
            description="desc",
            start_date=now + timedelta(days=1),
            end_date=now + timedelta(days=2),
        )
        team1 = Team.objects.create(name="Alpha")
        team2 = Team.objects.create(name="Beta")
        TeamMembership.objects.create(user=self.user, team=team1)
        HackathonTeam.objects.create(hackathon=self.hack, team=team1, placement=1)
        HackathonTeam.objects.create(hackathon=self.hack, team=team2, placement=2)

    def test_search_returns_hackathon_with_leaderboard(self):
        resp = self.client.get("/api/hackathons?offset=0&limit=5&query=Searchable")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data["hackathons"]), 1)
        hack = resp.data["hackathons"][0]
        self.assertEqual(hack["uuid"], str(self.hack.id))
        self.assertIsNotNone(hack["leaderboard"])
        self.assertEqual(len(hack["leaderboard"]), 2)

    def test_leaderboard_pagination(self):
        resp = self.client.get(f"/api/hackathon/{self.hack.id}/leaderboard?offset=0&limit=1")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data["leaderboard"]), 1)
        self.assertEqual(resp.data["leaderboard"][0]["placement"], 1)


@override_settings(
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
)
class LookupViewsTests(APITestCase):
    def setUp(self):
        self.client: APIClient
        self.user = User.objects.create_user(
            email="looker@example.edu", username="looker", password="pass123"
        )
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.cookies["auth_token"] = self.token.key

        self.other = User.objects.create_user(
            email="target@example.edu", username="target", password="pass123"
        )
        now = timezone.now()
        self.team = Team.objects.create(name="Lookup Team")
        TeamMembership.objects.create(user=self.other, team=self.team)
        past_h = Hackathon.objects.create(
            name="Lookup Past",
            description="old",
            start_date=now - timedelta(days=5),
            end_date=now - timedelta(days=4),
        )
        HackathonTeam.objects.create(hackathon=past_h, team=self.team, placement=3)

    def test_user_lookup_returns_profile(self):
        resp = self.client.get(f"/api/user/lookup?uuid={self.other.id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("user", resp.data)
        self.assertEqual(resp.data["user"]["uuid"], str(self.other.id))
        self.assertIn("past_hackathons", resp.data["user"])

    def test_user_history_paginated(self):
        resp = self.client.get(f"/api/user/lookup/{self.other.id}/history?offset=0&limit=5")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("hackathons", resp.data)
        self.assertGreaterEqual(len(resp.data["hackathons"]), 1)

    def test_team_lookup_returns_profile(self):
        resp = self.client.get(f"/api/team/lookup?uuid={self.team.id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("team", resp.data)
        self.assertEqual(resp.data["team"]["uuid"], str(self.team.id))
        self.assertIn("past_hackathons", resp.data["team"])

    def test_team_history_paginated(self):
        resp = self.client.get(f"/api/team/{self.team.id}/history?offset=0&limit=5")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("hackathons", resp.data)
        self.assertGreaterEqual(len(resp.data["hackathons"]), 1)

