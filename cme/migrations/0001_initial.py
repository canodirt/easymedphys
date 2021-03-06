# Generated by Django 2.2.6 on 2019-10-20 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('short_description', models.CharField(max_length=400)),
                ('isSAM', models.BooleanField()),
                ('isCAMPEP', models.BooleanField()),
                ('isMDCB', models.BooleanField()),
                ('start_datetime', models.DateTimeField(verbose_name='start time')),
                ('end_datetime', models.DateTimeField(verbose_name='end time')),
                ('presenter', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('address', models.CharField(max_length=200)),
                ('weblink', models.CharField(max_length=200)),
                ('urlshortOrganization', models.CharField(max_length=20, unique=True)),
                ('create_date', models.DateTimeField(verbose_name='date added')),
            ],
        ),
        migrations.CreateModel(
            name='samQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(max_length=900)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cme.event')),
            ],
        ),
        migrations.CreateModel(
            name='samAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField(max_length=900)),
                ('correct_answer', models.BooleanField(default=False)),
                ('samQuestion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cme.samQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=6000)),
                ('location', models.TextField(max_length=2000)),
                ('create_date', models.DateTimeField(verbose_name='date added')),
                ('urlshortEvents', models.CharField(max_length=20, unique=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cme.Organization')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cme.Events'),
        ),
        migrations.CreateModel(
            name='evaluation_Speaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('learningObjectives', models.IntegerField()),
                ('usefulness', models.IntegerField()),
                ('quality', models.IntegerField()),
                ('handout', models.IntegerField()),
                ('worthiness', models.IntegerField()),
                ('percentAttended', models.FloatField()),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cme.event')),
            ],
        ),
        migrations.CreateModel(
            name='evaluation_Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programContent', models.IntegerField()),
                ('learningObjectives', models.IntegerField()),
                ('facultyKnowledge', models.IntegerField()),
                ('quality', models.IntegerField()),
                ('handouts', models.IntegerField()),
                ('meetingRoom', models.IntegerField()),
                ('audio', models.IntegerField()),
                ('additionalComments', models.TextField()),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cme.Events')),
            ],
        ),
        migrations.CreateModel(
            name='attendance_Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendee', models.TextField(max_length=2000)),
                ('percentAttended', models.FloatField()),
                ('create_date', models.DateTimeField(verbose_name='date added')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cme.event')),
            ],
        ),
    ]
