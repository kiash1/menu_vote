# Generated by Django 3.2 on 2022-04-22 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import menu_vote.votes.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('menus', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at_date', models.DateField(auto_now_add=True, unique=True)),
                ('votes', models.IntegerField()),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vote_results', to='menus.menu')),
            ],
            bases=(menu_vote.votes.models.VoteResultMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at_date', models.DateField(auto_now_add=True)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='votes', to='menus.menu')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'menu', 'created_at_date')},
            },
            bases=(menu_vote.votes.models.VoteResultMixin, models.Model),
        ),
    ]