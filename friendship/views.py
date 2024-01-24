from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from accounts.models import Account
from friendship.exceptions import FriendsDoesNotExist
from friendship.models import FriendshipRequest, Friend


@login_required
def user_profile_view(request, username):
    owner = Account.objects.get(user=request.user)
    profile = Account.objects.get(username=username)
    incoming_friend_requests = FriendshipRequest.objects.filter(from_user=profile,
                                                                to_user=owner,
                                                                rejected_at__isnull=True)
    outgoing_friend_requests = FriendshipRequest.objects.filter(from_user=owner,
                                                                to_user=profile)

    in_friends = Friend.objects.is_friends(owner, profile)

    context = {
        'account': profile,
        'incoming_request': incoming_friend_requests,
        'outgoing_request': outgoing_friend_requests,
        'in_friends': in_friends
    }
    return render(request, 'friendship/user_profile.html', context)


class PeopleView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'friendship/people.html'
    context_object_name = 'accounts'
    paginate_by = 20


@login_required
def myfriends_view(request):
    account = Account.objects.get(user=request.user)
    friendship_requests = FriendshipRequest.objects.prefetch_related('from_user').filter(to_user=account)
    friends = Friend.objects.friends(account)
    context = {
        'account': account,
        'friendship_requests': friendship_requests,
        'friends': friends
    }
    return render(request, 'friendship/myfriends.html', context)


@login_required
@require_http_methods(['POST'])
def add_friend(request):
    owner = Account.objects.get(user=request.user)
    profile = request.POST.get('to_user').lower().strip()
    profile = Account.objects.get(username=profile)

    cur_requests = FriendshipRequest.objects.filter(from_user=profile, to_user=owner)

    if cur_requests:
        cur_requests[0].accept()
    else:
        FriendshipRequest.objects.create(from_user=owner, to_user=profile)

    return redirect('user_profile', username=profile.username)


@login_required
@require_http_methods(['POST'])
def accept_friendship(request):
    owner = Account.objects.get(user=request.user)
    profile = request.POST.get('to_user').lower().strip()
    profile = Account.objects.get(username=profile)
    try:
        friendship_request = FriendshipRequest.objects.get(from_user=profile, to_user=owner)
        friendship_request.accept()
    except FriendshipRequest.DoesNotExist:
        messages.error(request, 'Заявка в друзья не найдена')

    if request.POST.get('myfriends'):
        return redirect('myfriends')

    return redirect('user_profile', username=profile.username)


@login_required
@require_http_methods(['POST'])
def reject_friendship(request):
    owner = Account.objects.get(user=request.user)
    profile = request.POST.get('to_user').lower().strip()
    profile = Account.objects.get(username=profile)
    try:
        friendship_request = FriendshipRequest.objects.get(from_user=profile, to_user=owner)
        friendship_request.reject()
    except FriendshipRequest.DoesNotExist:
        messages.error(request, 'Заявка в друзья не найдена')

    return redirect('user_profile', username=profile.username)


@login_required
@require_http_methods(['POST'])
def cancel_friendship(request):
    owner = Account.objects.get(user=request.user)
    profile = request.POST.get('to_user').lower().strip()
    profile = Account.objects.get(username=profile)
    try:
        friendship_request = FriendshipRequest.objects.get(from_user=owner, to_user=profile)
        friendship_request.cancel()
    except FriendshipRequest.DoesNotExist:
        messages.error(request, 'Заявка в друзья не найдена')

    return redirect('user_profile', username=profile.username)


@login_required
@require_http_methods(['POST'])
def delete_friend(request):
    owner = Account.objects.get(user=request.user)
    profile = request.POST.get('to_user').lower().strip()
    profile = Account.objects.get(username=profile)

    try:
        Friend.objects.delete_friend(owner, profile)
    except FriendsDoesNotExist:
        messages.error(request, "Друзья не найдены")
    return redirect('user_profile', username=profile.username)
