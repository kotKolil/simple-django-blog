<iframe width=200 height=200 src="https://giphy.com/embed/ijvngPcd8kNOha4Se1" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/potato-server-potatoes-ijvngPcd8kNOha4Se1"></a> 
<H5 align="center" style="color:#87CEEB;">
Simple Django Blog by KotKolil 

</H5>

<br>
<p align="left">
I present to you my simple blog on the Django web framework. It allows users to register, create their own blog, view and comment on articles. I have used features provided by this framework, such as request handling, user authentication, and template rendering.
</p>

<H6>Starting server</H6>


To run the web server, you need to download this repository first. Before starting, you need to set up environment variables for your system that control the behavior of the web server:
1.) IS_DEBUG - This variable controls whether the server runs in debug or production mode.
2.) DOMAIN_NAME - This variable specifies the domain name for links on the pages.

If you are using Docker, you need to modify the environment variables of your server container in the Dockerfile. You need to create tables in the database using "python manage.py migrate". Then, if necessary, create a superuser using "python manage.py createsuperuser". The server uses static files, which need to be collected using "python manage.py collectstatic". Finally, the server is launched with "python manage.py runserver".

<br>

<hr>
<p><a href="https://t.me/Fx000777"><img width="30" src="https://cdn.icon-icons.com/icons2/923/PNG/256/telegram_icon-icons.com_72055.png"> </p></a>