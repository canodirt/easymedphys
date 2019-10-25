# Generated by Django 2.2.6 on 2019-10-24 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cme', '0003_auto_20191021_2216'),
    ]

    operations = [
        migrations.CreateModel(
            name='samResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('samQuestion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cme.samQuestion')),
                ('selectedAnswer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cme.samAnswer')),
            ],
        ),
    ]