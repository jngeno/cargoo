import json
from django.shortcuts import render,redirect
from django.views import View
from django.core.mail import send_mail
from .models import ServiceItem, Category, ServiceModel


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class Service(View):
    def get(self, request, *args, **kwargs):
        
        #get each item from each category
         chilled = ServiceItem.objects.filter(category__name__contains='Chilled Items')
         liquid = ServiceItem.objects.filter(category__name__contains='Liquid Bulk Cargo')
         dry = ServiceItem.objects.filter(category__name__contains='Dry Bulk Cargo')
         heavy = ServiceItem.objects.filter(category__name__contains='Machine, Equipment and Factory Parts')
         vehicles = ServiceItem.objects.filter(category__name__contains='Vehicles')
         livestock = ServiceItem.objects.filter(category__name__contains='Livestock and Animals')
         food = ServiceItem.objects.filter(category__name__contains='Food Stuff')

        #pass into context

         context = {
            'chilled': chilled,
            'liquid': liquid,
            'dry': dry,
            'heavy': heavy,
            'vehicles' : vehicles,
            'livestock' : livestock,
            'food' : food,
         }

         #render the template
         return render(request, 'customer/service.html', context)
        
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        town = request.POST.get('town')
        county = request.POST.get('county')
        number = request.POST.get('number')

        service_items = {
            'items':[]
        }

        items = request.POST.getlist('items[]')

        for item in items:
            service_item =ServiceItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': service_item.pk,
                'name': service_item.name,
                'price': service_item.price
            }

            service_items['items'].append(item_data)

            price = 0
            item_ids = []

            for item in service_items['items']:
                price += item['price']
                item_ids.append(item['id'])

            service = ServiceModel.objects.create(
                price=price,
                name=name,
                email=email,
                town=town,
                county=county,
                number=number,
            )

            service.items.add(*item_ids)

            body = ('A driver will be assigned to you shortly')

            send_mail(
                'Your Request Has Been Received',
                body,
                'example@example.com',
                [email],
                fail_silently=False
            )

            context = {
                'items': service_items['items'],
                'price': price
            }

            return redirect('service-confirmation', pk=service.pk)

            

class ServiceConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        service = ServiceModel.objects.get(pk=pk)

        context = {
            'pk': service.pk,
            'items': service.items,
            'price': service.price
        }

        return render(request, 'customer/service_confirmation.html', context)
    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            service = ServiceModel.objects.get(pk=pk)
            service.is_paid = True
            service.save()

        return redirect('payment-submitted')

class ServicePayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/service_pay_confirmation.html')
        

