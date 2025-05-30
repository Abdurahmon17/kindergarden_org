import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_create_user_with_default_role():
    user = User.objects.create_user(username="testuser1", password="pass1234")
    assert user.role == "Chef"  # Default value

@pytest.mark.django_db
def test_create_user_with_custom_role():
    user = User.objects.create_user(username="manager1", password="pass1234", role="Manager")
    assert user.role == "Manager"

@pytest.mark.django_db
def test_user_str_method():
    user = User.objects.create_user(username="oshpaz1", password="pass1234")
    assert str(user) == "oshpaz1"