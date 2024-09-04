from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserLogForm,UserRegForm,Post,ContactForm
from .models import UserTable,PostTable
from django.contrib import messages
from django.db.models import Q


def signOut(request):

	request.session.pop('name',None)
	request.session.pop('email',None)
	return redirect('userLogin')
	
def contactUs(request):
	
	context={}
	return render(request,'blogPages/contactUs.html',context)



def aboutUs(request):
	form=ContactForm()
	if request.method=='POST':
		form=ContactForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success('Thanks For The FeedBack !')
			return redirect('aboutUs')
	context={'form':form}
	return render(request,'blogPages/aboutUs.html',context)

def testing(request):

	url="https://www.youtube.com/embed/ly36kn0ug4k?si=PJxpJTsH2D311M2M"
	
	return render(request,'blogPages/test.html',{'url':url})

def home(request):

	posts_edu = PostTable.objects.select_related('user_id').values('user_id__name', 'topic', 'link', 'content','created_at').filter(category='education').order_by('created_at')
	posts_know = PostTable.objects.select_related('user_id').values('user_id__name', 'topic', 'link', 'content','created_at').filter(category='Knowledge').order_by('created_at')
	posts_enter = PostTable.objects.select_related('user_id').values('user_id__name', 'topic', 'link', 'content','created_at').filter(category='entertainment').order_by('created_at')
	posts_fitness = PostTable.objects.select_related('user_id').values('user_id__name', 'topic', 'link', 'content','created_at').filter(category='fitness').order_by('created_at')
	def linkFilter(dataset):
		for items in dataset:
			tokens=items['link'].split()
			path=(tokens[3])
			url_src=path.split('"')
			items['link']=url_src[1]
			return dataset
	post_edu=linkFilter(posts_edu)
	post_know=linkFilter(posts_know)
	post_enter=linkFilter(posts_enter)
	post_fitness=linkFilter(posts_fitness)
	context={'data_edu':post_edu,'data_know':post_know,'data_enter':post_enter,'data_fitness':post_fitness}
	return render(request,'blogPages/index.html',context)



def adminPost(request):
	data=PostTable.objects.select_related('user_id').values('topic','link','content','created_at').filter(user_id__name='admin')
	context={'data':data}
	return render(request,'blogPages/user/adminPost.html',context)


def userLogin(request):
	form=UserLogForm()
	if request.method=='POST':
		form=UserLogForm(request.POST)
		if form.is_valid():
			name=form.cleaned_data['name']
			email=form.cleaned_data['email']
			request.session['name']=name
			request.session['email']=email
			print("session has been set")
			#database
			model=UserTable
			data=model.objects.values('name','email').filter(Q(name=name)and Q(email=email))
			if data:
				request.session['name']=name
				request.session['email']=email
				context={'name':name}
				messages.success(request,'Login Success')
				return redirect('userHome',context)
			else:
				messages.success(request,'Check User Name Or Email ')
				return redirect('userLogin')
				print("Not exist")
			
	context={'form':form}
	return render(request,'blogPages/user/userLogin.html',context)



def userSignUp(request):
	name = request.session.get('name')
	email=request.session.get('email')
	if not email:
		form=UserRegForm()
		if request.method=='POST':
			form=UserRegForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request,'Success')
				return redirect('userLogin')
	else:
		return render(request,'blogPages/user/userHome.html')
		
	context={'form':form}
	return render(request,'blogPages/user/userReg.html',context)


def userHome(request):
	name = request.session.get('name')
	email=request.session.get('email')
	if email:
		model=PostTable
		name=request.session.get('name')
		email=request.session.get('email')
		dataset = model.objects.values('post_id', 'topic', 'content', 'link','created_at').filter(Q(user_id__name=name) & Q(user_id__email=email))
		for items in dataset:
			tokens=items['link'].split()
			path=(tokens[3])
			url_src=path.split('"')
			items['link']=url_src[1]
		
		context={'dataset':dataset}
		return render(request,'blogPages/user/userHome.html',context)
	else:
		return render(request,'blogPages/user/userLogin.html')



def delete(request,post_id):

	post=get_object_or_404(PostTable,post_id=post_id)
	if request.method=='POST':
		post.delete()
		return redirect('userHome')
	return render(request,'blogPages/delete.html')



# define another class to update post table with cusomized fields
#this is for all the field to update

def update(request,post_id):
	post=get_object_or_404(PostTable,post_id=post_id)
	if request.method=='POST':
		form=Post(request.POST,instance=post)
		if form.is_valid():
			form.save()
			return redirect('userHome')
	context={'form':form}
	return render(request,'blogPages/user/update.html',context)


def upload(request):
	name=request.session.get('name')
	email=request.session.get('email')
	form=Post()
	if request.method=='POST':
		form=Post(request.POST)
		if form.is_valid():
			# user_id=UserTable.objects.values('id').filter(Q(name=name)and Q(email=email))
			user = UserTable.objects.filter(name=name, email=email).first()
			if user:
				new_post=form.save(commit=False)
				new_post.user_id=user
				new_post.save()
				messages.success(request,'Post Uploaded !')
				return redirect('userHome')
	context={'form':form}
	return render(request,'blogPages/user/upload.html',context)

