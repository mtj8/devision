import random
from typing import List, Optional

from django.contrib.auth import authenticate
from django.db import models
from django.db.models import Q
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User, Friendship
from hackathons.models import Hackathon, HackathonTeam, Team


# --------------------------------------------------
# Helpers
# --------------------------------------------------


def _hex_distance(a: str, b: str) -> int:
    """Rough distance between two hex colors."""
    a_int = int(a, 16)
    b_int = int(b, 16)
    return abs(a_int - b_int)


def generate_gradient() -> List[str]:
    """Generate two hex strings with some separation."""
    first = f"{random.randint(0, 0xFFFFFF):06x}"
    second = f"{random.randint(0, 0xFFFFFF):06x}"
    while _hex_distance(first, second) < 10_000:
        second = f"{random.randint(0, 0xFFFFFF):06x}"
    return [first, second]


def compute_xp_needed(level: int, xp: int) -> int:
    target = max(level, 1) * 100
    return max(target - xp, 0)


def ensure_user_defaults(user: User):
    """Ensure gradients/xp_needed have reasonable defaults."""
    changed = False
    if not user.profile_gradient:
        user.profile_gradient = generate_gradient()
        changed = True
    expected_needed = compute_xp_needed(user.level or 1, user.xp or 0)
    if user.xp_needed != expected_needed:
        user.xp_needed = expected_needed
        changed = True
    if changed:
        user.save(update_fields=["profile_gradient", "xp_needed"])


def parse_pagination(request):
    try:
        offset = int(request.query_params.get("offset", 0))
        limit = int(request.query_params.get("limit", 10))
    except ValueError:
        return None, None
    offset = max(offset, 0)
    limit = max(min(limit, 50), 1)
    return offset, limit


def friendship_since(current_user: Optional[User], other: User) -> Optional[int]:
    if not current_user or current_user.is_anonymous:
        return None
    link = (
        Friendship.objects.filter(
            Q(user=current_user, friend=other) | Q(user=other, friend=current_user)
        )
        .order_by("created_at")
        .first()
    )
    if not link:
        return None
    return int(link.created_at.timestamp())


def is_blocked(current_user: Optional[User], other: User) -> bool:
    if not current_user or current_user.is_anonymous:
        return False
    return str(other.id) in (current_user.blocked or [])


def serialize_user_core(user: User, current_user: Optional[User] = None, include_email=True):
    ensure_user_defaults(user)
    return {
        "uuid": str(user.id),
        "created_at": int(user.date_joined.timestamp()),
        "profile_gradient": tuple(user.profile_gradient) if user.profile_gradient else None,
        "display_name": user.first_name or user.username or user.email.split("@")[0],
        "username": user.username,
        "school": user.school.name if user.school else None,
        "grad_year": str(user.grad_year) if user.grad_year else None,
        "level": user.level,
        "email": user.email if include_email else None,
        "xp": user.xp,
        "xp_needed": user.xp_needed,
        "is_public": user.visibility == "public",
        "bio": user.bio or "",
        "socials": {
            "discord": user.discord,
            "instagram": user.instagram,
            "github": user.github,
            "linkedin": user.linkedin,
            "personal": user.personal,
        },
        "skills": [s.name for s in user.skills.all()],
        "interests": [i.name for i in user.interests.all()],
        "friends_since": friendship_since(current_user, user),
        "is_blocked": is_blocked(current_user, user),
    }


def serialize_team_members(team: Team, current_user: Optional[User], exclude_user: Optional[User] = None):
    members = []
    qs = team.members.all()
    if exclude_user:
        qs = qs.exclude(id=exclude_user.id)
    for member in qs:
        members.append(
            {
                "uuid": str(member.id),
                "friends_since": friendship_since(current_user, member),
                "profile_gradient": tuple(member.profile_gradient) if member.profile_gradient else None,
                "display_name": member.first_name or member.username,
                "username": member.username,
                "level": member.level,
                "is_blocked": is_blocked(current_user, member),
            }
        )
    return members


def serialize_team(team: Team, current_user: Optional[User], exclude_user: Optional[User] = None):
    return {
        "uuid": str(team.id),
        "name": team.name,
        "created_at": int(team.created_at.timestamp()),
        "members": serialize_team_members(team, current_user, exclude_user=exclude_user),
    }


def serialize_hackathon(hackathon: Hackathon, current_user: Optional[User], include_user_team=False, include_leaderboard=False):
    payload = {
        "uuid": str(hackathon.id),
        "name": hackathon.name,
        "description": hackathon.description,
        "start_date": int(hackathon.start_date.timestamp()),
        "end_date": int(hackathon.end_date.timestamp()),
        "participants": hackathon.participants_count,
    }

    if include_user_team and current_user:
        entry = (
            HackathonTeam.objects.filter(hackathon=hackathon, team__members=current_user)
            .select_related("team")
            .first()
        )
        payload["team"] = serialize_team(entry.team, current_user, exclude_user=current_user) if entry else None
        payload["placement"] = entry.placement if entry else None
    else:
        payload["team"] = None
        payload["placement"] = None

    if include_leaderboard:
        leaderboard_entries = (
            HackathonTeam.objects.filter(hackathon=hackathon, placement__isnull=False)
            .select_related("team")
            .order_by("placement")[:10]
        )
        leaderboard = []
        for entry in leaderboard_entries:
            leaderboard.append(
                {
                    "placement": entry.placement,
                    "uuid": str(entry.team.id),
                    "name": entry.team.name,
                    "created_at": int(entry.team.created_at.timestamp()),
                    "members": serialize_team_members(entry.team, current_user),
                }
            )
        payload["leaderboard"] = leaderboard or None
    return payload


def serialize_friend(friendship: Friendship, current_user: User, reverse=False):
    other = friendship.friend if friendship.user == current_user else friendship.user
    ensure_user_defaults(other)
    return {
        "uuid": str(other.id),
        "friends_since": int(friendship.created_at.timestamp()),
        "profile_gradient": tuple(other.profile_gradient) if other.profile_gradient else None,
        "display_name": other.first_name or other.username,
        "username": other.username,
        "level": other.level,
        "is_blocked": is_blocked(current_user, other),
    }


def best_placement_for_user(user: User):
    entry = (
        HackathonTeam.objects.filter(team__members=user, placement__isnull=False)
        .select_related("hackathon")
        .order_by("placement", "-hackathon__end_date")
        .first()
    )
    if not entry:
        return None
    h = entry.hackathon
    return {
        "uuid": str(h.id),
        "name": h.name,
        "description": h.description,
        "start_date": int(h.start_date.timestamp()),
        "end_date": int(h.end_date.timestamp()),
        "participants": h.participants_count,
        "placement": entry.placement,
    }


def past_hackathons_for_user(user: User, offset=0, limit=5):
    now = timezone.now()
    entries = (
        HackathonTeam.objects.filter(team__members=user, hackathon__end_date__lt=now, placement__isnull=False)
        .select_related("hackathon")
        .order_by("-hackathon__end_date")[offset : offset + limit]
    )
    data = []
    for entry in entries:
        h = entry.hackathon
        data.append(
            {
                "uuid": str(h.id),
                "name": h.name,
                "description": h.description,
                "start_date": int(h.start_date.timestamp()),
                "end_date": int(h.end_date.timestamp()),
                "participants": h.participants_count,
                "placement": entry.placement,
            }
        )
    return data


def past_hackathons_for_team(team: Team, offset=0, limit=5):
    now = timezone.now()
    entries = (
        HackathonTeam.objects.filter(team=team, hackathon__end_date__lt=now, placement__isnull=False)
        .select_related("hackathon")
        .order_by("-hackathon__end_date")[offset : offset + limit]
    )
    data = []
    for entry in entries:
        h = entry.hackathon
        data.append(
            {
                "uuid": str(h.id),
                "name": h.name,
                "description": h.description,
                "start_date": int(h.start_date.timestamp()),
                "end_date": int(h.end_date.timestamp()),
                "participants": h.participants_count,
                "placement": entry.placement,
            }
        )
    return data


def build_bootstrap_payload(user: User):
    now = timezone.now()
    upcoming_entries = (
        HackathonTeam.objects.filter(team__members=user, hackathon__end_date__gte=now)
        .select_related("hackathon", "team")
        .order_by("hackathon__start_date")[:5]
    )
    hackathons = []
    for entry in upcoming_entries:
        hackathons.append(serialize_hackathon(entry.hackathon, user, include_user_team=True))

    friends = [
        serialize_friend(f, user)
        for f in Friendship.objects.filter(Q(user=user) | Q(friend=user))
        .order_by("-created_at")[:5]
    ]

    return {
        "user": serialize_user_core(user),
        "hackathons": hackathons,
        "friends": friends,
    }


def set_auth_cookie(response: Response, token_key: str):
    response.set_cookie(
        "auth_token",
        token_key,
        httponly=True,
        samesite="Lax",
        secure=False,
    )


# --------------------------------------------------
# Views
# --------------------------------------------------


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        username = request.data.get("username") or email.split("@")[0]
        if not email or not password:
            return Response({"detail": "email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"detail": "email already registered"}, status=status.HTTP_400_BAD_REQUEST)

        gradient = generate_gradient()
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            profile_gradient=gradient,
            xp=0,
            level=1,
            xp_needed=compute_xp_needed(1, 0),
        )

        token, _ = Token.objects.get_or_create(user=user)
        payload = build_bootstrap_payload(user)
        response = Response(payload, status=status.HTTP_201_CREATED)
        set_auth_cookie(response, token.key)
        return response


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return Response({"detail": "email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        payload = build_bootstrap_payload(user)
        response = Response(payload)
        set_auth_cookie(response, token.key)
        return response


class InitView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        payload = build_bootstrap_payload(request.user)
        return Response(payload)


class UserHackathonsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        offset, limit = parse_pagination(request)
        if offset is None:
            return Response({"detail": "Invalid pagination"}, status=status.HTTP_400_BAD_REQUEST)
        now = timezone.now()
        entries = (
            HackathonTeam.objects.filter(team__members=request.user, hackathon__end_date__gte=now)
            .select_related("hackathon", "team")
            .order_by("hackathon__start_date")[offset : offset + limit]
        )
        hackathons = [serialize_hackathon(entry.hackathon, request.user, include_user_team=True) for entry in entries]
        return Response({"hackathons": hackathons})


class UserPastHackathonsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        offset, limit = parse_pagination(request)
        if offset is None:
            return Response({"detail": "Invalid pagination"}, status=status.HTTP_400_BAD_REQUEST)
        now = timezone.now()
        entries = (
            HackathonTeam.objects.filter(team__members=request.user, hackathon__end_date__lt=now)
            .select_related("hackathon", "team")
            .order_by("-hackathon__end_date")[offset : offset + limit]
        )
        hackathons = []
        for entry in entries:
            h = entry.hackathon
            payload = serialize_hackathon(h, request.user, include_user_team=True)
            payload["placement"] = entry.placement
            hackathons.append(payload)
        return Response({"hackathons": hackathons})


class UserFriendsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        offset, limit = parse_pagination(request)
        if offset is None:
            return Response({"detail": "Invalid pagination"}, status=status.HTTP_400_BAD_REQUEST)
        friendships = (
            Friendship.objects.filter(Q(user=request.user) | Q(friend=request.user))
            .order_by("created_at")[offset : offset + limit]
        )
        friends = [serialize_friend(f, request.user) for f in friendships]
        return Response({"friends": friends})


class HackathonSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        offset, limit = parse_pagination(request)
        if offset is None:
            return Response({"detail": "Invalid pagination"}, status=status.HTTP_400_BAD_REQUEST)

        query = request.query_params.get("query", "")
        qs = Hackathon.objects.all()
        if query:
            qs = qs.filter(name__icontains=query)

        qs = (
            qs.annotate(participant_estimate=models.Count("hackathon_teams__team__members", distinct=True))
            .order_by("-participant_estimate")
        )[offset : offset + limit]

        hackathons = []
        for hackathon in qs:
            payload = serialize_hackathon(hackathon, request.user, include_user_team=True, include_leaderboard=True)
            hackathons.append(payload)

        return Response({"hackathons": hackathons})


class HackathonLeaderboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, hackathon_id):
        offset, limit = parse_pagination(request)
        if offset is None:
            return Response({"detail": "Invalid pagination"}, status=status.HTTP_400_BAD_REQUEST)

        entries = (
            HackathonTeam.objects.filter(hackathon_id=hackathon_id, placement__isnull=False)
            .select_related("team")
            .order_by("placement")[offset : offset + limit]
        )
        leaderboard = []
        for entry in entries:
            leaderboard.append(
                {
                    "placement": entry.placement,
                    "uuid": str(entry.team.id),
                    "name": entry.team.name,
                    "created_at": int(entry.team.created_at.timestamp()),
                    "members": serialize_team_members(entry.team, request.user),
                }
            )
        return Response({"leaderboard": leaderboard})


class UserLookupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get("uuid")
        if not user_id:
            return Response({"detail": "uuid is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            target = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        data = serialize_user_core(target, current_user=request.user)
        data["best_placement"] = best_placement_for_user(target)
        data["past_hackathons"] = past_hackathons_for_user(target, offset=0, limit=5)
        return Response({"user": data})


class UserHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        offset, limit = parse_pagination(request)
        if offset is None:
            return Response({"detail": "Invalid pagination"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            target = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"hackathons": past_hackathons_for_user(target, offset=offset, limit=limit)})


class TeamLookupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        team_id = request.query_params.get("uuid")
        if not team_id:
            return Response({"detail": "uuid is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"detail": "Team not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "uuid": str(team.id),
            "name": team.name,
            "created_at": int(team.created_at.timestamp()),
            "best_placement": None,
            "past_hackathons": past_hackathons_for_team(team, offset=0, limit=5),
            "members": serialize_team_members(team, request.user),
        }

        best_entry = (
            HackathonTeam.objects.filter(team=team, placement__isnull=False)
            .select_related("hackathon")
            .order_by("placement", "-hackathon__end_date")
            .first()
        )
        if best_entry:
            h = best_entry.hackathon
            data["best_placement"] = {
                "uuid": str(h.id),
                "name": h.name,
                "description": h.description,
                "start_date": int(h.start_date.timestamp()),
                "end_date": int(h.end_date.timestamp()),
                "participants": h.participants_count,
                "placement": best_entry.placement,
            }
        return Response({"team": data})


class TeamHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, team_id):
        offset, limit = parse_pagination(request)
        if offset is None:
            return Response({"detail": "Invalid pagination"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"detail": "Team not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"hackathons": past_hackathons_for_team(team, offset=offset, limit=limit)})

