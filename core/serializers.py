from rest_framework import serializers
from .models import CustomUser, Course, Material, Test, TestResult

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'

    def validate(self, data):
        if data['student'].role != 'student':
            raise serializers.ValidationError("Only students can submit test results.")
        return data