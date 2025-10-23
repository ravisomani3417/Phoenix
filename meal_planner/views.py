from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Student

# ---------- Home ----------
@login_required
def home(request):
    students = Student.objects.filter(teacher=request.user)
    avg_bmi = round(sum(s.bmi() for s in students if s.bmi()) / len(students), 2) if students else 0
    return render(request, 'home.html', {'students': students, 'avg_bmi': avg_bmi})

# ---------- Auth ----------
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        else:
            User.objects.create_user(username=username, password=password, email=email)
            messages.success(request, "Account created! Please log in.")
            return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# ---------- Students ----------
@login_required
def student_list(request):
    students = Student.objects.filter(teacher=request.user)
    return render(request, 'student_list.html', {'students': students})

@login_required
def add_student(request):
    if request.method == "POST":
        name = request.POST['name']
        student_id = request.POST['student_id']
        height = float(request.POST['height'])
        weight = float(request.POST['weight'])
        Student.objects.create(teacher=request.user, name=name, student_id=student_id,
                               height_cm=height, weight_kg=weight)
        return redirect('student_list')
    return render(request, 'add_student.html')

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk, teacher=request.user)
    return render(request, 'student_detail.html', {'student': student})
