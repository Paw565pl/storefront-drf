from rest_framework.exceptions import NotFound

from products.models import Product


def get_product_or_404(product_identifier: int | str) -> Product:
    try:
        return Product.objects.get(pk=product_identifier)
    except (Product.DoesNotExist, ValueError):
        pass

    try:
        return Product.objects.get(slug=product_identifier)
    except (Product.DoesNotExist, ValueError):
        pass

    raise NotFound("No %s matches the given query." % Product._meta.object_name)
