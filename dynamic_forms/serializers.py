from rest_framework import serializers
from django.db import transaction
from django.db.models import Max
from django.contrib.auth.models import Group
from .models import Step, Section, Field, Submission, AnswerText, AnswerNumber, AnswerDate, AnswerFile, AnswerBoolean

from django.contrib.auth import get_user_model
User = get_user_model()

class AnswerTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerText
        fields = ['field', 'value']

class AnswerNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerNumber
        fields = ['field', 'value']

class AnswerBooleanSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerBoolean
        fields = ['field', 'value']

class AnswerDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerDate
        fields = ['field', 'value']

class AnswerFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerFile
        fields = ['field', 'file']

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'name', 'order']
        read_only_fields = ['order']

    def create(self, validated_data):
        last_order = Step.objects.aggregate(Max('order'))['order__max']
        validated_data['order'] = (last_order or 0) + 1
        return super().create(validated_data)

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['id', 'section', 'name', 'content_type', 'autocomplete_options', 'order']
        read_only_fields = ['order']

    def create(self, validated_data):
        last_order = Field.objects.filter(section=validated_data['section']).aggregate(Max('order'))['order__max']
        validated_data['order'] = (last_order or 0) + 1
        return super().create(validated_data)

class SectionSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'step', 'name', 'order', 'fields']
        read_only_fields = ['order']

    def create(self, validated_data):
        last_order = Section.objects.filter(step=validated_data['step']).aggregate(Max('order'))['order__max']
        validated_data['order'] = (last_order or 0) + 1
        return super().create(validated_data)

class StepStructureSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Step
        fields = ['id', 'name', 'order', 'sections']

class SubmissionSerializer(serializers.ModelSerializer):
    answers = serializers.JSONField(write_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'step', 'submitted_at', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers', None)
        if answers_data is None:
            raise serializers.ValidationError("O campo 'answers' é obrigatório.")
        
        with transaction.atomic():
            user = self.context['request'].user
            submission = Submission.objects.create(step=validated_data['step'], user=user)

            for answer in answers_data:
                field_id = answer.get('field_id')
                answer_type = answer.get('type')
                value = answer.get('value')

                field = Field.objects.get(id=field_id)

                if answer_type == 'text':
                    AnswerText.objects.create(submission=submission, field=field, value=value)
                elif answer_type == 'number':
                    AnswerNumber.objects.create(submission=submission, field=field, value=value)
                elif answer_type == 'boolean':
                    AnswerBoolean.objects.create(submission=submission, field=field, value=value)
                elif answer_type == 'date':
                    AnswerDate.objects.create(submission=submission, field=field, value=value)
                elif answer_type == 'file':
                    AnswerFile.objects.create(submission=submission, field=field, file=value)
                else:
                    raise serializers.ValidationError(f"Tipo de resposta não suportado: {answer_type}")

        return submission
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['answers'] = {
            'text': AnswerTextSerializer(instance.answer_texts.all(), many=True).data,
            'number': AnswerNumberSerializer(instance.answer_numbers.all(), many=True).data,
            'boolean': AnswerBooleanSerializer(instance.answer_booleans.all(), many=True).data,
            'date': AnswerDateSerializer(instance.answer_dates.all(), many=True).data,
            'file': AnswerFileSerializer(instance.answer_files.all(), many=True).data
        }
        return representation

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'