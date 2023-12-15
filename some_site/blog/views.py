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

def gcd():
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y:%m:%d")
    return str(formatted_date)

#api views
@api_view(['GET', 'POST'])
def comment_api(request):
	if request.method == "GET":
		try:
			state_id = request.GET["id"]
			comment = comments.objects.filter(state_id=state_id)
			dat = comment_api_ser(comment , many=True)
			return Response(dat.data)
		except Exception as e:
			return Response([str(e)], status=400)


	else:
		return Response(["400"], status=400)


	I



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

def main(request):

	list_of_states = execcute("SELECT * FROM blog_states ORDER BY time_of_publicate LIMIT 5")

	html_string = """ """
	for i in list_of_states:
		html_string += f"<h3>{i[6]}</h3>"
		html_string += f'<a href="http://127.0.0.1:8000/state/?id={i[1]}"> {i[len(i)-1][:len(i[len(i)-1])//4]} ... </a>'



	return render(request , "main.html" , context={"content":mark_safe(html_string)})
	
def reg(request):
	if request.user.is_authenticated:
		return redirect('/')
	else:
		return render(request , "reg.html")

def get_reg(request):
    lg = request.POST.get("login")
    pswd = request.POST.get('pswd')
    mail = request.POST.get('email')
    first = request.POST.get('first')
    second = request.POST.get('second')
  
    if User.objects.filter(username=lg , email=mail ).exists():
        return render(request, "base.html" , context={'content':'Such user already exists in the system.'})
  
    else:
        user = User.objects.create_user(lg, mail, pswd)
        user.first_name = first
        user.last_name = second
        user.save()
        login(request, user)
        return redirect('/')

def auth(request):
	if not(request.user.is_authenticated):
		return render(request , "auth.html")
	else:
		return redirect("http://127.0.0.1:8000/")

def get_auth(request):
  usr = request.POST.get("login")
  pswd = request.POST.get('pswd')
  user = authenticate(request, username=usr, password=pswd)
  if user is not None:
    login(request, user) 
    return redirect('/')
  else:
    return render(request, "info.html", context={"content": 'wrong user or login'})

def lg(request):
    logout(request)
    return redirect('/')
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
		blog.objects.create(blog_id = gri(), themes = theme_of_channel , 
								about=about , cover=logo , author_id = request.user.id)
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
				html_string += f"<p>{i.time_of_publicate}</p>"
				html_string += f"<p>{i.topic}</p>"
				html_string += f"<a href='http://127.0.0.1:8000/state/?id={i.state_id}'>{i.text[:len(i.text)//8]}...</a> <p>"

			html_string += "<a href='http://127.0.0.1:8000/new_state'>Создать статью</a>"

			safe_html = mark_safe(html_string)


			




			return render(request , "studio.html" , context={"name_of_blog":blogic.blog_id , 
															"usr":request.user.username,
															"theme_blog":blogic.themes,
															"img_url":f"/media/{blogic.cover}",
															"blog_description":blogic.about,
															"states_html":safe_html})
		else:
			return redirect("http://127.0.0.1:8000/auth/")
	except:
		return redirect("set_channel/")

def create_new_state(request):
	if request.method == "GET":
		if  not request.user.is_authenticated:
			return redirect("/")
		else:
			return render(request , "create_state.html")	
	if request.method == "POST":
		#getting data from request
		name_of_state = request.POST.get("name_of_state")
		text_of_state = request.POST.get("text_of_state")

		#getting data from Db
		mother_blog = blog.objects.get(author_id = request.user.id)
		blog_id = mother_blog.blog_id

		#inserting data to Db

		states.objects.create(
								time_of_publicate = datetime.datetime.now().strftime("%Y-%m-%d"),
								topic = name_of_state,
								text = text_of_state,
								blog_id  = blog_id,
								state_id=gri(),
							)
		return redirect("/studio")
	else:
		return render(request, "info.html", context={"content": 'HTTP 400 Bad request'})


def view_state(request):
	pass
	# try:
	# 	state = request.GET.get("id")


	# 	state = states.objects.get(state_id=state)

	# 	mother_blog = blog.objects.get(blog_id = state.blog_id)

	# 	author = mother_blog.author

	# 	state.views += 1

	# 	state.save()

	# 	if author == request.user.username:
	# 		return render(request , "state.html" , context={
	# 		"topic":state.topic , "text":state.text , "date":state.time_of_publicate, "views":state.views , 
	# 		"author":mother_blog.name_of_blog, "img":f"{mother_blog.cover}", "st_id":request.GET.get("id"),
	# 		"del":"<button onclick='fetch('http://127.0.0.1:8000/upload_image', {method: "POST", body: formData});'>удалить статью</button>"})
	# 	else:
	# 		return render(request , "state.html" , context={
	# 			"topic":state.topic , "text":state.text , "date":state.time_of_publicate, "views":state.views , 
	# 			"author":mother_blog.name_of_blog, "img":f"{mother_blog.cover}", "st_id":request.GET.get("id")})

	# except:
	# 	return render(request, "state.html", context={"topic": "Oops... this article doesn't exist!", "text": "So create it yourself! It's quite easy!",})

def states_list(request):
	list_of_states = execcute("SELECT * FROM blog_states ORDER BY views")

	html_string = """ """
	for i in list_of_states:
		html_string += f"<h3>{i[6]}</h3>"
		html_string += f'<a href="http://127.0.0.1:8000/state/?id={i[1]}"> {i[len(i)-1][:len(i[len(i)-1])//4]} ... </a>'



	return render(request , "list_of_states.html" , context={"content":mark_safe(html_string)})


def all_channel(request):
	list_of_channels = execcute("SELECT * FROM blog_blog ")
	html_string = """ """
	for i in list_of_channels:
		html_string += f"<span><H1>{i[3]}</H1>"
		html_string += f"<img src='http://127.0.0.1:8000/media/{i[4]}' width=20px , height=20px> </span>"
		html_string += f"<p>About: {i[3]}</p>"
		html_string += f"<p>On theme: {i[2]}</p>"
		html_string += f'<a href="http://127.0.0.1:8000/channel/?id={i[0]}" ,  color="white"> Go to channel </a> <hr>'



	return render(request , "list_of_channels.html" , context={"content":mark_safe(html_string)})





def channel(request):
	blogic = blog.objects.get(blog_id=request.GET.get("id"))

	#getting list of states
	list_of_states = states.objects.filter(blog_id=blogic.blog_id)

	html_string = """ """

	for i in list_of_states:
		html_string += f"<p>{i.time_of_publicate}</p>"
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

		return redirect(f"http://127.0.0.1:8000/state/?id={st_id}")


	else:
		return JsonResponse(["400"], status=400)


def up_img(request):
	logo = request.FILES['photo']
	file_name = default_storage.save(logo.name, logo)
	return JsonResponse(["200"], safe=False)

