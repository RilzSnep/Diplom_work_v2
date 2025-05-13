from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import CustomUser, Course, Material, Test, TestResult
from core.serializers import TestResultSerializer
from rest_framework_simplejwt.tokens import AccessToken

class SelfLearningTests(TestCase):
    def setUp(self):
        # Создаем пользователей с разными ролями
        self.admin = CustomUser.objects.create_superuser(
            username='admin', password='admin123', role='admin'
        )
        self.teacher = CustomUser.objects.create_user(
            username='teacher', password='teacher123', role='teacher'
        )
        self.student = CustomUser.objects.create_user(
            username='student', password='student123', role='student'
        )

        # Настройка API-клиента
        self.client = APIClient()

        # Получаем JWT-токены для каждого пользователя
        self.teacher_token = AccessToken.for_user(self.teacher)
        self.student_token = AccessToken.for_user(self.student)

        # Создаем тестовые данные
        self.course = Course.objects.create(title='Test Course', owner=self.teacher)
        self.material = Material.objects.create(
            course=self.course, title='Test Material', content='Sample content'
        )
        self.test = Test.objects.create(
            material=self.material, question='What is 2+2?', correct_answer='4'
        )

    def test_create_course_as_teacher(self):
        # Тестируем создание курса преподавателем
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.teacher_token}')
        response = self.client.post(
            reverse('course-list'),
            {'title': 'New Course', 'owner': self.teacher.id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_create_course_as_student_fails(self):
        # Студент не должен создавать курс
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        response = self.client.post(
            reverse('course-list'),
            {'title': 'Invalid Course', 'owner': self.student.id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_submit_test_result_as_student(self):
        # Студент отправляет результат теста
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        response = self.client.post(
            reverse('test-result-create'),
            {'test': self.test.id, 'answer': '4'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result = TestResult.objects.get(student=self.student, test=self.test)
        self.assertTrue(result.is_correct)

    def test_submit_test_result_as_teacher_fails(self):
        # Преподаватель не должен отправлять результат теста
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.teacher_token}')
        response = self.client.post(
            reverse('test-result-create'),
            {'test': self.test.id, 'answer': '4'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_test_results_as_student(self):
        # Студент видит только свои результаты
        TestResult.objects.create(test=self.test, student=self.student, answer='4', is_correct=True)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        response = self.client.get(reverse('test-result-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_access_test_results_as_teacher(self):
        # Преподаватель видит результаты по своим курсам
        TestResult.objects.create(test=self.test, student=self.student, answer='4', is_correct=True)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.teacher_token}')
        response = self.client.get(reverse('test-result-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_model_str_methods(self):
        # Проверка строкового представления моделей
        self.assertEqual(str(self.course), 'Test Course')
        self.assertEqual(str(self.material), 'Test Material (Test Course)')
        self.assertEqual(str(self.test), 'Test for Test Material')
        self.assertEqual(str(self.student), 'student')

    def test_test_result_validation(self):
        # Проверка валидации сериализатора
        serializer = TestResultSerializer(data={
            'test': self.test.id,
            'student': self.teacher.id,
            'answer': '4'
        })
        self.assertFalse(serializer.is_valid())
        # Ошибка находится в 'student', а не в 'non_field_errors'
        self.assertIn("Only students can submit test results.", str(serializer.errors['student']))