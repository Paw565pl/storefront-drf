from rest_framework.generics import get_object_or_404, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated

from orders.models import CustomerAddress
from orders.serializers import CustomerAddressSerializer


# Create your views here.
class CustomerAddressView(CreateModelMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomerAddress.objects.filter(customer__user_id=self.request.user.id)

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), customer__user_id=self.request.user.id
        )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
