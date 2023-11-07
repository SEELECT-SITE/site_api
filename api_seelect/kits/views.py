###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from events.serializers import *
from kits.serializers import *
from users.serializers import *

###########################################################################################
# Pagination Classes                                                                      #
###########################################################################################
class StandardKitSetPagination(PageNumberPagination):
    page_size = 500
    page_size_query_param = 'page_size'
    max_page_size = 1000

###########################################################################################
# Requests Classes                                                                        #
###########################################################################################
# .../api/kits/
class KitsList(APIView, StandardKitSetPagination):
    """
    List all kits, or create a new kit.
    """
    pagination_class = StandardKitSetPagination

    def get(self, request, format=None):    
        queryset = Kits.objects.get_queryset().order_by('id')
        
        page = self.paginate_queryset(queryset, request)

        if page is not None:
            serializer = KitsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = Kits(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        kits_data = request.data.copy()
        events_data = kits_data.pop('events', [])

        # Check if user id exist.
        user_id = request.data.get('user')

        try:
            user_profile = UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return Response({"error": "User profile with ID {} does not exist.".format(user_id)}, status=status.HTTP_404_NOT_FOUND)

        # Check if model id exist.
        model_id = request.data.get('model')
        
        try:
            model = KitModels.objects.get(pk=model_id)
        except KitModels.DoesNotExist:
            return Response({"error": "Kit Model with ID {} does not exist.".format(model_id)}, status=status.HTTP_404_NOT_FOUND)
                
        # Getting user object to get the email
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User with ID {} does not exist.".format(user_id)}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the email have some discount.
        try:
            discount = KitsDiscount.objects.get(email=user.email)
            kits_data['discount'] = discount.discount
        except KitsDiscount.DoesNotExist:
            kits_data['discount'] = 0
        
        serializer = KitsSerializer(data=kits_data)

        if serializer.is_valid():
            serializer.validated_data['user'] = user_profile
            kit = serializer.save()

            for events_id in events_data:
                try:
                    event = Events.objects.get(pk=events_id)

                    if event.newInscription():
                        KitsEvents.objects.create(kit=kit, event=event)

                except Events.DoesNotExist:
                    pass

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

###########################################################################################
# .../api/kits/<id>
class KitsDetail(APIView):
    """
    Retrieve, update or delete a kit instance.
    """
    def get_object(self, pk):
        # Getting the kit by id.
        try:
            return Kits.objects.get(pk=pk)
        # Return 404 if the kit don't exist.
        except Kits.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        kit = self.get_object(pk)
        serializer = KitsSerializer(kit)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        kit = self.get_object(pk)
        
        kits_data = request.data.copy()
        # Getting events
        events_data = kits_data.pop('events', [])
        
        # Removing fields which you shouldn't change there.
        kits_data.pop('user', None)
        kits_data.pop('discount', None)
        kits_data.pop('is_payed', None)
        
        # If the payements was done, you can't change the model.
        if kit.is_payed:
            kits_data.pop('model', None)
                
        kits_serializer = KitsSerializer(kit, data=kits_data)

        if kits_serializer.is_valid():
            kit = kits_serializer.save() # Update event data

            # Access associated events
            associated_events = kit.events.all()

            # Print the associated events
            for event in associated_events:
                event = Events.objects.get(pk=event.id)
                event.deleteInscription()
                
            # Remove existing associations with places
            kit.events.clear()

            for events_id in events_data:
                try:
                    event = Events.objects.get(pk=events_id)
                    
                    if event.newInscription():
                        KitsEvents.objects.create(kit=kit, event=event)
                except Events.DoesNotExist:
                    pass
            
            return Response(kits_serializer.data, status=status.HTTP_200_OK)
        return Response(kits_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        kit = self.get_object(pk)
        
        # Access associated events
        associated_events = kit.events.all()

        # Print the associated events
        for event in associated_events:
            event = Events.objects.get(pk=event.id)
            event.deleteInscription()
        
        kit.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
###########################################################################################
# .../api/kits/models/
class KitsModelsList(APIView, StandardKitSetPagination):
    """
    List all kits models, or create a new kit model.
    """
    pagination_class = StandardKitSetPagination

    def get(self, request, format=None):    
        queryset = KitModels.objects.get_queryset().order_by('id')
        
        page = self.paginate_queryset(queryset, request)

        if page is not None:
            serializer = KitsModelSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = KitModels(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = KitsModelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

###########################################################################################
# .../api/kits/models/<id>
class KitsModelsDetail(APIView):
    """
    Retrieve, update or delete a kit model instance.
    """
    def get_object(self, pk):
        # Getting the kit model by id.
        try:
            return KitModels.objects.get(pk=pk)
        # Return 404 if the kit model don't exist.
        except KitModels.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        model = self.get_object(pk)
        serializer = KitsModelSerializer(model)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        model = self.get_object(pk)

        serializer = KitsModelSerializer(model, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    def delete(self, request, pk, format=None):
        model = self.get_object(pk)
        model.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

###########################################################################################
# .../api/kits/discount/
class KitsDiscountList(APIView, StandardKitSetPagination):
    """
    List all kits discounts, or create a new kit discount.
    """
    pagination_class = StandardKitSetPagination

    def get(self, request, format=None):    
        queryset = KitsDiscount.objects.get_queryset().order_by('id')
        
        page = self.paginate_queryset(queryset, request)

        if page is not None:
            serializer = KitsDiscountSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = KitsDiscount(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = KitsDiscountSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

###########################################################################################
# .../api/kits/discout/<id>
class KitsDiscountDetail(APIView):
    """
    Retrieve, update or delete a kit discount instance.
    """
    def get_object(self, pk):
        # Getting the kit discount by id.
        try:
            return KitsDiscount.objects.get(pk=pk)
        # Return 404 if the kit discount don't exist.
        except KitsDiscount.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        discount = self.get_object(pk)
        serializer = KitsDiscountSerializer(discount)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        discount = self.get_object(pk)

        serializer = KitsDiscountSerializer(discount, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    def delete(self, request, pk, format=None):
        discount = self.get_object(pk)
        discount.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
###########################################################################################
# .../api/kits/<id>/confirm_payment/
@api_view(['POST'])
def confirm_payment(request, pk):
    """
    Confirm payment.
    """

    # Getting the event by id.
    try:
        kit = Kits.objects.get(pk=pk)
    # Return 404 if the event don't exist.
    except Kits.DoesNotExist:
        raise Http404
    
    # Updating is_payed value or let the old value.
    kit.is_payed = request.data.get('is_payed', kit.is_payed)
    kit.save()
    
    serializer = KitsSerializer(kit)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

###########################################################################################
# .../api/kits/<id>/change_discount/
@api_view(['POST'])
def change_discount(request, pk):
    """
    Change discount value.
    """

    # Getting the event by id.
    try:
        kit = Kits.objects.get(pk=pk)
    # Return 404 if the event don't exist.
    except Kits.DoesNotExist:
        raise Http404
    
    # Updating is_payed value or let the old value.
    kit.discount = request.data.get('discount', kit.discount)
    kit.save()
    
    serializer = KitsSerializer(kit)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

###########################################################################################