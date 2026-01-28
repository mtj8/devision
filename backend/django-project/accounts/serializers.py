from .models import User, Skill, Interest, School, Major
from rest_framework import serializers
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError as DjangoValidationError


def ts_to_dt(value):
    """Convert unix timestamp (seconds) -> datetime"""
    if value is None:
        return None
    try:
        return timezone.datetime.fromtimestamp(int(value), tz=timezone.utc)
    except Exception:
        raise serializers.ValidationError("Invalid unix timestamp")


def dt_to_ts(dt):
    """Convert datetime -> unix timestamp"""
    if not dt:
        return None
    return int(dt.timestamp())


class CustomUserSerializer(serializers.BaseSerializer):

    # ---------------------------
    # Helper for required checks
    # ---------------------------
    def get_field(self, data, name, required=False):
        """
        Returns:
            - serializers.empty  -> field missing entirely (PATCH)
            - value               -> provided value
        Enforces 'required' only on POST.
        """
        method = self.context["request"].method
        value = data.get(name, serializers.empty)

        if required and method == "POST" and value is serializers.empty:
            raise serializers.ValidationError({name: "This field is required"})

        return value

    # ---------------------------
    #   INPUT → PYTHON
    # ---------------------------
    def to_internal_value(self, data):

        errors = {}
        url_validator = URLValidator()
        method = self.context["request"].method

        # ---------------------------
        # Required on POST only
        # ---------------------------
        email = self.get_field(data, "email", required=True)
        username = self.get_field(data, "username", required=True)
        visibility = self.get_field(data, "visibility", required=True)

        # ---------------------------
        # OPTIONAL FIELDS (PATCH-safe)
        # ---------------------------
        first = self.get_field(data, "first_name")
        last = self.get_field(data, "last_name")
        password = self.get_field(data, "password", required=True)
        xp = self.get_field(data, "xp")
        level = self.get_field(data, "level")
        school_id = self.get_field(data, "school")
        grad_year = self.get_field(data, "grad_year")
        major_id = self.get_field(data, "major")

        discord = self.get_field(data, "discord")
        instagram = self.get_field(data, "instagram")
        github = self.get_field(data, "github")
        linkedin = self.get_field(data, "linkedin")

        bio = self.get_field(data, "bio")
        skills = self.get_field(data, "skills")
        interests = self.get_field(data, "interests")
        blocked = self.get_field(data, "blocked")
        personal = self.get_field(data, "personal")
        xp_needed = self.get_field(data, "xp_needed")
        profile_gradient = self.get_field(data, "profile_gradient")

        # ---------------------------
        # FIELD VALIDATION
        # ---------------------------

        # Email validation (if provided)
        if email is not serializers.empty:
            if not isinstance(email, str):
                errors["email"] = "Must be a string."
            elif not email.endswith(".edu"):
                errors["email"] = "Must be a valid .edu email"

        if password is not serializers.empty and (not isinstance(password, str) or len(password) < 6):
            errors["password"] = "Password must be at least 6 characters."

        # Visibility normalization
        if visibility is not serializers.empty:
            if visibility not in ["public", "private"]:
                errors["visibility"] = "Must be 'public' or 'private'"

        # Int parsing helper
        def parse_int(name, value, minv=None, maxv=None):
            if value is serializers.empty:
                return serializers.empty
            try:
                iv = int(value)
            except (TypeError, ValueError):
                errors[name] = "Must be an integer."
                return None
            if minv is not None and iv < minv:
                errors[name] = f"Must be >= {minv}"
            if maxv is not None and iv > maxv:
                errors[name] = f"Must be <= {maxv}"
            return iv

        xp = parse_int("xp", xp, minv=0)
        level = parse_int("level", level, minv=0, maxv=500)
        grad_year = parse_int("grad_year", grad_year, minv=2015, maxv=2080)

        # FK validation (PATCH safe)
        def validate_fk(name, model, pk):
            if pk is serializers.empty:
                return serializers.empty
            try:
                pk_int = int(pk)
            except:
                errors[name] = "Must be an integer ID."
                return None
            if not model.objects.filter(pk=pk_int).exists():
                errors[name] = f"{model.__name__} does not exist."
            return pk_int

        school_id = validate_fk("school", School, school_id)
        major_id = validate_fk("major", Major, major_id)

        # URL validation
        def validate_url(name, value):
            if value is serializers.empty:
                return serializers.empty
            if value is None or value == "":
                return value
            try:
                url_validator(value)
            except DjangoValidationError:
                errors[name] = "Enter a valid URL."
            return value

        discord = validate_url("discord", discord)
        instagram = validate_url("instagram", instagram)
        github = validate_url("github", github)
        linkedin = validate_url("linkedin", linkedin)
        personal = validate_url("personal", personal)

        # M2M validation
        def validate_m2m(name, value, model):
            if value is serializers.empty:
                return serializers.empty
            if not isinstance(value, list):
                errors[name] = "Must be a list of IDs."
                return []
            bad = [pk for pk in value if not model.objects.filter(pk=pk).exists()]
            if bad:
                errors[name] = f"Invalid IDs: {bad}"
            return value

        skills = validate_m2m("skills", skills, Skill)
        interests = validate_m2m("interests", interests, Interest)

        # Blocked validation
        if blocked is not serializers.empty and not isinstance(blocked, list):
            errors["blocked"] = "Must be a list."

        if profile_gradient not in (serializers.empty, None):
            if not isinstance(profile_gradient, (list, tuple)) or len(profile_gradient) != 2:
                errors["profile_gradient"] = "Must be two hex strings."
            else:
                profile_gradient = [str(part) for part in profile_gradient]

        if errors:
            raise serializers.ValidationError(errors)

        # ---------------------------
        # BUILD validated_data
        # (keep serializers.empty so update() knows what to ignore)
        # ---------------------------

        return {
            "email": email,
            "username": username,
            "first_name": first,
            "last_name": last,
            "visibility": visibility,
            "password": password,
            "xp": xp,
            "level": level,
            "school_id": school_id,
            "grad_year": grad_year,
            "major_id": major_id,
            "discord": discord,
            "instagram": instagram,
            "github": github,
            "linkedin": linkedin,
            "bio": bio,
            "skills": skills,
            "interests": interests,
            "blocked": blocked,
            "personal": personal,
            "xp_needed": xp_needed,
            "profile_gradient": profile_gradient,
        }

    # ---------------------------
    # PYTHON → OUTPUT
    # ---------------------------
    def to_representation(self, instance: User):
        return {
            "id": str(instance.id),
            "email": instance.email,
            "username": instance.username,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "visibility": instance.visibility,
            "xp": instance.xp,
            "level": instance.level,
            "school": instance.school.id if instance.school else None,
            "school_name": instance.school.name if instance.school else None,
            "grad_year": instance.grad_year,
            "major": instance.major.id if instance.major else None,
            "major_name": instance.major.name if instance.major else None,
            "discord": instance.discord,
            "instagram": instance.instagram,
            "github": instance.github,
            "linkedin": instance.linkedin,
            "bio": instance.bio,
            "skills": [s.id for s in instance.skills.all()],
            "skill_names": [s.name for s in instance.skills.all()],
            "interests": [i.id for i in instance.interests.all()],
            "interest_names": [i.name for i in instance.interests.all()],
            "blocked": instance.blocked,
            "date_joined": dt_to_ts(instance.date_joined),
            "personal": instance.personal,
            "xp_needed": instance.xp_needed,
            "profile_gradient": instance.profile_gradient,
        }

    # ---------------------------
    # CREATE
    # ---------------------------
    def create(self, validated_data):
        skill_ids = validated_data.pop("skills", serializers.empty)
        interest_ids = validated_data.pop("interests", serializers.empty)
        school_id = validated_data.pop("school_id", serializers.empty)
        major_id = validated_data.pop("major_id", serializers.empty)
        password = validated_data.pop("password", None)

        if school_id is not serializers.empty:
            validated_data["school"] = School.objects.get(pk=school_id)
        if major_id is not serializers.empty:
            validated_data["major"] = Major.objects.get(pk=major_id)

        user = User.objects.create(**validated_data)
        if password not in (None, serializers.empty):
            user.set_password(password)
            user.save(update_fields=["password"])

        if skill_ids not in (serializers.empty, None):
            user.skills.set(skill_ids)
        if interest_ids not in (serializers.empty, None):
            user.interests.set(interest_ids)

        return user

    # ---------------------------
    # UPDATE (PATCH SAFE)
    # ---------------------------
    def update(self, instance: User, validated_data):

        skills = validated_data.pop("skills", serializers.empty)
        interests = validated_data.pop("interests", serializers.empty)
        school_id = validated_data.pop("school_id", serializers.empty)
        major_id = validated_data.pop("major_id", serializers.empty)
        profile_gradient = validated_data.pop("profile_gradient", serializers.empty)
        password = validated_data.pop("password", serializers.empty)

        for attr, value in validated_data.items():
            if value is not serializers.empty:
                setattr(instance, attr, value)

        if school_id is not serializers.empty:
            instance.school = School.objects.get(pk=school_id) if school_id else None

        if major_id is not serializers.empty:
            instance.major = Major.objects.get(pk=major_id) if major_id else None

        instance.save()

        if skills is not serializers.empty:
            instance.skills.set(skills)

        if interests is not serializers.empty:
            instance.interests.set(interests)

        if profile_gradient is not serializers.empty:
            instance.profile_gradient = profile_gradient
            instance.save(update_fields=["profile_gradient"])

        if password is not serializers.empty:
            instance.set_password(password)
            instance.save(update_fields=["password"])

        return instance

