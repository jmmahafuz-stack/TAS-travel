from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Place, Activity


@require_GET
def place_list_api(request):
    """Return a JSON list of places, optionally filtered by `city` or `destination` query param."""
    city = request.GET.get('city') or request.GET.get('destination')
    qs = Place.objects.all()
    if city:
        qs = qs.filter(city__icontains=city)

    data = []
    for p in qs[:200]:
        data.append({
            'id': p.id,
            'name': p.name,
            'city': p.city,
            'description': p.description,
            'thumbnail_url': request.build_absolute_uri(p.thumbnail.url) if p.thumbnail else '',
        })
    return JsonResponse(data, safe=False)


@require_GET
def activities_api(request):
    """Return activities for given place(s). Accepts `place_ids` (csv) or `place_id` or `city`."""
    place_ids = request.GET.get('place_ids')
    place_id = request.GET.get('place_id')
    qs = Activity.objects.select_related('place').all()

    if place_ids:
        ids = [int(x) for x in place_ids.split(',') if x.isdigit()]
        qs = qs.filter(place_id__in=ids)
    elif place_id and place_id.isdigit():
        qs = qs.filter(place_id=int(place_id))
    else:
        city = request.GET.get('city')
        if city:
            qs = qs.filter(place__city__icontains=city)

    data = []
    for a in qs[:500]:
        data.append({
            'id': a.id,
            'title': a.title,
            'description': a.description,
            'price': str(a.price),
            'place_id': a.place_id,
            'place_name': a.place.name,
        })
    return JsonResponse(data, safe=False)
