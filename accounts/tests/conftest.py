from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def create_seed_data():

    user1 = User.objects.create_user(
        email="user1@example.com", password="passWord!1", first_name="One", middle_name="M", last_name="User", is_active=True
    )

    user2 = User.objects.create_user(
        email="user2@example.com", password="passWord@2", first_name="Two",middle_name="T", last_name="User", is_active=True
    )

    return user1,user2


d