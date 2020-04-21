# Generated by Django 2.0.7 on 2018-09-04 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Acounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.IntegerField(default=0)),
                ('cookie', models.TextField(default=None, null=True)),
                ('website', models.CharField(max_length=255)),
                ('trouble', models.TextField(default=None, null=True)),
                ('baned', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'accounts',
                'ordering': ['-timestamp'],
            },
        ),
    ]