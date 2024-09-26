from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer

def home(request):
    return HttpResponse("Welcome to the Django application!")

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Custom response format for GET
        response_data = [
            {
                'id': client['id'],
                'client_name': client['client_name'],
                'created_at': client['created_at'],
                'created_by': client['created_by']
            } for client in serializer.data
        ]
        
        return Response(response_data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()  # Save the instance

        # Custom response format for POST
        response_data = {
            'id': instance.id,
            'client_name': instance.client_name,
            'created_at': instance.created_at.isoformat(),  # Ensure correct date format
            'created_by': instance.created_by.username  # Get the username
        }
        
        return Response(response_data, status=201)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Custom response format for GET
        response_data = {
            'id': instance.id,
            'client_name': instance.client_name,
            'created_at': instance.created_at.isoformat(),  # Ensure correct date format
            'created_by': instance.created_by.username  # Get the username
        }
        
        return Response(response_data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()  # Save the updated instance

        # Custom response format for PUT
        response_data = {
            'id': updated_instance.id,
            'client_name': updated_instance.client_name,
            'created_at': updated_instance.created_at.isoformat(),  # Ensure correct date format
            'created_by': updated_instance.created_by.username  # Get the username
        }
        
        return Response(response_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        
        # Extract data from the request
        project_name = request.data.get('project_name')
        client_id = request.data.get('client_id')
        users = request.data.get('users')

        # Retrieve the client instance
        client = Client.objects.get(id=client_id)

        # Create the project instance
        project = Project.objects.create(
            project_name=project_name,
            client=client,
            created_by=request.user  # Set the logged-in user
        )

        # Assign users to the project
        project.users.set(users)  # Assuming 'users' is a ManyToManyField in your Project model
        project.save()

        # Custom response format for POST
        response_data = {
            'id': project.id,
            'project_name': project.project_name,
            'client': client.client_name,  # Assuming client has a 'client_name' field
            'users': [{'id': user.id, 'name': user.username} for user in project.users.all()],  # Assuming user has a 'username' field
            'created_at': project.created_at.isoformat(),  # Ensure correct date format
            'created_by': request.user.username  # Get the username of the creator
        }

        return Response(response_data, status=201)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(users=request.user)  # Filter projects by logged-in user
        response_data = []

        for project in queryset:
            response_data.append({
                'id': project.id,
                'project_name': project.project_name,
                'client_name': project.client.client_name,  # Assuming client has a 'client_name' field
                'created_at': project.created_at.isoformat(),  # Ensure correct date format
                'created_by': project.created_by.username  # Get the username of the creator
            })

        return Response(response_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)
