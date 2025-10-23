from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    height_cm = models.FloatField()
    weight_kg = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def bmi(self):
        if self.height_cm > 0:
            return round(self.weight_kg / ((self.height_cm / 100) ** 2), 2)
        return None

    def bmi_status(self):
        bmi = self.bmi()
        if bmi is None:
            return "N/A"
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
