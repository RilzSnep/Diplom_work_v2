from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Course, Material, Test, TestResult
from .serializers import CourseSerializer, MaterialSerializer, TestSerializer, TestResultSerializer

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

class CourseListCreate(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

class MaterialListCreate(generics.ListCreateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

class TestListCreate(generics.ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

class TestResultListCreate(generics.ListCreateAPIView):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsStudent]

    def perform_create(self, serializer):
        test = serializer.validated_data['test']
        is_correct = serializer.validated_data['answer'].strip().lower() == test.correct_answer.strip().lower()
        serializer.save(student=self.request.user, is_correct=is_correct)

class TestResultList(generics.ListAPIView):
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'student':
            return TestResult.objects.filter(student=self.request.user)
        elif self.request.user.role == 'teacher':
            return TestResult.objects.filter(test__material__course__owner=self.request.user)
        return TestResult.objects.none()