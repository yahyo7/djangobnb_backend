from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

from .forms import PropertyForm
from .models import Property, Reservation
from .serializers import PropertiesListSerializer, PropertiesDetailSerializer, ReservationSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    properties = Property.objects.all()
    
    # filter properties
    landlord_id = request.GET.get('landlord_id', None)
    if landlord_id:
        properties = properties.filter(landlord__id=landlord_id)
    serializer = PropertiesListSerializer(properties, many=True)
    return JsonResponse({
        'data': serializer.data
    })
    
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_detail(request, pk):
    property = Property.objects.get(pk=pk)
    serializer = PropertiesDetailSerializer(property, many=False)
    return JsonResponse(serializer.data)

@api_view(['POST', 'FILES'])
def create_property(request):
    form = PropertyForm(request.POST, request.FILES)

    if form.is_valid():
        property = form.save(commit=False)
        property.landlord = request.user
        property.save()

        return JsonResponse({'success': True})
    else:
        print('error', form.errors, form.non_field_errors)
        return JsonResponse({'errors': form.errors.as_json()}, status=400)
    
@api_view(['POST'])
def book_property(request, pk):
    try: 
        check_in = request.POST.get('check_in', '')
        check_out = request.POST.get('check_out', '')
        number_of_nights = request.POST.get('number_of_nights', '')
        total_price = request.POST.get('total_price', '')
        guests = request.POST.get('guests', '')
        
        property = Property.objects.get(pk=pk)
        
        reservation = Reservation.objects.create(
            property=property,
            check_in=check_in,
            check_out=check_out,
            number_of_nights=number_of_nights,
            total_price=total_price,
            guests=guests,
            created_by=request.user
        )
        
        reservation.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        print("error", e)
        return JsonResponse({'success': False})
    
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_reservations(request, pk):
    property = Property.objects.get(pk=pk)
    reservations = property.reservations.all()
    
    serializer = ReservationSerializer(reservations, many=True)
    return JsonResponse(serializer.data, safe=False)