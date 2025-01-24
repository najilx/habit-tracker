from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Progress, UserProfile, Badge
from django.utils import timezone
from django.contrib.auth.models import User

@receiver(post_save, sender=Progress)
def update_streak(sender, instance, **kwargs):
    """
    Update the user's streak when a Progress entry is saved.
    """
    habit = instance.habit
    user_profile = UserProfile.objects.get(user=habit.user)
    today = timezone.now().date()

    # Check if the habit was completed today
    if instance.completed:
        # If the last progress was yesterday, increment the streak
        last_progress = Progress.objects.filter(habit=habit, date__lt=today).order_by('-date').first()
        if last_progress and last_progress.completed:
            user_profile.streak += 1
        else:
            # Reset the streak if it wasn't completed yesterday
            user_profile.streak = 1
    else:
        # Reset the streak if the habit wasn't completed today
        user_profile.streak = 0

    user_profile.save()

    # Assign badges based on the streak
    assign_badges(user_profile)


def assign_badges(user_profile):
    """
    Assign badges to the user based on their streak.
    """
    if user_profile.streak >= 7:
        badge, created = Badge.objects.get_or_create(
            name="7-Day Streak",
            defaults={
                'description': "Completed a habit for 7 consecutive days.",
                'criteria': "7-day streak"
            }
        )
        user_profile.badges.add(badge)

    if user_profile.streak >= 30:
        badge, created = Badge.objects.get_or_create(
            name="30-Day Streak",
            defaults={
                'description': "Completed a habit for 30 consecutive days.",
                'criteria': "30-day streak"
            }
        )
        user_profile.badges.add(badge)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a UserProfile whenever a new User is created.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the UserProfile whenever the User is saved.
    """
    instance.profile.save()