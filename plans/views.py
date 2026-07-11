from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .models import TravelPlan, PlanItem
from datetime import date, timedelta


def _get_active_plan(user):
    # Active plan: latest plan belonging to user that has no PlanBooking (not yet booked)
    pl = TravelPlan.objects.filter(user=user).filter(planbooking__isnull=True).order_by('-created_at').first()
    return pl


def planner(request):
    """Show the user's active plan (or prompt to add items)."""
    if not request.user.is_authenticated:
        return render(request, 'plans/planner.html', {'plans': []})

    active = _get_active_plan(request.user)
    return render(request, 'plans/planner.html', {'plan': active})


@login_required
def add_to_plan(request):
    if request.method != 'POST':
        return redirect('planner')

    item_type = request.POST.get('item_type')
    object_id = request.POST.get('object_id')
    if not item_type or not object_id:
        messages.error(request, 'Invalid item')
        return redirect('planner')

    # Map to model
    model = None
    try:
        if item_type == 'flight':
            from flights.models import Flight as model
        elif item_type == 'hotel':
            from hotels.models import Hotel as model
        elif item_type == 'package':
            from packages.models import Package as model
        elif item_type == 'place':
            from places.models import Place as model
        else:
            model = None
    except Exception:
        model = None

    if model is None:
        messages.error(request, 'Unknown item type')
        return redirect('planner')

    try:
        obj = model.objects.get(pk=object_id)
    except Exception:
        messages.error(request, 'Item not found')
        return redirect('planner')

    # Find or create active plan
    plan = _get_active_plan(request.user)
    if not plan:
        plan = TravelPlan.objects.create(user=request.user, title='My trip')

    ct = ContentType.objects.get_for_model(obj)
    # avoid duplicates
    exists = PlanItem.objects.filter(plan=plan, content_type=ct, object_id=obj.pk).exists()
    if exists:
        messages.info(request, 'Item already in plan')
        return redirect('planner')

    PlanItem.objects.create(plan=plan, content_type=ct, object_id=obj.pk)
    messages.success(request, 'Added to Trip Plan')
    return redirect('planner')


@login_required
def plan_detail(request, pk):
    plan = get_object_or_404(TravelPlan, pk=pk, user=request.user)
    items = plan.items.select_related('content_type').all()
    return render(request, 'plans/detail.html', {'plan': plan, 'items': items})


@login_required
def book_plan(request, pk):
    # Convert plan items into concrete bookings and create a PlanBooking
    from bookings.models import FlightBooking, HotelBooking, PackageBooking, PlanBooking, PlaceBooking

    plan = get_object_or_404(TravelPlan, pk=pk, user=request.user)
    if plan.planbooking_set.exists():
        messages.error(request, 'This plan is already booked')
        return redirect('planner')

    items = plan.items.select_related('content_type').all()
    services = []
    total = 0
    today = date.today()

    for it in items:
        obj = it.content_object
        if obj is None:
            continue
        app = it.content_type.app_label
        try:
            if app == 'flights':
                fb = FlightBooking.objects.create(user=request.user, flight=obj, total_price=obj.price)
                services.append({'type': 'flight', 'id': fb.id})
                total += float(obj.price)
            elif app == 'hotels':
                # default 1-night booking
                hb = HotelBooking.objects.create(user=request.user, hotel=obj, check_in=today, check_out=today + timedelta(days=1), total_price=obj.price_per_night)
                services.append({'type': 'hotel', 'id': hb.id})
                total += float(obj.price_per_night)
            elif app == 'packages':
                pb = PackageBooking.objects.create(user=request.user, package=obj, total_price=obj.price)
                services.append({'type': 'package', 'id': pb.id})
                total += float(obj.price)
            elif app == 'places':
                plb = PlaceBooking.objects.create(user=request.user, place=obj, total_price=0)
                services.append({'type': 'place', 'id': plb.id})
        except Exception:
            # skip failures but continue
            continue

    plan_booking = PlanBooking.objects.create(user=request.user, plan=plan, total_price=total, service_items=services)
    messages.success(request, 'Plan booked — bookings created.')
    return redirect('plan_booking_detail', pk=plan_booking.pk)
