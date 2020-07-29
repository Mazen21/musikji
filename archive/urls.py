from django.urls import path
from . import views

app_name = "archive"

urlpatterns = [
    path('', views.archive_home, name="archive_home"),
    path('search/', views.archive_search, name="search"),
    
    path('instrument/', views.instrument_home, name="instrument_home"),
    path('instrument/<int:instr_id>/', views.instrument_detail, name="instrument_detail"),

    path('maqam/', views.maqam_home, name="maqam_home"),
    path('maqam/<int:maqam_id>/', views.maqam_detail, name="maqam_detail"),

    path('rythm/', views.rythm_home, name="rythm_home"),
    path('rythm/<int:rythm_id>/', views.rythm_detail, name="rythm_detail"),

    path('jins/', views.jins_home, name="jins_home"),
    path('jins/<int:jins_id>/', views.jins_detail, name="jins_detail"),

    path('musicform/', views.musicForm_home, name="musicform_home"),
    path('musicform/<int:musicForm_id>/', views.musicForm_detail, name="musicform_detail"),

    path('artist/', views.artist_home, name="artist_home"),
    path('artist/add/', views.artist_add, name="artist_add"),
    path('artist/<int:artist_id>/', views.artist_detail, name="artist_detail"),
    path('artist/<str:key_l>/', views.artist_fl, name="artist_fl"),

    path('song/', views.song_home, name="song_home"),
    path('song/<int:song_id>/', views.song_detail, name="song_detail"),
    path('song/search/', views.song_search, name="song_search"),
    path('song/add/', views.song_add, name="song_add"),
    path('song/edit/<int:song_id>/', views.song_edit, name="song_edit"),

    path('lyrics/', views.lyric_home, name="lyric_home"),
    path('lyrics/<int:lyric_id>/', views.lyric_detail, name="lyric_detail"),
    path('lyric/add/<int:song_id>/', views.lyric_add, name="lyric_add"),

    path('scores/', views.score_home, name="score_home"),
    path('scores/<int:score_id>/', views.score_detail, name="score_detail"),
    path('score/add/<int:song_id>/', views.score_add, name="score_add"),
    path('score/download/<int:score_id>/', views.score_download, name="score_download"),

    path('wiki/', views.wiki_home, name="wiki_home"),
    path('no_element/',views.wiki_no_element, name="wiki_no_element"),
    
    path('contact/',views.contact, name="contact"),
    path('report_error/', views.report_error, name="report_error"),
]