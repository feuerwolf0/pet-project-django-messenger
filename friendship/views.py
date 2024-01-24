from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from accounts.models import Account
from friendship.models import FriendshipRequest, Friend


@login_required
def user_profile_view(request, username):
    from_user = Account.objects.get(user=request.user)
    to_user = Account.objects.get(username=username)
    frienship_request = FriendshipRequest.objects.filter(from_user=from_user, to_user=to_user).exists()
    context = {
        'account': to_user,
        'friendship_request': frienship_request
    }
    return render(request, 'friendship/user_profile.html', context)


@login_required
@require_http_methods(['POST'])
def add_friend(request):
    from_user = Account.objects.get(user=request.user)
    to_user = request.POST.get('to_user').lower().strip()
    to_user = Account.objects.get(username=to_user)

    FriendshipRequest.objects.create(from_user=from_user, to_user=to_user)
    return redirect('user_profile')


class PeopleView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'friendship/people.html'
    context_object_name = 'accounts'
    paginate_by = 20


@login_required
def myfriends_view(request):
    account = Account.objects.get(user=request.user)
    friendship_requests = FriendshipRequest.objects.filter(to_user=account)
    friends = Friend.objects.friends(account)
    context = {
        'account': account,
        'friendship_requests': friendship_requests,
        'friends': friends
    }
    return render(request, 'friendship/myfriends.html', context)
