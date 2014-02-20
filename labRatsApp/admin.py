from django.contrib import admin
from labRatsApp.models import User, Experiment,Timeslots,Tags,HaveTags,BidFor,ParticipateIn

admin.site.register(User)
admin.site.register(Experiment)
admin.site.register(Timeslots)
admin.site.register(Tags)
admin.site.register(HaveTags)
admin.site.register(BidFor)
admin.site.register(ParticipateIn)

