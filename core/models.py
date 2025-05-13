from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.username

class Course(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Material(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"

class Test(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='tests')
    question = models.TextField()
    correct_answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test for {self.material.title}"

class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    answer = models.TextField()
    is_correct = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.test} by {self.student.username}"