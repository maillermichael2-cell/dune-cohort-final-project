from django.shortcuts import render, get_object_or_404, redirect
from .models import Property, PropertyCategory, Favorite
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm
from django.contrib import messages

# Create your views here.

def home(request):
    properties = Property.objects.order_by('-created_at')[:4]
    categories = PropertyCategory.objects.annotate(property_count=Count('properties'))
    context = {
        'properties': properties,
        'categories': categories,
    }
    return render(request, 'propertyApp/PropertyDashboard.html', context)


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
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, property=property_item).exists()
    return render(request, 'propertyApp/property_detail.html', {
        'property': property_item,
        'categories': categories,
        'is_agent': is_agent,
        'agent':owner_profile,
        'is_favorite': is_favorite,
    })

@login_required
def toggle_favorite(request, pk):
    property_item = get_object_or_404(Property, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, property=property_item)
    if not created:
        favorite.delete()
        messages.info(request, 'Property removed from favorites.')
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

