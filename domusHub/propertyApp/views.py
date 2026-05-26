from django.shortcuts import render, get_object_or_404, redirect
from .models import Property, PropertyCategory, Favorite
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm
from django.contrib import messages
import urllib.parse 
# rest framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PropertySerializer, PropertyCategorySerializer
#
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .pagination import PropertyPagination
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.

def home(request):
    properties = Property.objects.order_by('-created_at')[:4]
    categories = PropertyCategory.objects.annotate(property_count=Count('properties'))
    context = {
        'properties': properties,
        'categories': categories,
    }
    return render(request, 'propertyApp/propertyDashboard.html', context)


def about(request):
    return render(request, 'propertyApp/about.html')


def property_detail(request, pk):
    property_item = get_object_or_404(Property, pk=pk)
    categories = PropertyCategory.objects.annotate(property_count=Count('properties'))
    profile = getattr(request.user, 'profile', None)
    is_agent = bool(request.user.is_authenticated and profile and profile.role == 'ESTATE AGENT')
    owner_profile = None
    if property_item.owner and hasattr(property_item.owner, 'profile'):
        owner_profile = property_item.owner.profile
        if getattr(owner_profile, 'phone_number', None):
            clean_phone = "".join(filter(str.isdigit, str(owner_profile.phone_number)))
            if clean_phone.startswith('0') and len(clean_phone) > 11:
                clean_phone = '234' + clean_phone[1:]
            message = f'Hello , i am intrested in your property: {property_item.title}'
            encoded_message = urllib.parse.quote(message)
            whatsapp_url = f"whatsapp://send?phone={clean_phone}&text={encoded_message}"
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, property=property_item).exists()
    
    return render(request, 'propertyApp/property_detail.html', {
        'property': property_item,
        'categories': categories,
        'is_agent': is_agent,
        'agent':owner_profile,
        "whatsapp_url": whatsapp_url,
        'is_favorite': is_favorite,
    })

@login_required
def toggle_favorite(request, pk):
    property_item = get_object_or_404(Property, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, property=property_item)
    if not created:
        favorite.delete()
        messages.info(request, 'Property removed from favorites.')
        return redirect('individual_dashboard')
    else:
        messages.success(request, 'Property added to favorites.')
    return redirect('property_detail', pk=pk)

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('property')
    categories = PropertyCategory.objects.annotate(property_count=Count('properties'))
    return render(request, 'propertyApp/favorites_list.html', {
        'favorites': favorites,
        'categories': categories,
    })

@login_required
def individual(request, slug=None):
    search = request.GET.get('search', '')
    categories = PropertyCategory.objects.annotate(property_count=Count('properties'))
    properties = Property.objects.all().order_by('-created_at')

    if slug:
        category = get_object_or_404(PropertyCategory, slug=slug)
        properties = properties.filter(category=category)
    if search:
        properties = properties.filter(
            Q(title__icontains=search) |
            Q(property_address__icontains=search) |
            Q(category__name__icontains=search)
        )

    return render(request, 'propertyApp/individual_dashboard.html', {
        'categories': categories,
        'properties': properties,
        'search': search,
        'active_category': slug,
    })


@login_required
def agent_dashboard(request):
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.role != 'ESTATE AGENT':
        messages.error(request, 'Only estate agents can access the agent dashboard.')
        return redirect('individual_dashboard')

    properties = Property.objects.filter(owner=request.user).order_by('-created_at')

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_item = form.save(commit=False)
            property_item.owner = request.user
            property_item.save()
            messages.success(request, 'Property created successfully.')
            return redirect('agent_dashboard')
    else:
        form = PropertyForm()

    return render(request, 'propertyApp/agent_dashboard.html', {
        'form': form,
        'properties': properties,
    })


@login_required
def property_edit(request, pk):
    property_item = get_object_or_404(Property, pk=pk)
    if property_item.owner != request.user:
        messages.error(request, 'You can only edit your own properties.')
        return redirect('property_detail', pk=property_item.pk)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully.')
            return redirect('property_detail', pk=property_item.pk)
    else:
        form = PropertyForm(instance=property_item)

    return render(request, 'propertyApp/property_edit.html', {
        'form': form,
        'property': property_item,
    })


@login_required
def property_delete(request, pk):
    property_item = get_object_or_404(Property, pk=pk)
    if property_item.owner != request.user:
        messages.error(request, 'You can only delete your own properties.')
        return redirect('property_detail', pk=property_item.pk)

    if request.method == 'POST':
        property_item.delete()
        messages.success(request, 'Property deleted successfully.')
        return redirect('agent_dashboard')

    return render(request, 'propertyApp/property_delete_confirm.html', {
        'property': property_item,
    })





# API VIEW SECTION START
class PropertyListAPIView(ListAPIView):
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination
    authentication_classes = [JWTAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category__slug']
    search_fields = ['title', 'property_address', 'category__name']
    ordering_fields = ['created_at', 'price']
    ordering = ['-created_at']

    def filter_queryset(self,queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset
    
    def get(self, request):
        filtered_queryset = self.filter_queryset(self.queryset)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(filtered_queryset, request, view=self)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.serializer_class(filtered_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PropertyDetail(APIView):
    def get_object(self,pk):
        try:
            return Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            return None
    def get(self,request,pk):
        property_item = self.get_object(pk)
        if not property_item:
            return Response({'detail': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PropertySerializer(property_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self,request,pk):
        property_item = self.get_object(pk)
        if not property_item:
            return Response({'detail': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)
        if property_item.owner != request.user:
            return Response({'detail': 'You do not have permission to edit this property.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PropertySerializer(property_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        property_item = self.get_object(pk)
        if not property_item:
            return Response({'detail': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)
        if property_item.owner != request.user:
            return Response({'detail': 'You do not have permission to delete this property.'}, status=status.HTTP_403_FORBIDDEN)
        property_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PropertyCategoryListAPIView(ListAPIView):
    def get(self, request):
        categories = PropertyCategory.objects.annotate(property_count=Count('properties'))
        serializer = PropertyCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PropertyCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        profile = getattr(request.user, 'profile', None)
        if not profile or profile.role != 'ESTATE AGENT':
            return Response({'detail': 'Only estate agents can create properties.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)