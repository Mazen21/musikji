from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from archive.models import Instrument, Lyric, Score, MusicGenre
from django.contrib.auth import update_session_auth_hash

from django.http import HttpResponse  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
from users.tokens import account_activation_token  
from django.core.mail import EmailMessage
from directmessages.apps import Inbox
from directmessages.models import Message

def _is_password_valid(password1,password2):
    ret = 1
    if password1 != password2:
        ret = 2
    elif len(password1) < 7:
        ret = 3
    else:
        ret = 1
    return ret
    
 
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            messages.success(request,'You have successfully created your account, log in now!')
            return redirect('archive:archive_home')
    else:
        form = UserRegisterForm() 
    context = {
        'form':form,
        'page_webtitle':'Regiter',
    }
    return render(request, 'users/register.html',context)

def activate(request, uidb64, token):  
        try:  
            uid = force_text(urlsafe_base64_decode(uidb64))  
            user = User.objects.get(id=uid)  
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
            user = None  
        if user is not None and account_activation_token.check_token(user, token):  
            user.is_active = True  
            user.save()
            messages.success(request,'Thank you for your email confirmation. Now you can login your account')
            return redirect('login')
        else:
            messages.error(request,'Activation link is invalid!')
            return redirect('login')

def profile_detail(request,user_id):
    conversations = []
    us_messages = []
    unread_messages = 0
    usr = get_object_or_404(User,pk=user_id)
    instr = Instrument.objects.all()
    genres = MusicGenre.objects.all()
    usrlyrics = Lyric.objects.filter(added_by=usr)
    usrScores = Score.objects.filter(added_by=usr)

    if request.user == usr:
        contacts = Inbox.get_conversations(request.user)
        for cont in contacts:
            conversations.append(Inbox.get_conversation(request.user, cont))
        for conv in conversations:
            for msg in conv:
                us_messages.append(msg)
        us_messages.sort(key = lambda x:x.sent_at, reverse=True)
        unread_messages = len(Inbox.get_unread_messages(request.user))

    if request.method=='POST':
        if 'update_profile' in request.POST:
            usr.username = request.POST.get('username',"")
            usr.save()
            usr.profile.first_name =request.POST.get('first_name',"")
            usr.profile.last_name = request.POST.get('last_name',"")
            usr.profile.birthday = request.POST.get('birthday') or None
            usr.profile.email = request.POST.get('email',"")
            usr.profile.website = request.POST.get('website',"")
            usr.profile.about = request.POST.get('about',"")
            usr.profile.experience = request.POST.get('experience',"")
            usr.profile.city = request.POST.get('city',"")
            usr.profile.country = request.POST.get('country',"")
            usr.profile.instruments.set(request.POST.getlist('instruments',[]))
            if 'loaded_image' in request.FILES:
                usr.profile.image = request.FILES['loaded_image']
            usr.profile.save()
            messages.success(request,f'Profile updated')
        elif 'update_password' in request.POST:
            pswd1 = request.POST.get('new_password1',"")
            pswd2 = request.POST.get('new_password2',"")
            ret = _is_password_valid(pswd1,pswd2)
            if ret == 1:
                usr.set_password(request.POST.get('new_password1',""))
                update_session_auth_hash(request, usr)
                usr.save()
                messages.success(request, 'Password has been updated successfully !')
            elif ret == 2:
                messages.error(request, 'Password mismatch')     
            elif ret == 3:
                messages.error(request, 'Password is too short')
            else:      
                messages.error(request, 'Could not update password')

    context = {
        'page_webtitle' : usr.profile,
        'profile':usr.profile,
        'instruments':instr,
        'genres':genres,
        'usrLyrics':usrlyrics,
        'usrScores':usrScores,
        'us_messages' : us_messages,
        'unread_messages' : unread_messages,
    }
    return render(request, 'users/profile_detail.html', context)

@login_required
def profile(request):
    if request.method=='POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
        messages.success(request,f'Your account has been updated')
        return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)

def home(request):
    return render(request,'users/home.html')

@login_required
def send_message(request,receiver_id):
    message =""
    if request.method=='POST':
        message = request.POST.get('message', '')
        receiver = get_object_or_404(User,pk=request.POST.get('receiver', ''))
        msg_id = Inbox.send_message(request.user, receiver, message)

        current_site = get_current_site(request)
        mail_subject = 'You have received a message'
        message = render_to_string('users/send_message_mail.html', {  
            'receiver': receiver,
            'sender': request.user,
            'msg_id':msg_id[0].id,
            'domain': current_site.domain,
        })  
        to_email = receiver.email
        email = EmailMessage(  
            mail_subject, message, to=[to_email]  
        )  
        email.send()
        messages.success(request,f'Your message has been sent to {receiver.username}')
        return redirect('archive:archive_home')
    else:
        receiver = get_object_or_404(User,pk=receiver_id)
    context = {
        'receiver' : receiver,
        'message' : message,
    }
    return render(request,'users/send_message.html',context)

@login_required
def message_detail(request,msg_id):
    msg = get_object_or_404(Message,pk=msg_id)
    if not(request.user == msg.sender or request.user == msg.recipient):
        messages.error(request,"You are not allowed to view this page")
        return redirect('archive:archive_home')
    context = {
        'msg':msg,
    }
    return render(request,'users/message_detail.html',context)