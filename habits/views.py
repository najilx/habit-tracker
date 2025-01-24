from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Habit, Progress, UserProfile
from .forms import HabitForm, ProgressForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserProfileSerializer

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def index(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'index.html', {'habits': habits})


@login_required
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('index')
    else:
        form = HabitForm()
    return render(request, 'add_habit.html', {'form': form})


@login_required
def mark_progress(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    today = timezone.now().date()

    # Check if a Progress entry already exists for today
    progress, created = Progress.objects.get_or_create(habit=habit, date=today)

    if request.method == 'POST':
        form = ProgressForm(request.POST, instance=progress)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProgressForm(instance=progress)

    return render(request, 'mark_progress.html', {'form': form, 'habit': habit})


@login_required
def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == 'POST':
        habit.delete()
        return redirect('index')
    return render(request, 'delete_habit.html', {'habit': habit})


@login_required
def edit_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'edit_habit.html', {'form': form, 'habit': habit})


class LeaderboardView(APIView):
    def get(self, request):
        # Fetch users ordered by streak (descending)
        leaderboard = UserProfile.objects.all().order_by('-streak')
        serializer = UserProfileSerializer(leaderboard, many=True)
        return Response(serializer.data)