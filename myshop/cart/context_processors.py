from .cart import Cart



def cart(request):
    return {'cart': Cart(request)}

# A context processor is a function that receives the 'request' object as a parameter and returns a dictionary of objects that will be available to all the templates rendered using 'RequestContext'. In our context processor, we instantiate the cart using the 'request' object and make it available for the templates as a variable named 'cart'.