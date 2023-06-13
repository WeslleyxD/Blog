from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, User
from .forms import EmailPostForm, CommentForm, PostForm
from django.core.mail import send_mail
import random
from django.core.paginator import Paginator
from django.db.models import Q



def post_detail(request, post):
    post = get_object_or_404(Post, slug=post, status='published')
    slug = post.slug


    # List of active comments for this post
    comments = post.comment_set.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database


            new_comment.save()

            return redirect(f'/{slug}')
    else:
        comment_form = CommentForm()

    paginator = Paginator(comments, 5) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
       
    # List of similar posts
    similar_posts = Post.published.exclude(id=post.id)
   

    return render(request, 'detail.html',
                {
                    'post': post, 
                    'new_comment': new_comment, 
                    'comments': comments, 
                    'comment_form': comment_form, 
                    'similar_posts': similar_posts,
                    'page_obj': page_obj,
                })


def post_share(request, post_slug):
    # Retrieve post by id
    post = get_object_or_404(Post, slug=post_slug, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        share_form = EmailPostForm(request.POST)

        if share_form.is_valid():
             # Form fields passed validation
            cd = share_form.cleaned_data

            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recomendou você ler {post.title}"
            message = f"Leia {post.title} no link {post_url}\n\n" \
                      f"Comentário de '{cd['name']}': {cd['comments'].title()}"
            send_mail(subject, message, cd['to'], ['projetodjango123@gmail.com'])
            sent = True
            # ... send email

    else:
        share_form = EmailPostForm()

    return render(request, 'share.html', 
                {
                    'post': post, 
                    'share_form': share_form, 
                    'sent': sent,                            
                })


def post_list(request, tag_slug=None):

    post_list = (Post.published.all())
    post_list_id = [x.id for x in post_list]
    post_random_id = random.sample(post_list_id, len(post_list_id))

    post_list_random = [Post.published.get(id=x) for x in post_random_id]
    random_posts = post_list_random[2::]

    post_last = None
    if post_list:
        post_last = post_list.latest('created_date','created_time')

    post_list_tag = None
    selected_tag = None

    if tag_slug:
        post_list_tag = post_list.filter(tag=tag_slug)
        selected_tag = tag_slug
        


    return render(request,'list.html',
                {
                    'selected_tag' : selected_tag,
                    'post_list_tag': post_list_tag,
                    'post_list_random': post_list_random,
                    'post_last': post_last,
                    'random_posts': random_posts,            
                })




def post_search(request):
    #Não precisa de render no method GET pelo fato que o input sempre vai ser POST
    
    list_query = None

    #O FORM AQUI FOI COM O .GET PORQUE NÃO TEM UM FORM NO FORM.PY PRA USAR O CLEANED_DATA
    if request.method == 'POST':
        search_form = request.POST.get('search')
        list_query = Post.published.filter(Q(body__icontains=search_form) | Q(title__icontains=search_form) )
        return render(request, 'search.html', 
                        {
                            'list_query' : list_query
                        })



def post_publication(request):
    post_form = PostForm()   

    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            post_form.save()
            
            return redirect(f'/')
            

    return render (request, 'publication.html',
                    {
                        'post_form' : post_form,
                    })

