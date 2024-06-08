from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Post, Comment
from .forms import SignUpForm, AuthorizeForm, ContactForm,CommentForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect,HttpResponse
from django.core.paginator import Paginator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from taggit.models import Tag


class MainView(View):
    def get(self,request,*args,**kwargs):
        posts = Post.objects.all().order_by('-created_at')
        paginator = Paginator(posts, 6)

        page_number = request.GET.get('page')
        obj_pag = paginator.get_page(page_number)

        return render(
            request,
            'my_blog/index.html',
            context={'obj_pag':obj_pag}
        )


class PostDetailView(View):
    def get(self, request, slug, *args,**kwargs):
        post = get_object_or_404(Post, url=slug)

        common_tag = Post.tag.all
        last_posts = Post.objects.all().order_by('-created_at')[:5]
        comment_form = CommentForm()

        return render(request,
            'my_blog/post.html',context = {'post':post,'last_posts':last_posts,'common_tag':common_tag, 'comment_form':comment_form}
        )
    def post(self,request,slug,*args,**kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            username = self.request.user
            text = request.POST['text']
            post = get_object_or_404(Post, url=slug)
            Comment.objects.create(post=post,username=username,text=text)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request,
            'my_blog/post.html',context = {'comment_form':comment_form}
            )



class SignUp(View):
    def get(self,request,*args,**kwargs):
        form = SignUpForm()
        return render(
            request,
            'my_blog/signup.html',
            context={
                'form':form
            }
        )
    def post(self,request,*args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/')
        return render(request, 'myblog/signup.html', context={
        'form': form,
    })

class Authorize(View):

    def get (self,request,*args,**kwargs):
        form = AuthorizeForm()
        return render(
            request,'my_blog/authorize.html',context={'form':form}
        )

    def post(self, request, *args, **kwargs):
        form = AuthorizeForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = AuthorizeForm(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                form.add_error(None, "Неправильный пароль или указанная учётная запись не существует!")
                return render(request, "my_blog/authorize.html", {"form": form})
        return render(request, 'my_blog/authorize.html', context={
            'form': form,
        })

class Contact(View):

    def get(self,request,*args,**kwargs):
        form = ContactForm()
        return render(
            request,'my_blog/contact.html',context={'form':form}
        )

    def post(self,request,*args,**kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            email = form.cleaned_data['email']
            subject  = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'От {name} | {email} ', subject, message, ['pervakovilia300@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')

            return HttpResponseRedirect('success')


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'my_blog/success.html', context={
            'title': 'Спасибо'
        })


class SearchView(View):

    def get(self,request,*args,**kwargs):
        query = request.GET.get('q')
        results = ""
        if query:
            results = Post.objects.filter(
                Q(h1__icontains=query) | Q(content__icontains=query)
            )
        paginator = Paginator(results,6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'my_blog/search.html', context={
            'title': 'Поиск',
            'results': page_obj,
            'count': paginator.count
        })


class TagView(View):
    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tag=tag)
        common_tags = Post.tag.most_common()
        return render(request, 'my_blog/tag.html', context={
            'title': f'#ТЕГ {tag}',
            'posts': posts,
            'common_tags': common_tags
        })
