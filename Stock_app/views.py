from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics, pagination
from .serializers import registerser, loginser
from rest_framework.response import Response
from rest_framework import status, serializers
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def abc(request):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    a = {
        'Stock_name': 'Nifty 50',
        'Price': '21873.23'
    }
    return Response(a)


class loginapi(APIView):
    permission_classes = []

    def post(self, request):
        data = request.data
        serializers = loginser(data=data)
        if not serializers.is_valid():
            return Response(
                {"status": False, "message": serializers.errors},
                status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(
            username=serializers.data["username"], password=serializers.data["password"]
        )
        print(serializers.data["username"])
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"status": True, "message": "Login Successfully !", "token": str(token)},
            status.HTTP_200_OK,
        )

    def get(self, request):
        content = {"user ": str(request.user), "auth ": str(request.auth)}


class registerapi(generics.GenericAPIView):
    def post(self, request):
        data = request.data
        serializers = registerser(data=data)

        if serializers.is_valid():
            serializers.save()
            return Response(
                {"message": "User Created Successfully !"}, status.HTTP_201_CREATED
            )
        return Response(
            {"status": False, "message": serializers.errors},
            status.HTTP_400_BAD_REQUEST,
        )
    
class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the token associated with the user
            token = Token.objects.get(user=request.user)
            # Delete the token
            token.delete()
            return Response({"success": "Logout successful."})
        except Token.DoesNotExist:
            return Response({"error": "User is not logged in."}, status=400)
