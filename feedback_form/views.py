from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from feedback_form.forms import FeedbackForm
from rest_framework.decorators import api_view, permission_classes

from feedback_form.serializers import FeedbackSerializer


# Create your views here.

def validate_form(form: FeedbackForm):
    if not form.is_valid():
        raise ValueError(form.errors)
    phone = form.cleaned_data['phone']
    if phone[0] != '+':
        raise ValueError('Phone number must start with "+"')
    phone = phone.strip().lstrip('+')
    try:
        int(phone)
    except ValueError:
        raise ValueError('Phone number must contain only digits and start with "+"')
    if len(phone) < 11:
        raise ValueError('Phone number must contain at least 11 digits')
    if len(phone) > 13:
        raise ValueError('Phone number must contain at most 13 digits')
    if not form.is_valid():
        raise ValueError(form.errors)
    feedback = form.save(commit=False)
    feedback.phone = phone
    return feedback


def create_feedback_util(data):
    form = FeedbackForm(data)
    validate_form(form)
    feedback = form.save()
    return feedback


@permission_classes([IsAuthenticated])
@swagger_auto_schema(method='post', request_body=FeedbackSerializer)
@api_view(['POST'])
def create_feedback(request):
    try:
        new_feedback = create_feedback_util(request.data)
        serializer = FeedbackSerializer(new_feedback)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
