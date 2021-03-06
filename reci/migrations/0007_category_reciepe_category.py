# Generated by Django 3.1 on 2020-10-23 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reci', '0006_auto_20201017_1810'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='reciepe_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reci.category')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reci.recipes')),
            ],
        ),
    ]
