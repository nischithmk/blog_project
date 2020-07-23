from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from blog.models import Post,Comment
from blog.forms import PostForm,CommentForm,UserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,UpdateView
                                  ,DeleteView)
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse



# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(LoginRequiredMixin,ListView):
    model =  Post
    def get_queryset(self):
        return Post.objects.filter(published_date__lte= timezone.now()).order_by('-published_date')


class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    login_required = True

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull = True).order_by('create_date')


#######################################
######################################
###################################

def LikeView(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.likes.add(request.user)
    like = Post.objects.get(pk=pk)
    total_likes = like.likes.all()
    total_likes = total_likes.count()
    return HttpResponseRedirect(reverse('post_list'))

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})



@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk = comment.post.pk)


@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)

def user_login(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)

                return HttpResponseRedirect(reverse_lazy('post_list'))
            else:
                return HttpResponse("Account not active")
        else:
            return HttpResponse('please enter login details correctly')
    else:
        return render(request,'blog/login.html',{})

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True
        else:
            print(user_form.errors)

    else:
        user_form = UserForm()

    return render(request,'blog/registration.html',{'user_form':user_form,'registered':registered})

@login_required
def user_logout(request):
    logout(request)
    return render(request,'blog/logout.html',{})


