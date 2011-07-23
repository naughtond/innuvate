from django.shortcuts import render_to_response
import cgi
import os
from models import Article,Idea,Score
from mongoengine import *
from django.http import HttpResponseRedirect, HttpResponseServerError
import random


def go(request):
	user = request.user
				
	scores = None
	#articles = Article.objects(reported=True)
	scores = Score.objects()
	
	
	template_values = {
		'scores': scores,
		'user' : user,
	}

	path = os.path.join(os.path.dirname(__file__), 'templates/ideas/managescores.html')
	return render_to_response(path, template_values)