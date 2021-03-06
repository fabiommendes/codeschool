# Generated by Django 2.0.5 on 2018-05-07 03:54

import autoslug.fields
import boogie.utils.phrases
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=40, verbose_name='name')),
                ('description', models.CharField(blank=True, help_text='Conscise description used on listings.', max_length=255, verbose_name='description')),
                ('slug', autoslug.fields.AutoSlugField(help_text='Unique identifier used to construct urls', primary_key=True, serialize=False, verbose_name='slug')),
                ('long_description', models.TextField(blank=True, help_text='Detailed description of object.', verbose_name='detailed description')),
                ('location', models.CharField(blank=True, help_text='Physical location of classroom, if applicable.', max_length=140, verbose_name='location')),
                ('is_accepting_subscriptions', models.BooleanField(default=True, help_text='Set it to false to prevent new student subscriptions.', verbose_name='accept subscriptions')),
                ('is_public', models.BooleanField(default=False, help_text='If true, all students will be able to see the contents of the course. Most activities will not be available to non-subscribed students.', verbose_name='is it public?')),
                ('subscription_passphrase', models.CharField(blank=True, default=boogie.utils.phrases.phrase_lower, help_text='A passphrase/word that students must enter to subscribe in the course. Leave empty if no passphrase should be necessary.', max_length=140, verbose_name='subscription passphrase')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=40, verbose_name='name')),
                ('description', models.CharField(blank=True, help_text='Conscise description used on listings.', max_length=255, verbose_name='description')),
                ('slug', autoslug.fields.AutoSlugField(help_text='Unique identifier used to construct urls', primary_key=True, serialize=False, verbose_name='slug')),
                ('school_id', models.CharField(blank=True, max_length=50)),
                ('since', models.DateField(blank=True, null=True)),
                ('syllabus', models.TextField(blank=True)),
                ('program', models.TextField(blank=True)),
                ('bibliography', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=40, verbose_name='name')),
                ('description', models.CharField(blank=True, help_text='Conscise description used on listings.', max_length=255, verbose_name='description')),
                ('slug', autoslug.fields.AutoSlugField(help_text='Unique identifier used to construct urls', primary_key=True, serialize=False, verbose_name='slug')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='discipline',
            name='organization',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='classrooms.Organization'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='discipline',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='classrooms.Discipline'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='staff',
            field=models.ManyToManyField(blank=True, related_name='classrooms_as_staff', to=settings.AUTH_USER_MODEL, verbose_name='staff'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='classrooms_as_student', to=settings.AUTH_USER_MODEL, verbose_name='students'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='classrooms_as_teacher', to=settings.AUTH_USER_MODEL),
        ),
    ]
