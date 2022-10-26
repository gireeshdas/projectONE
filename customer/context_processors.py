from owner.models import Carts,Categories
def cart_count(request):
    cnt=Carts.objects.filter(status="in-cart").count()
    return{"cnt":cnt}


