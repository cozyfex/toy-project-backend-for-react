# Generated by Django 4.1.3 on 2022-12-06 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseBoard',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Board Id')),
                ('title', models.CharField(max_length=255, verbose_name='Board Title')),
                ('name', models.CharField(max_length=255, verbose_name='Board Author')),
                ('content', models.TextField(null=True, verbose_name='Board Content')),
                ('reg_date', models.DateTimeField(auto_now_add=True, verbose_name='Register Date')),
                ('mod_date', models.DateTimeField(auto_now_add=True, verbose_name='Modify Date')),
            ],
            options={
                'db_table': 'base_board',
            },
        ),
    ]
