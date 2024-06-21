# Generated by Django 4.2.8 on 2024-05-21 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cur_unit', models.CharField(max_length=100)),
                ('cur_nm', models.CharField(max_length=100)),
                ('ttb', models.FloatField()),
                ('tts', models.FloatField()),
                ('deal_bas_r', models.FloatField()),
            ],
        ),
    ]
