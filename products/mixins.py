from django.http import Http404
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404


class MultipleFieldLookupMixin:
    def get_object(self):
        # Get the base queryset
        queryset = self.get_queryset()

        # Get the lookup fields. If not defined, default to ['id']
        lookup_fields = getattr(self, "lookup_fields", ["id"])

        for field in lookup_fields:
            try:
                # Try to filter the queryset based on the lookup field
                filter_kwargs = {field: self.kwargs[self.lookup_field]}
                obj = get_object_or_404(queryset, **filter_kwargs)

                # Check if the request has the necessary permissions
                self.check_object_permissions(self.request, obj)
                return obj

            except Http404:
                # If the object is not found, continue to the next lookup field
                continue

        # If no object is found after checking all lookup fields, raise a NotFound exception
        raise NotFound(
            "No %s matches the given query." % queryset.model._meta.object_name
        )
