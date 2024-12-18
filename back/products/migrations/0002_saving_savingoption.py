# Generated by Django 4.2.8 on 2024-05-22 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Saving',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kor_co_nm', models.CharField(max_length=100)),
                ('fin_prdt_cd', models.CharField(max_length=100)),
                ('fin_prdt_nm', models.CharField(max_length=100)),
                ('join_way', models.CharField(max_length=500)),
                ('mtrt_int', models.CharField(max_length=500)),
                ('spcl_cnd', models.CharField(max_length=500)),
                ('join_deny', models.CharField(max_length=5)),
                ('join_member', models.CharField(max_length=100)),
                ('etc_note', models.CharField(max_length=500)),
                ('max_limit', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SavingOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intr_rate_type_nm', models.CharField(max_length=2)),
                ('save_trm', models.CharField(max_length=5)),
                ('intr_rate', models.FloatField()),
                ('intr_rate2', models.FloatField()),
                ('saving', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.saving')),
            ],
        ),
    ]
