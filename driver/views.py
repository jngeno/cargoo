from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from customer.models import ServiceModel


class Dashboard(UserPassesTestMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        today = datetime.today()
        services = ServiceModel.objects.filter(created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)

        unshipped_services = []
        total_revenue = 0
        for service in services: 
            total_revenue += service.price

            if not service.is_shipped:
                unshipped_services.append(service)

        context = {
            'services': unshipped_services,
            'total_revenue': total_revenue,
            'total_service': len(services),
        }

        return render(request, 'driver/dashboard.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Driver').exists()

class ServiceDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        service = ServiceModel.objects.get(pk=pk)
        context = {
            'service': service
        }

        return render(request, 'driver/service-details.html', context)

    def post(self, request, pk, *args, **kwargs):
        service = ServiceModel.objects.get(pk=pk)
        service.is_shipped = True
        service.save()

        context = {
            'service': service
        }

        return render(request, 'driver/service-details.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Driver').exists()
        

  
