# Generated by Django 4.2.5 on 2024-01-01 06:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_id', models.IntegerField()),
                ('user', models.CharField(max_length=7777)),
                ('date', models.DateField()),
                ('text', models.CharField(max_length=666)),
            ],
        ),
        migrations.CreateModel(
            name='states',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_id', models.IntegerField()),
                ('blog_id', models.IntegerField()),
                ('time_of_publication', models.DateField()),
                ('views', models.IntegerField(default=0)),
                ('topic', models.CharField(help_text='название статьи', max_length=23)),
                ('text', models.CharField(help_text='текст статьи', max_length=7777)),
                ('likes', jsonfield.fields.JSONField(default=dict)),
                ('dislikes', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='blog',
            fields=[
                ('blog_id', models.CharField(help_text='id блога', max_length=777, primary_key=True, serialize=False)),
                ('themes', models.CharField(help_text='темы блога (вводить через пробел)', max_length=777)),
                ('about', models.CharField(help_text='о блоге', max_length=777)),
                ('name_of_blog', models.CharField(help_text='имя блога', max_length=20)),
                ('cover', models.ImageField(upload_to='images/')),
                ('followers', models.IntegerField(default=0)),
                ('sub', jsonfield.fields.JSONField(default=dict)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
