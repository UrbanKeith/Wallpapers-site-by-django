# Generated by Django 3.1.1 on 2020-09-10 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=30, unique=True, verbose_name='Категория')),
                ('category_link_name', models.CharField(max_length=30, unique=True, verbose_name='Название для ссылки')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Имя картинки')),
                ('date', models.DateField(auto_now=True, verbose_name='Дата загрузки')),
                ('categories', models.ManyToManyField(blank=True, to='wallpapers_main.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('1280x720', 'HD'), ('1600x900', 'WXGA++'), ('1920x1080', 'Full HD'), ('2560×1440', 'Quad HD')], max_length=30, verbose_name='Разрешение')),
                ('source', models.URLField(verbose_name='Ссылка на источник')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallpapers_main.images')),
            ],
        ),
    ]
