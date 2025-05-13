from django.urls import path
from .views import CourseListCreate, MaterialListCreate, TestListCreate, TestResultListCreate, TestResultList

urlpatterns = [
    path('courses/', CourseListCreate.as_view(), name='course-list'),
    path('materials/', MaterialListCreate.as_view(), name='material-list'),
    path('tests/', TestListCreate.as_view(), name='test-list'),
    path('test-results/', TestResultListCreate.as_view(), name='test-result-create'),
    path('my-results/', TestResultList.as_view(), name='test-result-list'),
]