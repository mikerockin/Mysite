from django.shortcuts import render



def post_list(request):
    return render(request, 'story/post_list.html', {})


