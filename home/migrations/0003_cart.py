# Generated by Django 3.1.7 on 2021-03-05 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20210225_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=300)),
                ('quantity', models.IntegerField(default=1)),
                ('user', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now=True)),
                ('total', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.items')),
            ],
        ),
    ]
