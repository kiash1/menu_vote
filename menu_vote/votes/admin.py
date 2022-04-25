from django.contrib import admin

from menu_vote.votes.models import Vote, VoteResult

admin.site.register(Vote)
admin.site.register(VoteResult)
