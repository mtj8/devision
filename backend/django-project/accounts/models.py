from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Helper tables
class Skill(models.Model): # optional skills for the user
    name = models.CharField(max_length=25, unique=True, db_index=True)
    def __str__(self): 
        return f"{self.name}"

class Interest(models.Model): # optional interests for the user
    name = models.CharField(max_length=25, unique=True, db_index=True)
    def __str__(self): 
        return f"{self.name}"

class School(models.Model): # school user goes to
    name = models.CharField(max_length=100, unique=True, db_index=True)
    def __str__(self):
        return self.name

class Major(models.Model): # majors
    name = models.CharField(max_length=25, unique=True, db_index=True)
    def __str__(self):
        return self.name

# Main tables
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # use email for login
    email = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # Extra Fields
    first_name = models.CharField(max_length=35, blank=True)
    last_name = models.CharField(max_length=35, blank=True)

    VISIBILITY_CHOICES = [ # Can add more later if needed
            ("public", "Public"),
            ("private", "Private"),
    ]

    visibility = models.CharField(
            max_length=10,choices=VISIBILITY_CHOICES,default="public",db_index=True
    )

    # Expereince/Levels
    xp = models.PositiveIntegerField(default=0)
    xp_needed = models.PositiveIntegerField(default=0)
    level = models.PositiveSmallIntegerField(default=1,
        validators=[MaxValueValidator(500)]
    )

    # Optional
    school = models.ForeignKey(School, 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name="users"
    )
    grad_year = models.PositiveSmallIntegerField(null=True, blank=True, 
        validators=[MinValueValidator(2015), MaxValueValidator(2080)],
        db_index=True,
        help_text="4-digit grad year (e.g. 2028)"
    )
    # major = models.CharField(max_length=50, blank=True)
    major = models.ForeignKey(Major,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="users"
    )

    # Socials
    discord = models.URLField(max_length=200, null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)
    linkedin = models.URLField(max_length=200, null=True, blank=True)
    personal = models.URLField(max_length=200, null=True, blank=True)

    #Information
    bio = models.TextField(null=True, blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name="users")
    interests  = models.ManyToManyField(Interest,  blank=True, related_name="users")
    blocked = models.JSONField(blank=True,default=list)
    profile_gradient = models.JSONField(blank=True, default=list)

    # Extra info
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_joined"] # newest to oldest

    def __str__(self): #how this table is visualized as plain text
        return f"{self.email}"

    objects = UserManager()


class Friendship(models.Model):
    user = models.ForeignKey(User, related_name="friendships", on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name="reverse_friendships", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "friend")

    def __str__(self):
        return f"{self.user} -> {self.friend}"
    
