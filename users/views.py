from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer, UserSerializer, LoginSerializer
from .services import UserService
from rest_framework.permissions import AllowAny


class UserSignupView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():

            try:
                service = UserService()

                created_user = service.signup(
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password'],
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name']
                )

                if created_user:
                    serialized_user = UserSerializer(created_user).data

                    return Response({'data': serialized_user, 'message': 'user created successfully'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "User creation failed"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                service = UserService()
                login_response = service.login(
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password'],
                    is_remembered=serializer.validated_data.get(
                        'is_remembered', False)
                )

                reponse = {
                    'refresh': login_response['refresh'],
                    'access': login_response['access'],
                    'user': UserSerializer(login_response['user']).data

                }

                return Response({'data': reponse, 'message': 'Login successful'}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
