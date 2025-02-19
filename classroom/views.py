import base64
import json
from django.shortcuts import redirect, render, get_object_or_404
import requests
from .models import Vehicle, ParkingLocation, VehicleLocation
from .forms import VehicleLocationForm
from classroom.models import Vehicle
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from twilio.rest import Client
import stripe
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import Payment
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.urls import reverse_lazy
from classroom.models import ParkingLocation
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView 
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse
from .forms import CustomerForm, UserForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.http import Http404
from geopy.geocoders import Nominatim
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.core import serializers
from django.conf import settings
from django.utils.timezone import now
import os
from .models import Customer,User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from datetime import datetime, date
from django.core.exceptions import ValidationError
from . import models
import operator
import itertools
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from .mpesa import stk_push_request
from django.contrib.auth.mixins import LoginRequiredMixin
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.hashers import make_password
from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)

stripe.api_key = settings.STRIPE_SECRET_KEY



def signup(request):
    return render(request, 'dashboard/login.html')


def home(request):
    return render(request, 'dashboard/login.html')


def dashboard(request):
    total_it = Customer.objects.aggregate(Sum("total_cost"))

    print(total_it.get("total_cost__sum"))
    total_it = total_it.get("total_cost__sum")

    total_cost = total_it
    
    customers = Customer.objects.all()

    total_vehicles = Customer.objects.all().count()
    total_users = User.objects.all().count()


    context = {'total_cost':total_cost, 'users':total_users, 'cars':total_vehicles,'customers': customers,}
    return render(request, 'dashboard/dashboard.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('dashboard')
            elif user.is_cashier:
                return redirect('dashboard')
            else:
                return redirect('login')
        else:
            messages.error(request, 'Wrong Username or Password')
            return redirect('home')        

def logout_view(request):
    logout(request)
    return redirect('/')                


def add_vehicle(request):
    choice = ['1', '0', 10000, 15000, 'Accomodation Fee', 'Verified All Spare']
    choice = {'choice':choice}
    return render(request, 'dashboard/add_vehicle.html', choice)


def save_vehicle(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        card_number = request.POST['card_number']
        car_model = request.POST['car_model']
        car_color = request.POST['car_color']
        phone_number = request.POST['phone_number']
        comment = request.POST['comment']
        device = request.POST['device']
        cost_per_day = request.POST['cost_per_day']
        register_name = request.POST['register_name']
        current_time = datetime.now()
        date_time = current_time.strftime("%Y,%m,%d")
        email = request.POST['email']
        location =request.POST['location']

        a = Customer(first_name=first_name, last_name=last_name, card_number=card_number, car_model=car_model, car_color=car_color, reg_date=date_time,register_name=register_name,comment=comment, cost_per_day=cost_per_day, device=device, email=email, location=location)
        a.save()


        send_mail(
        'Parking Spot Reserved',
        f'Hello {first_name} {last_name},\n\nYour parking spot has been successfully reserved.',
        'settings.EMAIL_HOST_USER',
        [email],
        fail_silently=False,


    )


        messages.success(request, 'Vehicle Registered Successfully')
        return redirect('vehicle')


class ListVehicle(ListView):
    model = Customer
    template_name = 'dashboard/vehicles.html'
    context_object_name = 'customers'
    paginate_by = 2

    def get_queryset(self):
        return Customer.objects.filter(is_payed=True)
    
class VehicleDetailsView(ListView):  # Wrong for a detail view
    model = Vehicle
    template_name = 'vehicle_details.html'
    context_object_name = 'vehicle'


class UserView(ListView):
    model = User
    template_name = 'dashboard/list_user.html'
    context_object_name = 'users'
    paginate_by = 5

    def get_queryset(self):
        return User.objects.order_by('-id')



class Vehicle(ListView):
    model = Customer
    template_name = 'dashboard/list_vehicle.html'
    context_object_name = 'customers'
    paginate_by = 2

    def get_queryset(self):
        return Customer.objects.filter(is_payed="False")



class UserUpdateView(BSModalUpdateView):
    model = User
    template_name = 'dashboard/u_update.html'
    form_class = UserForm
    success_message = 'Success: Data was updated.'
    success_url = reverse_lazy('users')



class VehicleReadView(BSModalReadView):
    model = Customer
    template_name = 'dashboard/view_vehicle.html'


class CarReadView(BSModalReadView):
    model = Customer
    template_name = 'dashboard/view_vehicle2.html'

class UserReadView(BSModalReadView):
    model = User
    template_name = 'dashboard/view_user.html'

class VehicleUpdateView(BSModalUpdateView):
    model = Customer
    template_name = 'dashboard/update_vehicle.html'
    form_class = CustomerForm
    success_url = reverse_lazy('vehicle')


class CarUpdateView(BSModalUpdateView):
    model = Customer
    template_name = 'dashboard/update_vehicle2.html'
    form_class = CustomerForm
    success_url = reverse_lazy('listvehicle')



class VehicleDeleteView(BSModalDeleteView):
    model = Customer
    template_name = 'dashboard/delete_vehicle.html'
    form_class = CustomerForm
    success_url = reverse_lazy('vehicle')
    success_message = "Vehicle has been successfully deleted."




class CarDeleteView(BSModalDeleteView):
    model = Customer
    template_name = 'dashboard/delete_vehicle2.html'
    form_class = CustomerForm
    success_url = reverse_lazy('listvehicle')
    success_message = 'car was successfully deleted.'

    def get_success_message(self, cleaned_data):
        return self.success_message
    
class VehicleLocationView(DetailView):
    model = Vehicle
    template_name = 'vehicle_location.html'  # Your template
    context_object_name = 'vehicle'

    def get(self, request, *args, **kwargs):
        # Ensuring that you get the correct vehicle instance based on the URL argument
        vehicle = self.get_object()  # This retrieves the vehicle based on the ID in the URL
        return self.render_to_response(self.get_context_data(vehicle=vehicle))




def Pay(request, pk):
    # try:
    #     # Fetch customer by pk
    #     customer = Customer.objects.get(id=pk)
    # except ObjectDoesNotExist:
    #     # Handle customer not found
    #     messages.error(request, "Customer not found.")
    #     return redirect('listvehicle')

    # if request.method == 'POST':
    #     payment_method = request.POST.get('payment_method')
    #     print(f'Payment method received: {payment_method}')

    #     if not payment_method:
    #         messages.error(request, "Please select a payment method.")
    #         return redirect('pay', pk=pk)  # Redirect back to payment page with error

    #     # Update customer status and payment method
    #     customer.exit_date = timezone.now()
    #     customer.is_payed = True
    #     customer.payment_method = payment_method
    #     customer.save()

    #     # Calculate months spent
    #     reg_date = customer.reg_date
    #     exit_date = customer.exit_date
    #     delta = exit_date - reg_date
    #     mo = delta.days // 30  # Calculate months spent

    #     if mo == 0:
    #         mo = 1  # Minimum 1 month

    #     customer.days_spent = mo
    #     total_cost = customer.cost_per_day * mo
    #     customer.total_cost = total_cost
    #     customer.save()

    #     messages.success(request, f'Payment was finished successfully using {payment_method}.')
    #     print(f'Redirect to listvehicle with customer {customer.pk}')
    #     return redirect('listvehicle')

    # return render(request, 'dashboard/payment.html', {'customer': customer})

    Customer.objects.filter(id = pk).update(exit_date = timezone.now())
    Customer.objects.filter(id = pk).update(is_payed = "True")
    reg_date = Customer.objects.values_list('reg_date').filter(id = pk)
    exit_date = Customer.objects.values_list('exit_date').filter(id = pk)

    a = str(reg_date)
    b = str(exit_date)

    x = a[30:59]
    y = b[30:59]

    date_time_str = x
    date_time_str2 = y

    myTime = datetime.strptime(date_time_str, "%Y, %m, %d, %H, %M, %S, %f")
    myTime2 = datetime.strptime(date_time_str2, "%Y, %m, %d, %H, %M, %S, %f")


    myFormat = ("%Y,%m,%d")
    new_reg_date = myTime.strftime(myFormat)
    new_exit_date = myTime2.strftime(myFormat)

    d2 = myTime2.date()
    d1 = myTime.date()

    delta = d2 -d1
    mo = delta.days

    if mo == 0:
        mo =1
    else:
        mo = mo

    Customer.objects.filter(id = pk).update(days_spent = mo)
    cost_per_day = Customer.objects.values_list('cost_per_day').filter(id = pk)
    days_spent = Customer.objects.values_list('days_spent').filter(id = pk)

    cpd = str(cost_per_day)
    cpd = cpd[12:-7]

    if cpd == str(15):
       cost_per_day = 15000
       total_cost = cost_per_day * mo
       Customer.objects.filter(id = pk).update(total_cost = total_cost)
       messages.success(request, 'Payment Was Finished Successfully')
       return redirect('listvehicle')
    else:
        cost_per_day = 10000
        total_cost = cost_per_day * mo
        Customer.objects.filter(id = pk).update(total_cost = total_cost)
        payment_method = request.POST.get('payment_method')
        payment_date = timezone.now()
        Customer.payment_method = payment_method
        Customer.payment_date = payment_date
        customer = Customer.objects.get(id = pk)
        customer.save()
        messages.success(request, 'Payment Was Finished Successfully')
        return redirect('listvehicle')   





def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



class GeneratePdf(ListView):
    def get(self, request, pk, *args, **kwargs):
        #info = Customer.objects.filter(id=pk)
        infos = Customer.objects.filter(id=pk).values('id','first_name','last_name','total_cost','days_spent', 'reg_date', 'exit_date', 'card_number','payment_method','payment_date')
        print(infos)
        context = {
        "data": {
            'today': 'Today', 
             'amount': 39.99,
            'customer_name': 'Festus ',
            'order_id': 1233434,
            'location': ' KENYA, NAIROBI',
            'address': 'P.Box 1458 NAIROBI',
            'email': 'info@techapp.com',
        },
        "infos": infos,
        }

        pdf = render_to_pdf('dashboard/invoice.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


class GeneratePDF(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')  # get customer ID from URL kwargs
        customer = Customer.objects.get(id=customer_id)  # retrieve customer by ID
        
        # Prepare the context with payment details
        context = {
            "invoice_id": customer.id,
            "customer_name": f"{customer.first_name} {customer.last_name}",
            "amount": customer.total_cost,
            "payment_method": customer.payment_method,  # Add payment method
            "payment_date": customer.payment_date,  # Add payment date
            "today": "Today",
        }
        
        # Use the template to render the HTML content
        template = get_template('invoice.html')
        html = template.render(context)
        
        # Generate the PDF
        pdf = render_to_pdf('dashboard/invoice.html', context)
        
        if pdf:
            # Prepare the response to return the generated PDF
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"Invoice_{customer.id}.pdf"
            content = f"inline; filename='{filename}'"
            download = request.GET.get("download")
            if download:
                content = f"attachment; filename='{filename}'"
            response['Content-Disposition'] = content
            return response
        
        # In case the PDF is not generated
        return HttpResponse("Not found")


class DeleteUser(BSModalDeleteView):
    model = User
    template_name = 'dashboard/delete_user.html'
    success_message = 'Success: Data was deleted.'
    success_url = reverse_lazy('users')



def create(request):
    choice = ['1', '0', 5000, 10000, 15000, 'Register', 'Admin', 'Cashier']
    choice = {'choice': choice}
    if request.method == 'POST':
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            username=request.POST['username']
            userType=request.POST['userType']
            email=request.POST['email']
            password=request.POST['password']
            password = make_password(password)
            print("User Type")
            print(userType)
            if userType == "Register":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_register=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('users')
            elif userType == "Cashier":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_cashier=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('users')
            elif userType == "Admin":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_admin=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('users')    
            else:
                messages.success(request, 'Member was not created')
                return redirect('users')
    else:
        choice = ['1', '0', 5000, 10000, 15000, 'Register', 'Admin', 'Cashier']
        choice = {'choice': choice}
        return render(request, 'dashboard/add.html', choice)
    

def calculate_total(request):
    # Example data
    charges = {
        'base_fee': 50,
        'hourly_fee': 20,
        'tax': 10,
    }
    total_amount = charges['base_fee'] + charges['hourly_fee'] + charges['tax']
    return render(request, 'total_amount.html', {'charges': charges, 'total_amount': total_amount})



class CustomerListView(ListView):
    model = Customer
    template_name = 'customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10

    def get_queryset(self):
        # ordering = self.request.GET.get('ordering', 'name')
        return Customer.objects.all().order_by('reg_date')

def park_vehicle(request, vehicle_id, location_id):
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
        location = ParkingLocation.objects.get(id=location_id)
    except Vehicle.DoesNotExist:
        raise Http404("Vehicle not found")
    except ParkingLocation.DoesNotExist:
        raise Http404("Parking location not found")
    
    if location.is_occupied:
        return render(request, 'error.html', {'message': 'Parking spot is already occupied.'})

    vehicle.parking_location = location
    vehicle.save()
    location.is_occupied = True
    location.save()

    return render(request, 'dashboard/park_vehicle.html', {'vehicle': vehicle, 'location': location})
def unpark_vehicle(request, pk):
    vehicle = Vehicle.objects.get(pk=pk)
    parking_location = vehicle.parked_at
    if parking_location:
        parking_location.is_occupied = False
        parking_location.save()
    vehicle.delete()
    return redirect('dashboard')  # Or another page

def track_vehicle(request, pk):
    # Get the vehicle by its primary key (pk)
    vehicle = get_object_or_404(VehicleLocation, pk=pk)

    # If the vehicle has a town name, use geocoding to find coordinates
    geolocator = Nominatim(user_agent="vehicle_tracker")
    location = geolocator.geocode(vehicle.town)
    
    if location:
        latitude = location.latitude
        longitude = location.longitude
    else:
        latitude = None
        longitude = None
    
    # Pass the vehicle's details along with the coordinates to the template
    context = {
        'vehicle': vehicle,
        'latitude': latitude,
        'longitude': longitude,
    }
    return render(request, 'dashboard/track_vehicle.html', context)


def parking_lot(request):
    # Fetch all parking locations
    locations = ParkingLocation.objects.all()
    
    # If you want to track a specific vehicle's location
    vehicle_id = request.GET.get('vehicle_id')  # Get the vehicle ID from the query parameters
    vehicle = None
    if vehicle_id:
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    
    return render(request, 'dashboard/parking_lot.html', {'locations': locations, 'vehicle': vehicle})

def vehicle_location(request, license_plate):
    vehicle = get_object_or_404(VehicleLocation, license_plate=license_plate)    

    return render(request, 'vehicle_location.html', {
        'vehicle': vehicle,
    })


def update_car(request, pk):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        car = get_object_or_404(car, pk=pk)
        car.status = 'updated'
        car.save()
        return JsonResponse({'message': 'Car updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    

# def payment(request):
#     if request.method == 'POST':
#         payment_method = request.POST.get('payment_method')
#         amount = 100.00  # Fixed parking fee (you can make this dynamic)
#         Payment.objects.create(user=request.user, amount=amount, payment_method=payment_method)

#         # Success message
#         messages.success(request, "Payment successful! Your booking is confirmed.")
#         return redirect('home')  # Redirect to home after payment

#     return render(request, 'dashboard/payment.html')
class ParkCarView(APIView):
    def post(self, request):
        car_id = request.data.get("car_id")
        space_id = request.data.get("space_id")
        try:
            car = Vehicle.objects.get(id=car_id)
            space = ParkingLocation.objects.get(id=space_id)
            if not space.is_occupied:
                car.parked_at = space
                car.save()
                space.is_occupied = True
                space.save()

                # Send notification
                self.send_parking_notification(car.phone_number, car.license_plate, space.space_number)
                return Response({"message": "Car parked successfully"})
            return Response({"error": "Space is already occupied"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

def send_parking_notification(request, parking_spot_id):
    # Email configuration
    parking_spot = ParkingLocation.objects.get(id=parking_spot_id)
    user = request.user

    # Reserve the parking spot (You can customize this logic)
    parking_spot.is_reserved = True
    parking_spot.reserved_by = user
    parking_spot.save()

    # Send notification email
    send_mail(
        'Parking Spot Reserved',
        f'Hello {user.username},\n\nYour parking spot (Spot #{parking_spot.id}) has been successfully reserved.',
        'admin@example.com',  # Sender's email
        [user.email],  

    )
    # Redirect or render the response as needed
    return render(request, 'dashboard/parking_lot.html', {'parking_spot': parking_spot})

def amount_details(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    return render(request, 'dashboard/amount_details.html', {'total_amount': customer.total_cost})

def vehicle_details(request):
    from classroom.models import Vehicle
    vehicles = Vehicle.objects.all()  # Get all vehicles
    return render(request, 'dashboard/vehicle_details.html', {'vehicles': vehicles})


def user_details(request, user_id=None):
    if user_id:
        # Retrieve the specific user by user_id
        try:
            user = User.objects.get(id=user_id)
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "date_joined": user.date_joined,
                "last_login": user.last_login,
            }
        except User.DoesNotExist:
            user_data = {"error": "User not found"}
    else:
        # If no user_id is provided, retrieve all users
        users = User.objects.all()
        user_data = []
        for user in users:
            user_data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "date_joined": user.date_joined,
                "last_login": user.last_login,
            })

    return JsonResponse(user_data, safe=False)

def update_payment_method_page(request, id):
    customer_id = request.user.profile.stripe_customer_id
    setup_intent = stripe.SetupIntent.create(customer=customer_id)
    return render(request, "update_payment_method.html", {
        "publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
        "client_secret": setup_intent.client_secret,
        "id":id
    })


def update_payment_method(request, pk):
    if request.method == "POST":
        try:
            # Retrieve the customer by pk
            customer = Customer.objects.get(id=pk)
            payment_method = request.POST.get("payment_method")

            if not payment_method:
                messages.error(request, "No payment method selected.")
                return redirect('pay', pk=pk)

            # Update the payment method
            customer.payment_method = payment_method
            customer.payment_date = timezone.now()
            customer.is_payed = True
            customer.save()

            # Optionally, perform additional payment logic (e.g., Stripe integration)
            # For example, save the payment method to Stripe if you're using it
            # stripe.PaymentMethod.attach(payment_method_id, customer=customer.stripe_customer_id)

            messages.success(request, "Payment method updated successfully.")
            return redirect('listvehicle')
        except Customer.DoesNotExist:
            messages.error(request, "Customer not found.")
            return redirect('listvehicle')
    else:
        messages.error(request, "Invalid request method.")
        return redirect('listvehicle')


def invoice_view(request, pk):
    customer = get_object_or_404(Customer, id=pk)

    

    return render(request, 'invoice.html', {'infos': [customer]})

      

def get_vehicle_data(request):
    from classroom.models import Vehicle
    vehicles = Vehicle.objects.all().values('id', 'owner', 'license_plate', 'vehicle_type')
    return JsonResponse(list(vehicles), safe=False)


def vehicle_map(request):
    vehicles = VehicleLocation.objects.all()
    return render(request, 'dashboard/vehicle_map.html', {'vehicles': vehicles})

from rest_framework.decorators import api_view

@api_view(['GET'])
def get_vehicle_data(request):
    from .serializers import VehicleSerializer
    from classroom.models import Vehicle
    vehicles = Vehicle.objects.all()  # Fetch all vehicles from the database
    serializer = VehicleSerializer(vehicles, many=True)  # Serialize the vehicle data
    return Response(serializer.data)

def global_search(request):
    query = request.GET.get("query", "")
    vehicle_results = VehicleLocation.objects.filter(
        Q(license_plate__icontains=query) | 
        Q(town__icontains=query) | 
        Q(parking_slot__slot_number__icontains=query)
    ) if query else []

    user_results = User.objects.filter(
        Q(username__icontains=query) | 
        Q(email__icontains=query)
    ) if query else []

    # Add other models as needed

    return render(request, "dashboard/global_search.html", {
        "query": query,
        "vehicle_results": vehicle_results,
        "user_results": user_results
    })

@csrf_exempt
def initiate_payment(request):
     if request.method == "POST":
        try:
            print("Raw request body:", request.body)  # Debugging print
            data = json.loads(request.body.decode('utf-8'))  # Decode JSON properly

            phone_number = data.get("phone_number")
            amount = data.get("amount")

            if not phone_number or not amount:
                return JsonResponse({"error": "Phone number and amount are required"}, status=400)

            return JsonResponse({"success": True, "message": "STK Push request sent!"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

     return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

@csrf_exempt
def mpesa_callback(request):
    """Handle M-Pesa STK push callback"""
    if request.method == "POST":
        mpesa_response = json.loads(request.body)
        print("M-Pesa Callback:", mpesa_response)
        
        # TODO: Process the callback response and update the database
        
        return JsonResponse({"message": "Callback received"}, status=200)
    
    return JsonResponse({"error": "Invalid request"}, status=400)