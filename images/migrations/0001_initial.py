# Generated by Django 2.0.6 on 2018-06-28 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import images.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('image', models.ImageField(upload_to=images.models.upload_location)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateField(auto_now_add=True, db_index=True)),
                ('total_likes', models.PositiveIntegerField(db_index=True, default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images_created', to=settings.AUTH_USER_MODEL)),
                ('user_like', models.ManyToManyField(blank=True, related_name='images_liked', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
