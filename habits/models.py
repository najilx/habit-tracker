from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Habit model
class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=100)
    goal = models.PositiveIntegerField(help_text="Daily target for the habit")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"



# Progress model
class Progress(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='progress')
    date = models.DateField(auto_now_add=True)
    count = models.PositiveIntegerField(default=0)  # Track progress count
    completed = models.BooleanField(default=False)  # Track completion status

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['habit', 'date'], name='unique_progress_per_habit_per_day')
        ]

    def __str__(self):
        return f"{self.habit.name} - {self.date} - {self.count}/{self.habit.goal}"


# Badge model
class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    criteria = models.CharField(max_length=100, help_text="Criteria for earning this badge")  # Fixed typo

    def __str__(self):
        return self.name


# User profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  # Fixed typo
    badges = models.ManyToManyField(Badge, blank=True)
    streak = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}'s profile"