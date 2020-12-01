# Generated by Django 3.1 on 2020-11-28 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reci', '0015_auto_20201028_2143'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Categorie'},
        ),
        migrations.AlterModelOptions(
            name='comments',
            options={'verbose_name': 'Comment'},
        ),
        migrations.AlterModelOptions(
            name='recipes',
            options={'verbose_name': 'Recipe'},
        ),
        migrations.AddField(
            model_name='recipes',
            name='star',
            field=models.BooleanField(default=False),
        ),
    ]