from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Skill, Interest, School, Major
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm as BaseUserChangeForm

# admin.site.register(User, UserAdmin)
class UserChangeForm(BaseUserChangeForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = "__all__"

class UserCreationForm(AdminUserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        # fields = ["email", "visibility"]
        fields = AdminUserCreationForm.Meta.fields + ("email", "visibility")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display  = ["email", "first_name", "last_name", "username", "visibility", "school", "grad_year", "date_joined"]

    # fields for when user is edited
    fieldsets = [
        (
            None, {"fields": ["email", "password", "visibility"]}
        ),
        (
            "Personal info", {"fields": [("first_name", "last_name"), "username"]}
        ),
        (
            "Education", {"fields": ["school","grad_year", "major"]}
        ),
        (
            "Profile info", {
                "classes": ["collapse","wide"],
                "fields": [
                    "bio", ("skills", "interests"),
                    "level", ("xp"), "blocked"
                ]
            }
        ),
        (
            "Meta data", {
                "classes": ["collapse"],
                "fields": ["is_superuser", "date_joined", ("updated_at","last_login")]
            }
        ),
    ]

    # fields for when user is created
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2", "visibility"],
            },
        ),
    ]

    list_filter   = ("is_superuser", "visibility", "school", "grad_year", "date_joined")
    search_fields = ("email", "school", "bio")
    autocomplete_fields = ("skills", "interests")  
    readonly_fields = ("date_joined", "updated_at", "last_login")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display  = ("name",)

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display  = ("name",)

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display  = ("name",)

@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display  = ("name",)

