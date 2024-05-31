<H5 align="center" style="color:#87CEEB;">
Simple Django Blog by KotKolil 

</H5>

<br>
<p align="left">

<H6>About</H6>

I present to you my simple blog on the Django web framework. It allows users to register, create their own blog, view arcticles. I have used features provided by this framework, such as request handling, user authentication, and template rendering.

<H6>Starting server</H6>

To run the web server, you need to download this repository first. Before starting, you need to set up environment variables for your system that control the behavior of the web server:
1.) IS_DEBUG - This variable controls whether the server runs in debug or production mode.
2.) DOMAIN_NAME - This variable specifies the domain name for links on the pages.

If you are using Docker, you need to modify the environment variables of your server container in the Dockerfile. You need to create tables in the database using "python manage.py migrate". Then, if necessary, create a superuser using "python manage.py createsuperuser". The server uses static files, which need to be collected using "python manage.py collectstatic". Finally, the server is launched with "python manage.py runserver".

<br>

<H6>Working with Docker</H6>

To run the server as a Docker container, you need to execute the command "sudo docker-compose up -d". After that, the PostgresSQL database will start first, and then the application.

<hr>