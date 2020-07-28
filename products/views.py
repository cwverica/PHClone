from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Vote
from django.utils import timezone


def home(request):
    votes = Vote.objects
    products = Product.objects
    return render(request, 'products/home.html',{'products':products, 'votes':votes})


@login_required(login_url="/accounts/signup")
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['image']:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('https://') or request.POST['url'].startswith('http://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.image = request.FILES['image']
            try:
                product.icon = request.FILES['icon']
            except:
                product.icon = request.FILES['image']

            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            vote = Vote()
            vote.product_id = product
            vote.user_id = request.user
            vote.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error':'Please fill in all required fields.'})
    else:
        return render(request, 'products/create.html')


def detail(request, product_id):
    votes = Vote.objects
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product':product, 'votes':votes})


@login_required(login_url="/accounts/signup")
def upvote(request, product_id):
    if request.method == 'POST':
        voted = 0
        for each in Vote.objects:
            if each.product_id == product_id and each.user_id == request.user:
                voted = 1
        if voted == 1:
            return redirect('/products/' + str(product_id), {'error':'You cannot vote for a product more than once.'})
        elif voted == 0:
            cur_vote = Vote()
            cur_vote.product_id = product_id
            cur_vote.user_id = request.user
            cur_vote.save()
            return redirect('/products/' + str(product_id))

        # product = get_object_or_404(Product, pk=product_id)
        # product.votes_total += 1
        # product.save()

