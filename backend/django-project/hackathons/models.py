import uuid
from django.db import models
from django.utils import timezone
from accounts.models import User


class Hackathon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return self.name

    @property
    def participants_count(self) -> int:
        """Count distinct users across teams for this hackathon."""
        return (
            User.objects.filter(teams__hackathon_entries__hackathon=self)
            .distinct()
            .count()
        )

    def is_past(self) -> bool:
        return self.end_date < timezone.now()


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, through="TeamMembership", related_name="teams")

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="team_memberships")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="memberships")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "team")

    def __str__(self):
        return f"{self.user} -> {self.team}"


class HackathonTeam(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name="hackathon_teams")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="hackathon_entries")
    placement = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("hackathon", "team")
        ordering = ["placement", "created_at"]

    def __str__(self):
        return f"{self.team} @ {self.hackathon}"

