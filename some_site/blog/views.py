
from django.core.files.storage import default_storage
from django.shortcuts import *
from django.http import *
from django.contrib.auth.models import User
from django.contrib.auth import *
from django.db import connection
from blog.models import *
import random
from datetime import datetime
from django.utils.safestring import mark_safe
import asyncio
from asgiref.sync import async_to_sync, sync_to_async
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime
from django.shortcuts import redirect 
from django.conf import settings
import json

#TODO change localhost to variable
#Domain name of your web server
DOMAIN = settings.DOMAIN_URI



def is_not_his_state(ids=None, usr=None):
	print(ids)
	print(usr)
	if ids is None:
		return True
	else:
		blg = blog.objects.get(author=usr)
		try:
			state = states.objects.get(state_id=ids, blog_id=blg.blog_id)
			return False
		except Exception as e:
			print(e)
			return True




def gcd():
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")
    return formatted_date


#normal views

#get random id

def gri():
	#unique indeficator of session
	return random.randint(0, 1000000)

def execcute(query):
	with connection.cursor() as cursor:
		cursor.execute(query)
		rows = cursor.fetchall() #get all strings of answer
		return rows 
	
def reg(request):
  if request.method == "GET":
    if not request.user.is_authenticated:
      return render(request, 'reg.html', status=200)
    else:
      return redirect("/")
  elif request.method == "POST":
    lg = request.POST.get("login")
    mail = request.POST.get("email")
    pswd = request.POST.get('password')
    try:
      usr = User.objects.create_user(username=lg, email=mail, password=pswd)
      usr.save()
      userok = authenticate(username=lg, password=pswd)
      login(request, userok)  
      return redirect("/")
    except Exception as e:
      return render(request, "info.html", context={"content": str(e)})


def main(request):

	list_of_states = execcute("SELECT * FROM blog_states ORDER BY time_of_publication LIMIT 5")

	html_string = """ """
	for i in list_of_states:
		html_string += f"<h3>{i[6]}</h3>"
		html_string += f'<a href="http://{DOMAIN}/state/?id={i[1]}"> {i[len(i)-1][:len(i[len(i)-1])//4]} ... </a>'



	return render(request , "main.html" , context={"content":mark_safe(html_string)})
	

def ish_kab(request):
	if request.user.is_authenticated:
		return render(request, "ish_kab.html" , context={
			'name':f'{request.user.username}',
			



			})

	else:
		return redirect('/auth/')
		


def pnf(request , exception):
	return render(request , "404.html" , status=404)


def set_channel(request):
	if request.method == "GET":
		if request.user.is_authenticated:
			id_user = request.user.id
			print(f'aaaaaaaaaaaa {id_user}')
			#return render(request, "info.html", context={"content": id_user})
			result = execcute(f"SELECT * FROM blog_blog WHERE author_id = '{id_user}'")

			if len(result) != 0: 
				return render(request, "info.html", context={"content": "You channel is already exists"})
			else:
				return render(request , "create_channel.html")

		else:
			return redirect('/auth')
	if request.method == "POST":
		about = request.POST.get('about')
		name_of_blog = request.POST.get("name_of_blog")
		theme_of_channel = request.POST.get('theme')
		logo = request.FILES['photo']
		blg = blog.objects.create(blog_id = gri(), themes = theme_of_channel , 
								about=about , cover=logo , author_id = request.user.id)
		blg.save()
		return redirect("/")

	else:
		return render(request, "info.html", context={"content": 'HTTP 400 Bad request'})




def fuck_dogs(request):
	h = blog.objects.get(blog_id=' f787kt')

	return render(request , "info.html" , context={"content":h.cover.url})




def studio(request):
	try:
		if request.user.is_authenticated:
			blogic = blog.objects.get(author_id = request.user.id)

			#getting list of states
			list_of_states = states.objects.filter(blog_id=blogic.blog_id)

			html_string = """ """

			for i in list_of_states:
				html_string += f"<p>{i.time_of_publication}</p>"
				html_string += f"<p>{i.topic}</p>"
				html_string += f"<a href='http://{DOMAIN}/state/?id={i.state_id}'>{i.text[:len(i.text)//8]}...</a> <p>"

			html_string += "<a href='http://{DOMAIN}/new_state'>Создать статью</a>"

			safe_html = mark_safe(html_string)


			




			return render(request , "studio.html" , context={"name_of_blog":blogic.blog_id , 
															"usr":request.user.username,
															"theme_blog":blogic.themes,
															"img_url":f"/media/{blogic.cover}",
															"blog_description":blogic.about,
															"states_html":safe_html})
		else:
			return redirect(f"http://{DOMAIN}/auth/")
	except:
		return redirect(f"http://{DOMAIN}/set_channel/")

def create_new_state(request):
	try:
		if request.method == "GET":
			# foo = is_not_his_state(request.GET.get("id"), request.user)
			# if foo:
				# return redirect("/")
			# else:
			return render(request , "create_state.html")	
		if request.method == "POST":

			#getting json data from request
			dat = json.loads(request.body)
		
			data = dat["state_data"]
			token = dat["token"]
			top = dat['topic']

			print(data)
			print(token)
			print(top)



			mother_blog = blog.objects.get(author=request.user)



			try:
				#queryset is not empty
				lst = states.objects.get(state_id=token)
				lst.time_of_publication = gcd()
				lst.text = data
				lst.topic = top
				lst.save()
				return JsonResponse(["201"], status=201, safe=False)


			except states.DoesNotExist:
				#queryset is empty
				state = states.objects.create(state_id=token,
									blog_id = mother_blog.blog_id,
									time_of_publication=gcd(),
									text = data,
									topic = top)
				return JsonResponse(['OK'], status=201, safe=False)



	except Exception as error:
		print(error)
		return JsonResponse(json.dumps(
			{
				"message":"500 Internal Server Error",
				"error":str(error)	
			}
				), status=500, safe=False)
		



	else:
		return render(request, "info.html", context={"content": 'HTTP 400 Bad request'}, status=400)


def view_state(request):
	try:
		state = request.GET.get("id")


		state = states.objects.get(state_id=state)

		mother_blog = blog.objects.get(blog_id = state.blog_id)

		author = mother_blog.author

		state.views += 1

		state.save()

		if not is_not_his_state(state.state_id, request.user):
			print("regvre")
			return render(request , "state.html" , context={
			"topic":state.topic , "text":state.text , "date":state.time_of_publication, "views":state.views , 
			"author":mother_blog.name_of_blog, "img":f"{mother_blog.cover}", "st_id":request.GET.get("id") 
			, "edt":f"""<a href='http://{DOMAIN}/new_state/?id={state}'>edit state</a>
						<a href='http://{DOMAIN}/del_state/?id={state}'>delete state</a>"""})
		else:
			return render(request , "state.html" , context={
				"topic":state.topic , "text":mark_safe(state.text) , "date":state.time_of_publication, "views":state.views , 
				"author":mother_blog.name_of_blog, "img":f"{mother_blog.cover}", "st_id":request.GET.get("id")})

	except:
		return render(request, "state.html", context={"topic": "Oops... this article doesn't exist!", "text": "So create it yourself! It's quite easy!",})

def states_list(request):
	list_of_states = execcute("SELECT * FROM blog_states ORDER BY views")

	html_string = """ """
	for i in list_of_states:
		html_string += f"<h3>{i[6]}</h3>"
		html_string += f'<a href="http://{DOMAIN}/state/?id={i[1]}"> {i[len(i)-1][:len(i[len(i)-1])//4]} ... </a>'



	return render(request , "list_of_states.html" , context={"content":mark_safe(html_string)})


def all_channel(request):
	list_of_channels = execcute("SELECT * FROM blog_blog ")
	html_string = """ """
	for i in list_of_channels:
		html_string += f"<span><H1>{i[3]}</H1>"
		html_string += f"<img src='http://{DOMAIN}/media/{i[4]}' width=20px , height=20px> </span>"
		html_string += f"<p>About: {i[3]}</p>"
		html_string += f"<p>On theme: {i[2]}</p>"
		html_string += f'<a href="http://{DOMAIN}/channel/?id={i[0]}" ,  color="white"> Go to channel </a> <hr>'



	return render(request , "list_of_channels.html" , context={"content":mark_safe(html_string)})





def channel(request):
	blogic = blog.objects.get(blog_id=request.GET.get("id"))

	#getting list of states
	list_of_states = states.objects.filter(blog_id=blogic.blog_id)

	html_string = """ """

	for i in list_of_states:
		html_string += f"<p>{i.time_of_publication}</p>"
		html_string += f"<p>{i.topic}</p>"
		html_string += f"<p>{i.text[:len(i.text)//8]}...</p>"

	safe_html = mark_safe(html_string)



	




	return render(request , "studio.html" , context={"name_of_blog":blogic.blog_id , 
													"usr":request.user.username,
													"theme_blog":blogic.themes,
													"img_url":f"/media/{blogic.cover}",
													"blog_description":blogic.about,
													"states_html":safe_html})

def post_comment(request):
	if request.user.is_authenticated and request.method == "POST":
		text = request.POST.get("text")
		st_id = request.POST.get("state_id")
		comments.objects.create(state_id=str(st_id) , user = request.user.username , 
			date = datetime.datetime.now().strftime("%Y-%m-%d"), text= text )

		return JsonResponse(["200"], status=300)


	else:
		return JsonResponse(["400"], status=400)


def up_img(request):
	logo = request.FILES['photo']
	file_name = default_storage.save(logo.name, logo)
	return JsonResponse(["200"], safe=False)


#NOTE This is API views
#NOTE creating API by DRF is too difficult

def view_state_api(request):
	if request.method == "POST":
		# try:
		dat = json.loads(request.body)
		tok = dat["tok"]

		print(f'[*]:{tok}')

		try:
			queryset = states.objects.get(state_id=tok)

			return JsonResponse([

			queryset.topic,
			queryset.text,
			
	


			], safe = False, status=200)
		except states.DoesNotExist as e:
			return JsonResponse(['404', str(e)], status=404, safe=False)
		# except Exception as e:
		# 	return JsonResponse([str(e) , "404"], status=400, safe=False)

	else:
		return JsonResponse(['400'], status=400, safe=False)


def del_state(request):
	foo = is_not_his_state(request.GET.get("id"), request.user)
	if foo:
		return redirect("/")
	else:
		lst = states.objects.get(state_id=request.GET.get("id"))
		lst.delete()
		return redirect("/studio")
		
def comment_api(request):
	if request.method == "GET":
		state_id = request.GET.get("id")
		query_set = comment_api_ser(comments.objects.filter(state_id=state_id), many=True)
		if query_set.is_valid:
			return JsonResponse(query_set.data, safe=False)

	elif request.method == "POST":
		if request.user.is_authenticated:
			dat = json.loads(request.body)
			print(dat)
			state_id = dat[f"state_id"]
			text  = dat["text"]
			usr = request.user.username
			date = gcd()
			comments.objects.create(state_id=state_id,
						   			text=text,
									user=usr,
									date=gcd(),
			)
			return JsonResponse(["200"], safe=False)
		else:
			return JsonResponse(["401"], status=401)
	else:
		return JsonResponse(["400"], status=400)


def reactions_api(request):
	if request.user.is_authenticated:
		if request.method == "GET":
			state_id = request.GET.get("id")
			state = states.objects.get(state_id=state_id)
			likes = state.likes
			dislikes = state.dislikes
			if request.GET.get("type") == "state":
				return JsonResponse([len(likes), len(dislikes) ], safe=False)
			elif request.GET.get("type") == "user":
				l =  int(request.user.username in likes)
				d =  int(request.user.username in likes)
				return JsonResponse([str(l),str(d)], safe=False)
			else:
				return JsonResponse(["barabaraberere"], status=400, safe=False)
			
		elif request.method == "POST":
			try:
				dat = json.loads(request.body);
				print(dat)
				react = dat["react"]
				state_id = dat["state_id"]
				print(dat)
				user  = request.user.username
				state = states.objects.get(state_id=state_id)
				if react == "like":
					if user in state.dislikes:
						state.dislikes.remove(user) 
						state.likes.append(user)
					elif user in state.likes:
						state.likes.remove(user)
				if react == "dislike":
					if user in state.likes:
						state.likes.remove(user) 
						state.likes.append(user)
					elif user in state.dislikes:
						state.dislikes.remove(user)
				return JsonResponse(["200"], status=200, safe=False)

			except Exception as e:
				return JsonResponse([str(e)], status=500, safe=False)


		else:
			return JsonResponse(['400'], status=400, safe=False)