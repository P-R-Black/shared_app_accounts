import pytest
from django.test import TestCase
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from .conftest import create_seed_data


User = get_user_model()

class TestActiveUserManager(TestCase):
    """Tests for ActiveUserManager (filters out deleted users)"""

    def setUp(cls):
        """Create test users"""
        cls.product, cls.color_spec, cls.size_spec, cls.user1, cls.profile_one, cls.user2, cls.profile_two = create_seed_data()

        # Deleted user
        cls.deleted_user = User.all_objects.create(
            email="deleted@example.com",
            first_name="Deleted",
            last_name="User",
            deleted_at=now()
        )

    def test_get_queryset_excludes_deleted_users(self):
        """Test that default manager excludes soft-deleted users"""
        users = User.objects.all()

        self.assertEqual(users.count(), 2)
        self.assertIn(self.user1, users)
        self.assertNotIn(self.deleted_user, users)

    def test_filter_on_active_users_only(self):
        """Test filtering works on non-deleted users"""
        users = User.objects.filter(first_name="One")

        self.assertEqual(users.count(), 1)
        self.assertEqual(users.first(), self.user1)

    def test_get_on_deleted_user_raises_does_not_exist(self):
        """Test that getting a deleted user raises DoesNotExist"""
        from django.core.exceptions import ObjectDoesNotExist

        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(email="deleted@example.com")

    def test_count_excludes_deleted_users(self):
        """Test that count() excludes deleted users"""
        self.assertEqual(User.objects.count(), 2)