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
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Hub, Machine
from .serializers import HubSerializer, MachineSerializer, UserSerializer
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


class HubListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = HubSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Hub.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class HubRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HubSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Hub.objects.filter(owner=self.request.user)

# class HubListCreateAPIView(generics.ListCreateAPIView):
#     serializer_class = HubSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Hub.objects.filter(owner=self.request.user)

#     def perform_create(self, serializer):
#         service_provider = self.request.user
#         if service_provider.user_type == 'technician':
#             serializer.save(owner=self.request.user)
#         else:
#             return Response({"error": "Only technicians can create hubs"}, status=status.HTTP_403_FORBIDDEN)

class HubRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HubSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Hub.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.instance
        service_provider = self.request.user
        if service_provider.user_type == 'technician':
            serializer.save()
        else:
            return Response({"error": "Only technicians can update hubs"}, status=status.HTTP_403_FORBIDDEN)

class MachineListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MachineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        hub_id = self.kwargs.get('pk')  # Get the hub ID from URL parameter
        return Machine.objects.filter(hub_id=hub_id)

    def perform_create(self, serializer):
        # Retrieve hubs owned by the authenticated user
        user_hubs = Hub.objects.filter(owner=self.request.user)
        
        if user_hubs.exists():
            # Select the first hub owned by the user
            hub = user_hubs.first()
            
            # Print the hub id before saving
            print(serializer.validated_data.get('hub').id)
            
            # Retrieve the hub instance based on the provided ID
            hub_id = serializer.validated_data.get('hub').id
            hub_instance = Hub.objects.get(pk=hub_id)
            
            serializer.save(hub=hub_instance)
        else:
            # Handle the case where the user doesn't own any hubs
            raise serializers.ValidationError("User does not own any hubs.")



def machineview(request, hub_id):
    try:
        # Retrieve machines whose hub ID matches the one provided in the URL
        machines = Machine.objects.filter(hub_id=hub_id)
        
        # Serialize the queryset to JSON
        machine_data = list(machines.values())

        return JsonResponse(machine_data, safe=False)
    
    except Exception as e:
        # Handle any errors
        return JsonResponse({'error': str(e)}, status=500)

class MachineRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MachineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Machine.objects.filter(user=self.request.user)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def abc(request):
#    permission_classes = [IsAuthenticated]
#    authentication_classes = [TokenAuthentication]

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
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"status": True, "message": "Login Successfully !", "token": str(token), "user_id": user.id},
                status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": False, "message": "Invalid username or password"},
                status.HTTP_401_UNAUTHORIZED,
            )

    def get(self, request):
        if request.user.is_authenticated:
            return Response(
                {"user_id": request.user.id},
                status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "User not authenticated"},
                status.HTTP_401_UNAUTHORIZED,
            )


class registerapi(generics.GenericAPIView):
    def post(self, request):
        data = request.data
        print(data)
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
            print("user =",request.user)
            # print(request.headers)
            # Get the token associated with the user
            token = Token.objects.get(user=request.user)
            # Delete the token
            token.delete()
            return Response({"success": "Logout successful."})
        except Token.DoesNotExist:
            return Response({"error": "User is not logged in."}, status=400)
        

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def listalltechnicians(request):
    if request.method == 'GET':
        # Filter users by group name 'technician'
        technicians = User.objects.filter(groups__name='technician')
        
        # Serialize the queryset
        serializer = UserSerializer(technicians, many=True)
        
        # Return the serialized data
        return Response(serializer.data)




@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_investment(request):
    if request.method == 'POST':
        investment_amount = request.data.get('investment_amount')
        number_of_months = request.data.get('number_of_months')

        try:
            investment_amount = float(investment_amount)
            number_of_months = int(number_of_months)
            result = investment_amount * number_of_months + 2
            return Response({"result": result}, status=status.HTTP_200_OK)
        except (ValueError, TypeError):
            return Response({"error": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)


