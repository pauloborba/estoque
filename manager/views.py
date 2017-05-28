from django.shortcuts import render
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from custom_user.models import customUser
from models import Item, Category, Price, Store
from models import *
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
    return render(request, 'home.html', {'is_home': True})

@require_http_methods(["GET"])
@login_required
def help(request):
    return render(request, 'help.html')

def price_list(request):
    prices = Price.objects.all()
    return render(request, 'price_list.html', {'prices': prices})

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


@require_http_methods(["GET", "POST"])
@login_required
def new_price(request):
    categories = Category.objects.all()
    itens = Item.objects.all()
    if request.method == 'GET':
        return render(request, 'new_price.html', {'name_taken': False, 'itens': itens, 'categories': categories})
    cost_product = float(request.POST["price"])
    item = request.POST["item"]
    item = Item.objects.get(id=int(item))
    category = request.POST["category"]
    category = Category.objects.get(id=int(category))
    try:
        price = Price.objects.get(price_category=category, price_product=item)
    except:
        Price.objects.create(cost_product=cost_product, price_category=category, price_product=item)
        x = Price.objects.all()
        return render(request, 'price_list.html', {'name_taken': False, 'prices': x})
    price.cost_product = cost_product;
    price.save()
    return HttpResponseRedirect(reverse("price_list"))


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


@require_http_methods(["GET", "POST"])
@login_required
def new_store(request):
    if request.method == 'GET':
        return render(request, 'new_store.html', {'name_taken': False})
    store_name = request.POST["name"].capitalize()
    try:
        Store.objects.create(store_name=store_name)
    except IntegrityError:
        return render(request, 'new_store.html', {'name_taken': True})
    return HttpResponseRedirect(reverse("home"))

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home_login"))

@login_required
@require_http_methods(["GET", "POST"])
def generate_list(request):
    if request.method == 'GET':
        stores = Store.objects.all()
        return render(request, 'chooseStores.html', {'stores': stores})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename='"+'lista'+".pdf'"
    p = canvas.Canvas(response)
    i = 0
    stores = request.POST.getlist('store_checkbox')
    stores = Store.objects.filter(id__in=stores)
    for store in stores:
        p.setFont("Helvetica", 25)
        p.drawString(35, (800-(30*i)), store.store_name)
        i += 1
        for cat in store.category_set.all():
            products = Price.objects.filter(price_category=cat)
            if not products:
                continue
            p.setFont("Helvetica", 20)
            p.drawString(120, (800-(30*i)), cat.category_name)
            i += 1
            for prod in products:
                p.setFont("Helvetica", 15)
                name = prod.price_product.item_name
                p.drawString(200, (800-(30*i)), name)
                p.drawString(240+(len(name)*5), (800-(30*i)), ' - ')
                p.drawString(240+(len(name)*10), (800-(30*i)), str(prod.cost_product))
                i += 1
            i += 1
    p.showPage()
    p.save()
    return response

    


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
        p.drawString(250, (800 - (30 * i)), cat.category_name)
        i += 1
        for item in items:
            p.setFont("Helvetica", 15)
            p.drawString(200, (800 - (30 * i)), item.item_name)
            i += 1
        i += 1

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


@require_http_methods(["GET", "POST"])
@login_required
def create_list_by_store(request):
    stores = Store.objects.all()
    cat = Category.objects.all()
    prices = Price.objects.all()
    return render(request, 'new_list_store.html', {'stores': stores, 'categories': cat, 'prices': prices})


@require_http_methods(["GET", "POST"])
@login_required
def create_store_file(request):
    stores = Store.objects.all()
    id = request.POST["store"]
    file_name = ''
    response = HttpResponse(content_type='application/pdf')
    for store in stores:
        if store.id == id:
            file_name = store.store_name
            categories = store.category_set.filter(category_store=id)
            response['Content-Disposition'] = "attachment; filename='" + file_name + ".pdf'"

            # Create the PDF object, using the response object as its "file."
            p = canvas.Canvas(response)

            i = 0
            for cat in categories:
                items = cat.item_set.filter(enough=False)
                if not items:
                    continue
                p.setFont("Helvetica", 25)
                p.drawString(250, (800 - (30 * i)), cat.category_name)
                i += 1
                for item in items:
                    p.setFont("Helvetica", 15)
                    p.drawString(200, (800 - (30 * i)), item.item_name)
                    i += 1
                i += 1

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
