from django.shortcuts import render_to_response
import cgi
from operator import itemgetter
import os
from models import Idea
from mongoengine import *
from django.http import HttpResponseRedirect, HttpResponseServerError
import random

class tagclass:
	tag = ''
	val = ''
	color = ''

def go(request):
	user = request.user
	
	filtertag =  request.META['HTTP_REFERER']
	showtag = False
	if filtertag.find('/tag/') >=0:
		showtag = True
		filtertag = filtertag.split('/')[4]
	else:
		filtertag = None
	
	tags = Idea.objects.item_frequencies('tags', normalize=True)
	top_tags = sorted(tags.items(), key=itemgetter(1), reverse=True)[:6]
	tagobs = []
	for key in top_tags:
		tg = tagclass()
		tg.tag = key[0]
		tg.val = key[1]
		tg.color = str(random.randrange(10,30,1))
		if len(tg.tag)>0:
			tagobs.append(tg)

	
	ideas = None
	ideas = Idea.objects(Q(isvisible=True) & Q(ispromoted=False)).order_by('-votecount')[:20]
	s_ideas = []
	for idea in ideas:
		if str(request.user) in idea.voters:
			idea.hasvoted = True
		if showtag:
			if filtertag in idea.tags:
				s_ideas.append(idea)
		else:
			s_ideas.append(idea)

	
	template_values = {
		'ideas': s_ideas,
		'user' : user,
		'tags': tagobs,
		'filtertag':filtertag,
	}

	path = os.path.join(os.path.dirname(__file__), 'templates/ideas/topten.html')
	return render_to_response(path, template_values)