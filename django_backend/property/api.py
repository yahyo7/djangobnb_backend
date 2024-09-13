from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

from .forms import PropertyForm
from .models import Property
from .serializers import PropertiesListSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    properties = Property.objects.all()
    serializer = PropertiesListSerializer(properties, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_property(request):
    form = PropertyForm(request.data, request.FILES)  # use request.data for POST data
    if form.is_valid():
        property = form.save(commit=False)
        property.landlord = request.user  # assuming you're using authentication
        property.save()
        return JsonResponse({
            'success': True,
            'message': 'Property created successfully',
        }, status=201)
    
    return JsonResponse({
        'success': False,
        'errors': form.errors.as_json()
    }, status=400)