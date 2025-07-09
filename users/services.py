from .dtos import UserDTO
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta


class UserService:

    def signup(self, email, password, first_name, last_name):

        if not email or not password or not first_name or not last_name:
            raise ValueError("All fields are required")

        # check if email already exists
        if AuthUser.objects.filter(email=email).exists():
            raise ValueError("Email already exists")

        # save user to database
        user = AuthUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.save()

        # return user dto
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )

    def login(self, email, password, is_remembered=False):
        if not email or not password:
            raise ValueError("Email and password are required")

        user = authenticate(username=email, password=password)
        if user is None:
            raise ValueError("Invalid credentials")

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        if is_remembered:
            refresh_token.set_exp(lifetime=timedelta(days=60))
            access_token.set_exp(lifetime=timedelta(days=30))
        else:
            refresh_token.set_exp(lifetime=timedelta(days=10))
            access_token.set_exp(lifetime=timedelta(hours=8))

        return {
            'refresh': str(refresh_token),
            'access': str(access_token),
            'user': UserDTO(
                id=user.id,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name
            )
        }
