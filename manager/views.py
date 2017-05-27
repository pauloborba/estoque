from django.shortcuts import render
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from custom_user.models import customUser
from models import Item, Category, Price
from reportlab.pdfgen import canvas
import datetime



@require_http_methods(["GET","POST"])
def home_login(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("home"))
        return render(request, 'home_login.html', {'error': False})
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'home_login.html', {'error': True})

@require_http_methods(["GET"])
@login_required
def home(request):
    cat = Category.objects.all()
    return render(request, 'home.html', {'categories': cat})

def test(request):
    prices = Price.objects.all()
    return render(request, 'teste.html', {'prices': prices})

@require_http_methods(["GET", "POST"])
def sign_up(request):
    if request.method=='GET':
        return render(request, 'sign_up.html')
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]
    customUser.objects.create_user(username, email, password)
    return HttpResponseRedirect(reverse("home_login"))

@require_http_methods(["GET", "POST"])
@login_required
def new_item(request):
    categories = Category.objects.all()
    if request.method=='GET':
        return render(request, 'new_item.html', {'name_taken': False, 'categories': categories})
    item_name = request.POST["name"].capitalize()
    enough = request.POST["enough"]
    enough = True if enough=="1" else False
    category = request.POST["category"]
    category = Category.objects.get(id=int(category))
    try:
        Item.objects.create(item_name=item_name, enough=enough, category=category)
    except IntegrityError:
        return render(request, 'new_item.html', {'name_taken': True, 'categories': categories})
    return HttpResponseRedirect(reverse("home"))

@require_http_methods(["POST"])
@login_required
def edit_item(request):
    item_id = request.POST["id"];
    item_to_edit = Item.objects.get(id=item_id)
    request.user.points += 1
    request.user.save()
    item_to_edit.enough = not item_to_edit.enough
    item_to_edit.save()
    return HttpResponse(request.user.points);

@require_http_methods(["GET", "POST"])
@login_required
def new_category(request):
    if request.method=='GET':
        return render(request, 'new_category.html', {'name_taken': False})
    category_name = request.POST["name"].capitalize()
    try:
        Category.objects.create(category_name=category_name)
    except IntegrityError:
        return render(request, 'new_category.html', {'name_taken': True})
    return HttpResponseRedirect(reverse("home"))

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home_login"))

@login_required
def generate_pdf(request):
    today_date = datetime.datetime.today()
    day = ("0"+str(today_date.day)) if today_date.day < 10 else str(today_date.day)
    month = ("0"+str(today_date.month)) if today_date.month < 10 else str(today_date.month)
    file_name = "feira_"+day+"_"+month+"_"+str(today_date.year)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename='"+file_name+".pdf'"

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    categories = Category.objects.all()

    i = 0
    for cat in categories:
        items = cat.item_set.filter(enough=False)
        if not items:
            continue
        p.setFont("Helvetica", 25)
        p.drawString(250, (800-(30*i)), cat.category_name)
        i += 1
        for item in items:
            p.setFont("Helvetica", 15)
            p.drawString(200, (800-(30*i)), item.item_name)
            i += 1
        i += 1

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
