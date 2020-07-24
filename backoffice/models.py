from django.db import models
from users.models import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    categories = [
        ('contact','contact'),
        ('request','request'),
        ('add song','add song'),
        ('update song','update song'),
        ('error song','error song'),
        ('add artist','add artist'),
        ('update artist','update artist'),
        ('error artist','error artist'),
        ('add score','add score'),
        ('update score','update score'),
        ('error score','error score'),
        ('add lyric','add lyric'),
        ('update lyric','update lyric'),
        ('error lyric','error lyric'),
        ('error','error'),
    ]
    status = [
        ('created','created'),
        ('processed','processed'),
        ('treated','treated'),
        ('abondanned','abondonned'),
        ('closed','closed'),
    ]
    usr_creator = models.ForeignKey(User,related_name="user_creator_set",on_delete=models.CASCADE,blank=True,null=True)
    usr_manager = models.ForeignKey(User,related_name="user_manager_set",on_delete=models.CASCADE,blank=True,null=True)
    tag = models.CharField(choices=categories, max_length=30,default="uncategorised")
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    link = models.URLField(max_length=200,blank=True)
    state = models.CharField(max_length=50,choices=status,default='created',blank=True)

    def __str__(self):
        return 'Ticket #' + str(self.id) + '__' + self.tag