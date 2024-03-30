from rest_framework.exceptions import NotFound

from products.models import Product


def get_product_or_404(product_identifier: int | str) -> Product | None:
    try:
        return Product.objects.get(pk=product_identifier)
    except Exception:
        pass

    try:
        return Product.objects.get(slug=product_identifier)
    except Exception:
        pass

    raise NotFound("No %s matches the given query." % Product._meta.object_name)
