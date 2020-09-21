import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","web_dev.settings")

import django 
django.setup()


import random

from networking.models import *
from posts.models import *
from networking.models import *
from reg_sign_in_out.models import *

from faker import Faker

fakegen = Faker()
topics = ["Search","Social","Marketplace","News","Games"]

def add_topic():
    t = Topic.objects.get_or_create(top_name=random.choice(topics))
    t = t[0]
    t.save()
    return t

def populate(N=5):

    for i in range(N):
        top = add_topic()

        f_url = fakegen.url()
        f_date = fakegen.date()
        f_name = fakegen.company()

        webpg = Webpage.objects.get_or_create(topic=top,url=f_url,name=f_name)[0]

        acc_rec = AccessRecord.objects.get_or_create(name=webpg,date=f_date)[0]

if __name__=="__main__":
    populate(20)