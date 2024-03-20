from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (StepViewSet, SectionViewSet, FieldViewSet, FormStructureView, StepStructureView, SectionStructureView, FormSubmissionView, StepSubmissionsView, UserSubmissionsView, StepUserSubmissionsView)

# Configuração do router para os viewsets
router = DefaultRouter()
router.register(r'steps', StepViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'fields', FieldViewSet)

urlpatterns = [
    # Inclui as URLs definidas pelo router
    path('', include(router.urls)),
    
    # URL para obter a estrutura completa de formulário (Steps/Sections/Fields) ordenados
    path('form-structure/', FormStructureView.as_view(), name='form-structure'),
    
    # URL para obter a estrutura de um Step específico (com suas Sections/Fields)
    path('steps/<uuid:step_id>/structure/', StepStructureView.as_view(), name='step-structure-specific'),
    
    # URL para obter a estrutura de uma Section específica (com seus Fields)
    path('sections/<uuid:section_id>/structure/', SectionStructureView.as_view(), name='section-structure-specific'),
    
    # URL para submissão de formulários
    path('submissions/', FormSubmissionView.as_view(), name='form-submissions'),
    
    # URLs para obter submissões
    path('steps/<uuid:step_id>/submissions/', StepSubmissionsView.as_view(), name='step-submissions'),
    path('users/<uuid:user_id>/submissions/', UserSubmissionsView.as_view(), name='user-submissions'),
    path('steps/<uuid:step_id>/users/<uuid:user_id>/submissions/', StepUserSubmissionsView.as_view(), name='step-user-submissions'),
]
