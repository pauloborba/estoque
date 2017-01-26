from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from custom_user.models import customUser
from models import Item
from reportlab.pdfgen import canvas
import datetime

@require_http_methods(["GET","POST"])
def home_login(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("home"))
        return render(request, 'home_login.html')
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
    return HttpResponseRedirect(reverse('home_login'))

@require_http_methods(["GET"])
@login_required
def home(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

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
    if request.method=='GET':
        return render(request, 'new_item.html')
    item_name = request.POST["name"]
    qty = request.POST["qty"]
    Item.objects.create(item_name=item_name, qty=int(qty))
    return HttpResponseRedirect(reverse("home"))

@require_http_methods(["GET", "POST"])
@login_required
def edit_item(request, item_id):
    item_to_edit = Item.objects.get(id=item_id)
    if request.method=="GET":
        return render(request, 'edit_item.html', {'item': item_to_edit})
    updateVal = int(request.POST["qty"])
    if updateVal != item_to_edit.qty:
        request.user.points += 1
        request.user.save()
        item_to_edit.qty = updateVal
        item_to_edit.save()
    return HttpResponseRedirect(reverse('home'))

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
    p.setFont("Helvetica", 15)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    items = Item.objects.filter(qty__in=[1,2])
    i = 0
    for item in items:
        p.drawString(10, (800-(30*i)), item.item_name+':')
        if item.qty == 1:
            p.drawString(140, (800-(30*i)), "Pouco")
        else:
            p.drawString(140, (800-(30*i)), "Acabou")
        i += 1

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
