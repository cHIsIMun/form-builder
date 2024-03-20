from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Step, Field, Section, Submission
from .serializers import StepSerializer, StepStructureSerializer, SectionSerializer, FieldSerializer, SubmissionSerializer
from django.contrib.auth.models import Group
from .serializers import GroupSerializer

class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

class FormStructureView(APIView):
    def get(self, request, format=None):
        steps = Step.objects.all()
        serializer = StepStructureSerializer(steps, many=True)
        return Response(serializer.data)

class StepStructureView(APIView):
    def get(self, request, step_id, format=None):
        step = Step.objects.get(id=step_id)
        serializer = StepStructureSerializer(step)
        return Response(serializer.data)

class SectionStructureView(APIView):
    def get(self, request, section_id, format=None):
        section = Section.objects.get(id=section_id)
        serializer = SectionSerializer(section)
        return Response(serializer.data)

class FormSubmissionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SubmissionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StepSubmissionsView(APIView):
    def get(self, request, step_id, format=None):
        submissions = Submission.objects.filter(step_id=step_id)
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

class UserSubmissionsView(APIView):
    def get(self, request, user_id, format=None):
        submissions = Submission.objects.filter(user_id=user_id)
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

class StepUserSubmissionsView(APIView):
    def get(self, request, step_id, user_id, format=None):
        submissions = Submission.objects.filter(step_id=step_id, user_id=user_id)
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer