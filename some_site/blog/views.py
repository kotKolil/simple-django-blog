
from django.core.files.storage import default_storage
from django.shortcuts import *
from django.http import *
from django.contrib.auth.models import User
from django.contrib.auth import *
from django.db import connection
from .models import *
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

	list_of_states = states.objects.all()

	html_string = ""
	for i in list_of_states:
		html_string += f"<div class = 'card' > <a href='http://{DOMAIN}/state/?id={i.state_id}'> <h3>{i.topic} </h3> </a>  { i.text[ :len( i.text ) // 8 ] }... </div>"
		
		
		
	html_string = f"<div class = 'wrapper'>{html_string}</div>"

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
	# try:
	if request.user.is_authenticated:
		blogic = blog.objects.get(author_id = request.user.id)

		#getting list of states
		list_of_states = states.objects.filter(blog_id=blogic.blog_id)


		html_string = ""
		

		
		for i in list_of_states:
			html_string += f"<div class = 'card' > <a href='http://{DOMAIN}/state/?id={i.state_id}'> <h3>{i.topic} </h3> </a>  { i.text[:len(i.text)//4] }... </div>"
			
			
			
		html_string = f"<div class = 'wrapper'>{html_string}</div>"
		
		return render(request , "studio.html" , context={
			"name_of_blog":blogic.name_of_blog , 
			"usr":request.user.username,
			"theme_blog":blogic.themes,
			"img_url":f"/media/{blogic.cover}",
			"blog_description":blogic.about,
			"states_html":mark_safe(html_string),
			"awesome_html": f"<a href = '/new_state'><H3>create state</H3></a>",
														}
					)
	else:
		return redirect(f"http://{DOMAIN}/accounts/login")
	# except:
	# 	return redirect(f"http://{DOMAIN}/set_channel/")

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
					return render(request , "state.html" , context={
			"text":state.text,
			"topic":state.topic,
			"name_of_blog":mother_blog.name_of_blog, 
			"usr":request.user.username,
			"theme_blog":mother_blog.themes,
			"img_url":f"/media/{mother_blog.cover}",
			"blog_description":mother_blog.about,
														}
					)


		else:
				return render(request , "state.html" , context={
			"text":state.text,
			"topic":state.topic,
			"name_of_blog":mother_blog.name_of_blog, 
			"usr":request.user.username,
			"theme_blog":mother_blog.themes,
			"img_url":f"/media/{mother_blog.cover}",
			"blog_description":mother_blog.about,
														}
					)



	except:
		return render(request, "state.html", context={"topic": "Oops... this article doesn't exist!", "text": "So create it yourself! It's quite easy!",})

def states_list(request):
	list_of_states = execcute("SELECT * FROM blog_states ORDER BY views")

	print(len(list_of_states))

	html_string = ""
	for i in list_of_states:
		html_string += f"<div class = 'card' > <a href='http://{DOMAIN}/state/?id={i[1]}'> <h3>{i[5]} </h3> </a>  { i[6][ :len( i[6] ) // 8 ] }... </div>"
		
		
		
	html_string = f"<div class = 'wrapper'>{html_string}</div>"

	return render(request , "main.html" , context={"content":mark_safe(html_string)})


def all_channel(request):
	list_of_channels = execcute("SELECT * FROM blog_blog ")
	html_string = """ """

	html_string = ""
	for i in list_of_channels:

		html_string += f"""<div class = 'card' > 
		
				<img src='/media/{i[4]}' style="border-radius:50%;with:20%;height:20%;" /> <a href = '/channel?id={i[0]}'> {i[3]} </a>
				<p> {i[1]} </p>
				<p> {i[2]} </p>
		
		</div>"""
		html_string = f"<div class = 'wrapper'>{html_string}</div>"




	return render(request , "main.html" , context={"content":mark_safe(html_string)})





def channel(request):

	blogic = blog.objects.get(author_id = request.user.id)

	#getting list of states
	list_of_states = states.objects.filter(blog_id=blogic.blog_id)


	html_string = ""
	for i in list_of_states:
		html_string += f"<div class = 'card' > <a href='http://{DOMAIN}/state/?id={i.state_id}'> <h3>{i.topic} </h3> </a>  { i.text[:len(i.text)//4] }... </div>"
		
		
		
	html_string = f"<div class = 'wrapper'>{html_string}</div>"

	




	return render(request , "studio.html" , context={
		"name_of_blog":blogic.name_of_blog , 
		"usr":request.user.username,
		"theme_blog":blogic.themes,
		"img_url":f"/media/{blogic.cover}",
		"blog_description":blogic.about,
		"states_html":mark_safe(html_string)					
													}
				)


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


