from django.views.generic.edit import CreateView
from .forms import OrderForm

class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm