from django.contrib import admin
from labRatsApp.models import LabRatUser, Experiment,Timeslot,Tags,HaveTags,BidFor,ParticipateIn,EnrolIn

admin.site.register(LabRatUser)
admin.site.register(Experiment)
admin.site.register(Timeslot)
admin.site.register(Tags)
admin.site.register(HaveTags)
admin.site.register(BidFor)
admin.site.register(ParticipateIn)
admin.site.register(EnrolIn)
