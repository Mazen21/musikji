from archive.models import *
from archive.forms import SongForm, LyricForm, ScoreForm, ArtistForm, CommentForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import os
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from backoffice.models import *

def _update_song_active_state(song,state):
    for score in song.score_set.all():
        score.is_active = state
        score.save()
    for lyric in song.lyric_set.all():
        lyric.is_active = state
        lyric.save()
    song.is_active = state
    song.save()

def _update_artist_active_state(artist,state):
    for song in artist.song_set.all():
        _update_song_active_state(song,state)
    artist.is_active = state
    artist.save()

def _update_musikji_points(request,context):
    if context == 'download_score':
        if (request.user.profile.points - settings.DOWNLOAD_SCORE_POINTS) < 0 :
            return False
        else:
            request.user.profile.points -= settings.DOWNLOAD_SCORE_POINTS
            request.user.save()
            return True
    else:
        return False

@login_required
def _update_rank(request,elem,impre):
    user_vote = elem.votes.filter(user=request.user)
    if user_vote.count() == 1:
        v = user_vote.first()
        if v.value != impre:  
            v.delete()
            v2 = Vote(user=request.user,value=impre)
            v2.save()
            elem.votes.add(v2)
            elem.save()
    elif user_vote.count() == 0:
        v = Vote(user=request.user,value=impre)
        v.save()
        elem.votes.add(v)
        elem.save()
    else:
        for v in user_vote:
            v.delete()
        
        v = Vote(user=request.user,value=impre)
        v.save()
        elem.votes.add(v)
        elem.save()
    elem.upvotes = elem.votes.filter(value=True).count()
    elem.downvotes = elem.votes.filter(value=False).count()
    elem.rank = elem.upvotes - elem.downvotes

    if elem.upvotes == elem.downvotes:
        elem.rate = 2
    else :
        elem.rate = int(round(2 + 2 * ((elem.upvotes - elem.downvotes)//elem.votes.all().count())))
    elem.save()

def home(request):
    context = {
        'page_webtitle':"Musikji",
    }
    return render(request,'archive/home.html',context)

def archive_home(request):
    context = {
        'page_webtitle':"Musikji",
    }
    return render(request, 'archive/home.html', context)

def instrument_home(request):
    instruments = Instrument.objects.all()
    context = {
        "page_title":"Instruments list",
        "page_webtitle":"Instruments list",
        "instruments":instruments,
    }
    return render(request, 'archive/instrument.html', context)

def instrument_detail(request,instr_id):
    instruments = Instrument.objects.all()
    instrument = get_object_or_404(Instrument,pk=instr_id)
    context = {
        "page_title": instrument.title_eng,
        "instruments": instruments,
        "instrument": instrument,
    }
    return render(request, 'archive/instrument_detail.html',context)

def maqam_home(request):
    maqams = Maqam.objects.all()
    context = {
        "page_title": "Maquam list",
        'maqams' : maqams,
    }
    return render(request,'archive/maqam.html', context)

def maqam_detail(request,maqam_id):
    maqams = Maqam.objects.all()
    maqam = get_object_or_404(Maqam,pk=maqam_id)
    context = {
        "page_title": maqam.title_eng,
        "maqams": maqams,
        "maqam": maqam,
    }
    return render(request, 'archive/maqam_detail.html', context)

def rythm_home(request):
    rythms = Rythm.objects.all()
    context = {
        "page_title": "Rythm list",
        'rythms' : rythms,
    }
    return render(request,'archive/rythm.html', context)

def rythm_detail(request,rythm_id):
    rythms = Rythm.objects.all()
    rythm = get_object_or_404(Rythm,pk=rythm_id)
    context = {
        "page_title": rythm.title_eng,
        "rythms": rythms,
        "rythm": rythm,
    }
    return render(request, 'archive/rythm_detail.html', context)

def jins_home(request):
    jinss = Jins.objects.all()
    context = {
        "page_title": "Jins list",
        'jinss' : jinss,
    }
    return render(request,'archive/jins.html', context)

def jins_detail(request,jins_id):
    jinss = Jins.objects.all()
    jins = get_object_or_404(Jins,pk=jins_id)
    context = {
        "page_title": jins.title_eng,
        "jinss": jinss,
        "jins": jins,
    }
    return render(request, 'archive/jins_detail.html', context)

def musicForm_home(request):
    musicforms = MusicForm.objects.all()
    context = {
        "page_title": "Music form list",
        'musicforms' : musicforms,
    }
    return render(request,'archive/musicforms.html', context)

def musicForm_detail(request,musicForm_id):
    musicforms = MusicForm.objects.all()
    musicform = get_object_or_404(MusicForm,pk=musicForm_id)
    context = {
        "page_title": musicform.title_eng,
        "musicforms": musicforms,
        "musicform": musicform,
    }
    return render(request, 'archive/musicforms_detail.html', context)

def artist_home(request):
    artist_search=""
    artist_country=""
    artist_music_genre=0
    artist_artist_type=0

    artists = Artist.objects.filter(is_active=True).order_by('name_eng')
    if request.method == 'POST':
        if 'search' in request.POST:
            artists = artists.filter(name_eng__icontains=request.POST.get('search',""))
            artist_search=request.POST['search']
        if 'country' in request.POST:
            artists = artists.filter(country=request.POST['country'])
            artist_country=request.POST['country']
        if 'music_genre' in request.POST:
            artists = artists.filter(music_genre=request.POST['music_genre'])
            artist_music_genre=int(request.POST['music_genre'])
        if 'artist_type' in request.POST:
            artists = artists.filter(artist_type=request.POST['artist_type'])
            artist_artist_type=int(request.POST['artist_type'])

    artist_paginator = Paginator(artists, 12) # Show 12 artist per page
    page_number = request.GET.get('page')
    page_obj = artist_paginator.get_page(page_number)

    context = {
        'page_title': "Artists",
        'page_webtitle': "Artists",
        'artist_search':artist_search,
        'artist_country':artist_country,
        'artist_music_genre':artist_music_genre,
        'artist_artist_type':artist_artist_type,
        'artists': artists,
        'page_obj': page_obj,
    }
    return render(request,'archive/artists.html', context)

def artist_detail(request,artist_id):
    artist = get_object_or_404(Artist,pk=artist_id)
    if ((artist.is_active == False) and ((request.user.profile.role != 'moderator') and (request.user != artist.added_by))):
        messages.error(request,'This element is waiting for administration approval !')
        return redirect('archive:archive_home')
    if artist.is_active == False and request.user == artist.added_by:
        messages.warning(request,'This element is not public yet, only you can visualize it!')

    songs = Song.objects.filter(artists=artist)
    if request.method=="POST":
        if 'upvote' in request.POST:
            _update_rank(request,artist,True)
        elif 'downvote' in request.POST:
            _update_rank(request,artist,False)
        elif 'deactive' in request.POST:
            _update_artist_active_state(artist,False)
        elif 'active' in request.POST:
            _update_artist_active_state(artist,True)
    context = {
        'page_title' : artist.name_eng,
        'page_webtitle' : artist.name_eng,
        'artist' : artist,
        'empty_stars': 4-artist.rate,
        'songs' : songs,
    }
    return render(request, 'archive/artist_detail.html', context)

def artist_fl(request, key_l):
    artist_search=""
    artist_country=""
    artist_music_genre=0
    artist_artist_type=0

    artists_l = Artist.objects.filter(name_eng__startswith=key_l, is_active=True).order_by('name_eng')
    if request.method == 'POST':
        if 'search' in request.POST:
            artists_l = artists_l.filter(name_eng__icontains=request.POST.get('search',""))
            artist_search=request.POST['search']
        if 'country' in request.POST:
            artists_l = artists_l.filter(country=request.POST['country'])
            artist_country=request.POST['country']
        if 'music_genre' in request.POST:
            artists_l = artists_l.filter(music_genre=request.POST['music_genre'])
            artist_music_genre=int(request.POST['music_genre'])
        if 'artist_type' in request.POST:
            artists_l = artists_l.filter(artist_type=request.POST['artist_type'])
            artist_artist_type=int(request.POST['artist_type'])

    artist_paginator = Paginator(artists_l, 12) # Show 12 artist per page
    page_number = request.GET.get('page')
    page_obj = artist_paginator.get_page(page_number)

    context = {
        'page_title':"Artists",
        'artist_search':artist_search,
        'artist_country':artist_country,
        'artist_music_genre':artist_music_genre,
        'artist_artist_type':artist_artist_type,
        'artists_l':artists_l,
        'page_obj': page_obj,
    }
    return render(request, 'archive/artists.html', context)

@login_required
def artist_add(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            artist = form.save()
            artist.added_by = request.user
            if request.user.profile.role == 'moderator':
                artist.is_active = True
            else:
                tk = Ticket(usr_creator = request.user,
                            tag='add artist',
                            message='add artist',
                            link=f'http://localhost:8000/archive/artist/{artist.id}'
                            )
                tk.save()
            request.user.profile.points += 50
            request.user.profile.save()
            artist.save()
            messages.success(request,f'artist added')
            return redirect('archive:artist_detail',artist_id=artist.id)
    else:
        form = ArtistForm()
    context = {
        'form': form,
        'page_title' : "Add artist",
        'page_webtitle' : "Add artist",
    }
    return render(request, 'archive/artist_add.html', context)

def song_home(request):
    song_search=""
    song_artist=0
    song_rythm=0
    song_maqam=0
    song_music_form=0
    with_scores=False
    with_lyrics=False

    songs = Song.objects.filter(is_active=True).order_by('name_eng')
    if request.method == 'POST':
        if 'song_search' in request.POST:
            songs = songs.filter(name_eng__icontains=request.POST['song_search'])
            song_search= request.POST['song_search']
        if 'song_artist' in request.POST:
            songs = songs.filter(artists=request.POST['song_artist'])
            song_artist = int(request.POST['song_artist'])
        if 'song_rythm' in request.POST:
            songs = songs.filter(rythm=request.POST['song_rythm'])
            song_rythm = int(request.POST['song_rythm'])
        if 'song_maqam' in request.POST:
            songs = songs.filter(maqam=request.POST['song_maqam'])
            song_maqam = int(request.POST['song_maqam'])
        if 'song_music_form' in request.POST:
            songs = songs.filter(music_form=request.POST['song_music_form'])
            song_music_form = int(request.POST['song_music_form'])
        if 'with_scores' in request.POST:
            songs = songs.exclude(score=None)
            with_scores = True
        if 'with_lyrics' in request.POST:
            songs = songs.exclude(lyric=None)
            with_lyrics = True

    artist_paginator = Paginator(songs, 10)
    page_number = request.GET.get('page')
    page_obj = artist_paginator.get_page(page_number)
    context = {
        'page_title':"Songs",
        'page_webtitle':"Songs",
        'song_search':song_search,
        'song_artist':song_artist,
        'song_rythm':song_rythm,
        'song_maqam':song_maqam,
        'song_music_form':song_music_form,
        'song_with_scores':with_scores,
        'song_with_lyrics':with_lyrics,
        'page_obj': page_obj,
    }
    return render(request, 'archive/song.html',context)

def song_detail(request, song_id):
    context = {}
    song = get_object_or_404(Song, pk=song_id)
    if ((song.is_active == False) and ((request.user.profile.role != 'moderator') and (request.user != song.added_by))):
        messages.error(request,'This element is waiting for administration approval !')
        return redirect('archive:archive_home')
    if song.is_active == False and request.user == song.added_by:
        messages.warning(request,'This element is not public yet, only you can visualize it!')

    comments = song.comments.filter(active=True)
    if request.method == 'POST':
        if 'upvote' in request.POST:
            _update_rank(request,song,True)
        elif 'downvote' in request.POST:
            _update_rank(request,song,False)
        elif 'deactive' in request.POST:
            _update_song_active_state(song,False)
        elif 'active' in request.POST:
            _update_song_active_state(song,True)
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = song
                new_comment.added_by = request.user
                new_comment.save()
                comment_form = CommentForm()
            else:
                comment_form = CommentForm()
            context['comment_form'] = comment_form

    context.update({
        'page_title':song.name_eng,
        'page_webtitle':song.name_eng,
        'song': song,
        'comments':comments,
        'empty_stars': 4-song.rate,
    })
    return render(request, 'archive/song_detail.html', context)

def song_search(request):
    songs = Song.objects.filter(name_eng__icontains=request.POST['search'])
    context = {
        'page_title':"Search songs",
        'songs': songs,
    }
    return render(request, 'archive/song_search.html',context)

@login_required
def song_add(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            song = form.save()
            song.added_by= request.user
            if request.user.profile.role == 'moderator':
                song.is_active = True
            else:
                tk = Ticket(usr_creator = request.user,
                            tag='add song',
                            message='add song',
                            link=f'http://localhost:8000/archive/song/{song.id}'
                            )
                tk.save()
            request.user.profile.points += 50
            request.user.profile.save()
            song.save()
            messages.success(request,f'Song added successfully!')
            return redirect('archive:song_detail', song_id=song.id)
    else:
        form = SongForm()
    context = {
        'form':form,
        'page_title':"Add song",
        'page_webtitle':"Add song",
    }
    return render(request,'archive/song_add.html', context)


def lyric_home(request):
    context={
        "page_title":"Lyrics",
    }
    return render(request, 'archive/lyric.html',context)

def lyric_detail(request,lyric_id):
    lyric = get_object_or_404(Lyric,pk=lyric_id)
    if ((lyric.is_active == False) and ((request.user.profile.role != 'moderator') and (request.user != lyric.added_by))):
        messages.error(request,'This element is waiting for administration approval !')
        return redirect('archive:archive_home')
    if lyric.is_active == False and request.user == lyric.added_by:
        messages.warning(request,'This element is not public yet, only you can visualize it!')
    if request.method=="POST":
        if 'upvote' in request.POST:
            _update_rank(request,lyric,True)
        elif 'downvote' in request.POST:
            _update_rank(request,lyric,False)
        elif 'deactive' in request.POST:
            lyric.is_active = False
            lyric.save()
        elif 'active' in request.POST:
            lyric.is_active = True
            lyric.save()
    context = {
        'empty_stars': 4-lyric.rate,
        'page_webtitle':lyric.song.name_eng,
        'page_title':"lyric " + lyric.song.name_eng,
        'page_webtitle':"lyric " + lyric.song.name_eng,
        'lyric':lyric
    }
    return render(request,'archive/lyric_detail.html',context)

@login_required
def lyric_add(request, song_id):
    if request.method == 'POST':
        form = LyricForm(request.POST)
        if form.is_valid():
            lyric = form.save()
            lyric.added_by = request.user
            lyric.save()
            if request.user.profile.role == 'moderator':
                lyric.is_active = True
            else:
                tk = Ticket(usr_creator = request.user,
                            tag='add lyric',
                            message='add lyric',
                            link=f'http://localhost:8000/archive/lyrics/{lyric.id}'
                            )
                tk.save()
            messages.success(request,f'Lyrics added')
            request.user.profile.points += 50
            request.user.profile.save()
            lyric.save()
        return redirect('archive:song_detail',song_id=song_id )
    else:
        song = get_object_or_404(Song,pk=song_id)
        lyric = Lyric()
        lyric.song = song
        form = LyricForm(instance = lyric)
    context = {
        'form':form,
        'page_title':'Add lyric',
    }
    return render(request,'archive/lyric_add.html',context)

@login_required
def score_add(request, song_id):
    if request.method == 'POST':
        form = ScoreForm(request.POST, request.FILES)
        if form.is_valid():
            score = form.save()
            score.added_by = request.user
            score.save()
            if request.user.profile.role == 'moderator':
                score.is_active = True
            else:
                tk = Ticket(usr_creator = request.user,
                            tag='add score',
                            message='add score',
                            link=f'http://localhost:8000/archive/scores/{score.id}'
                            )
                tk.save()
            request.user.profile.points += 50
            request.user.profile.save()
            messages.success(request,f'score added')
            score.save()
            return redirect('archive:song_detail',song_id=song_id)
        else:
            return render(request,'archive/score_add.html',{'form':form})
    else:
        song = get_object_or_404(Song,pk=song_id)
        score = Score()
        score.song = song
        form = ScoreForm(instance = score)
    context = {
        'form':form,
        'page_title':"Add score",
    }
    return render(request,'archive/score_add.html',context)

def score_home(request):
    context = {
        'page_title': 'Scores',
    }
    return render(request, 'archive/score_home.html', context)

def score_detail(request, score_id):
    score = get_object_or_404(Score, pk=score_id)
    user = request.user

    if ((score.is_active == False) and ((request.user.profile.role != 'moderator') and (request.user != score.added_by))):
        messages.error(request,'This element is waiting for administration approval !')
        return redirect('archive:archive_home')
    if score.is_active == False and request.user == score.added_by:
        messages.warning(request,'This element is not public yet, only you can visualize it!')
    if request.method=="POST":
        if 'upvote' in request.POST:
            _update_rank(request,score,True)
        elif 'downvote' in request.POST:
            _update_rank(request,score,False)
        elif 'deactive' in request.POST:
            score.is_active = False
            score.save()
        elif 'active' in request.POST:
            score.is_active = True
            score.save()
    context = {
        'empty_stars': 4-score.rate,
        'score':score,
        'is_favorit':False,
        'page_webtitle':"Score " + score.song.name_eng,
        'page_title':"Score " + score.song.name_eng,
    }
    if request.user.is_authenticated and score in user.profile.favorit_scores.all():
        context['is_favorit'] = True
    if request.method == 'POST':
        user.profile.favorit_scores.add(score)
        context['is_favorit'] = True
    return render(request, 'archive/score_detail.html', context)

@login_required
def score_download(request, score_id):
    if _update_musikji_points(request,'download_score'):
        score = get_object_or_404(Score,pk=score_id)
        file_path = os.path.join(settings.MEDIA_ROOT, score.score.path)
        if (os.path.exists(file_path)):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'attachement; filename=' + os.path.basename(file_path)
                #increment number of downloads
                score.downloads += 1
                score.save()
                if request.user.profile.points >= 10: 
                    request.user.profile.points -= 10
                    request.user.profile.save()
                    return response
                else:
                    messages.error(request,'You have reached maximum number of downloads, Contribute to musikji in order to gain points ' )
                    return redirect('archive:archive_home')
        raise Http404
    else:
        messages.error(request,f'Not enough musikji points')
        score = get_object_or_404(Score, pk=score_id)
        user = request.user
        context = {
            'score':score,
            'is_favorit':False,
            'page_webtitle':"Score " + score.song.name_eng,
            'page_title':"Score " + score.song.name_eng,
        }
        if request.user.is_authenticated and score in user.profile.favorit_scores.all():
            context['is_favorit'] = True
        if request.method == 'POST':
            user.profile.favorit_scores.add(score)
            context['is_favorit'] = True
        return render(request, 'archive/score_detail.html', context)

def archive_search(request):
    # search artists, songs, archive, users,
    search_text = request.GET.get('search_text','')
    artists = []
    songs = []
    users = []
    if search_text != '':
        artists = Artist.objects.filter(name_eng__icontains=search_text)
        songs = Song.objects.filter(name_eng__icontains=search_text)
        users = User.objects.filter(username__icontains=search_text)
    context = {
        'page_webtitle':"Search results",
        'search_text':search_text,
        'artists_results':artists,
        'songs_results':songs,
        'users_results':users,
    }
    return render(request,'archive/home_search.html',context)

def wiki_home(request):
    context = {
        'page_webtitle' : "Wiki",
        'page_title' : "Wiki",
    }
    return render(request,'archive/wiki_home.html',context)

def wiki_no_element(request):
    context = {
        'page_webtitle': "No element",
    }
    return render(request,'archive/no_element.html',context)

def contact(request):
    if request.method == 'POST':
        contact_ticket = Ticket()
        name = request.POST.get('txtName','')
        if request.user.is_authenticated:
            name += '(' +request.user.username +')'
            contact_ticket.usr_creator = request.user
        else:
            contact_ticket.usr_creator = User.objects.filter(username="admin").first()
        email = request.POST.get('txtEmail','')
        phone = request.POST.get('txtPhone','')
        text_message = request.POST.get('txtMsg','')
        contact_ticket.message = f'<h3>{name}</h3></br>{email}</br>{phone}</br>***********</br><p>{text_message}<p>\n'
        contact_ticket.tag = 'contact'
        contact_ticket.save()
        messages.success(request,f'Your request has been saved correctly, we will go back to you shortly!')
        return redirect('archive:archive_home')
        
    context = {
        'page_webtitle': 'Contact us',
    }
    return render(request,'archive/contact_us.html',context)

@login_required
def report_error(request):
    link = ''
    if request.method == 'GET':
        url=str(request.GET['url'])
        context = {
            'url':url,
        }
        return render(request,'archive/report_error.html',context)
    elif request.method == 'POST':
        tk = Ticket(usr_creator = request.user,
                    tag='error',
                    message=str(request.POST['msg']),
                    link=str(request.POST['url'])
                    )
        tk.save()
        return redirect('archive:archive_home')