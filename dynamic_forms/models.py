from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.db import models
import uuid
from django.conf import settings

# Modelo para os Steps
class Step(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    order = models.IntegerField(unique=True)  # Garante a ordem única para cada step

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

# Modelo para as Seções
class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=255)
    order = models.IntegerField()  # Ordem da seção dentro do step

    class Meta:
        unique_together = ('step', 'order')  # Garante ordem única dentro de cada step
        ordering = ['order']
    
    def __str__(self):
        return self.name

# Modelo para os Campos
class Field(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='fields')
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    autocomplete_options = models.JSONField(blank=True, null=True)
    order = models.IntegerField()  # Ordem do campo dentro da seção

    class Meta:
        unique_together = ('section', 'order')
        ordering = ['order']
    
    def __str__(self):
        return self.name

class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')  # Associando submissão ao usuário
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.step.name} - {self.user.username}'

class Answer(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.submission} - {self.field}'

class AnswerText(Answer):
    submission = models.ForeignKey(Submission, related_name='answer_texts', on_delete=models.CASCADE)
    value = models.TextField()

class AnswerNumber(Answer):
    submission = models.ForeignKey(Submission, related_name='answer_numbers', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)

class AnswerBoolean(Answer):
    submission = models.ForeignKey(Submission, related_name='answer_booleans', on_delete=models.CASCADE)
    value = models.BooleanField()

class AnswerDate(Answer):
    submission = models.ForeignKey(Submission, related_name='answer_dates', on_delete=models.CASCADE)
    value = models.DateField()

class AnswerFile(Answer):
    submission = models.ForeignKey(Submission, related_name='answer_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email