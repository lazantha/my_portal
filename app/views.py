
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLogForm, UserRegForm, Post, ContactForm
from django.utils.cache import add_never_cache_headers
from .models import UserTable, PostTable
from django.contrib import messages
from django.db.models import Q


def signOut(request):
    request.session.pop('name', None)
    request.session.pop('email', None)
    return redirect('userLogin')


def contactUs(request):
    context = {}
    return render(request, 'blogPages/contactUs.html', context)


def aboutUs(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks For The Feedback!')
            return redirect('aboutUs')
    context = {'form': form}
    return render(request, 'blogPages/aboutUs.html', context)


def testing(request):
    url = "https://www.youtube.com/embed/ly36kn0ug4k?si=PJxpJTsH2D311M2M"
    return render(request, 'blogPages/test.html', {'url': url})


def home(request):
    posts_edu = PostTable.objects.select_related('user_id').values('user_id__name', 'topic', 'link', 'content', 'created_at').filter(category='education').order_by('created_at')
    posts_know = PostTable.objects.select_related('user_id').values('user_id__name', 'topic', 'link', 'content', 'created_at').filter(category='Knowledge').order_by('created_at')
    posts_enter = PostTable.objects.select_related('user_id').values('user_id__name', 'topic', 'link', 'content', 'created_at').filter(category='entertainment').order_by('created_at')
    posts_fitness = PostTable.objects.select_related('user_id').values('user_id__name', 'topic', 'link', 'content', 'created_at').filter(category='fitness').order_by('created_at')

    def linkFilter(dataset):
        for items in dataset:
            tokens = items['link'].split()
            if len(tokens) > 3:
                path = tokens[3]
                url_src = path.split('"')
                if len(url_src) > 1:
                    items['link'] = url_src[1]
        return dataset

    post_edu = linkFilter(posts_edu)
    post_know = linkFilter(posts_know)
    post_enter = linkFilter(posts_enter)
    post_fitness = linkFilter(posts_fitness)

    context = {
        'data_edu': post_edu,
        'data_know': post_know,
        'data_enter': post_enter,
        'data_fitness': post_fitness
    }
    return render(request, 'blogPages/index.html', context)


def adminPost(request):
    data = PostTable.objects.select_related('user_id').values('topic', 'link', 'content', 'created_at').filter(user_id__name='admin')
    context = {'data': data}
    return render(request, 'blogPages/user/adminPost.html', context)



def userLogin(request):
    # Check if the user is already logged in
    if request.session.get('email'):
        return redirect('userHome')

    form = UserLogForm()
    if request.method == 'POST':
        form = UserLogForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            request.session['name'] = name
            request.session['email'] = email

            data = UserTable.objects.filter(Q(name=name) & Q(email=email)).exists()
            if data:
                messages.success(request, 'Login Success')
                return redirect('userHome')
            else:
                messages.error(request, 'Check Username or Email')
                return redirect('userLogin')

    context = {'form': form}
    response = render(request, 'blogPages/user/userLogin.html', context)

    # Prevent back navigation from showing the login page
    add_never_cache_headers(response)
    
    return response


def userSignUp(request):
    if not request.session.get('email'):
        form = UserRegForm()
        if request.method == 'POST':
            form = UserRegForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Registration Successful')
                return redirect('userLogin')

        context = {'form': form}
        return render(request, 'blogPages/user/userReg.html', context)
    else:
        return redirect('userHome')


def userHome(request):
    if request.session.get('email'):
        dataset = PostTable.objects.values('post_id', 'topic', 'content', 'link', 'created_at').filter(
            Q(user_id__name=request.session['name']) & Q(user_id__email=request.session['email'])
        )

        for items in dataset:
            tokens = items['link'].split()
            if len(tokens) > 3:
                path = tokens[3]
                url_src = path.split('"')
                if len(url_src) > 1:
                    items['link'] = url_src[1]
        name=request.session.get('name')

        context = {'dataset': dataset,'name':name}
        return render(request, 'blogPages/user/userHome.html', context)
    else:
        return redirect('userLogin')


def delete(request, post_id):
    post = get_object_or_404(PostTable, post_id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('userHome')
    return render(request, 'blogPages/delete.html')


def update(request, post_id):
    post = get_object_or_404(PostTable, post_id=post_id)
    form = Post(request.POST or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('userHome')

    context = {'form': form}
    return render(request, 'blogPages/user/update.html', context)


def upload(request):
    if not request.session.get('email'):
        return redirect('userLogin')

    form = Post()
    if request.method == 'POST':
        form = Post(request.POST)
        if form.is_valid():
            user = UserTable.objects.filter(name=request.session['name'], email=request.session['email']).first()
            if user:
                new_post = form.save(commit=False)
                new_post.user_id = user
                new_post.save()
                messages.success(request, 'Post Uploaded!')
                return redirect('userHome')

    context = {'form': form}
    return render(request, 'blogPages/user/upload.html', context)