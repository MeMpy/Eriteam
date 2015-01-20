# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('effort', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delay', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Dependencies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('duration', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('code', models.CharField(default=b'', max_length=150, blank=True)),
                ('description', models.TextField(default=b'', max_length=255, blank=True)),
                ('row_index', models.IntegerField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('duration', models.FloatField()),
                ('status', models.CharField(default=b'STATUS_ACTIVE', max_length=50, choices=[(b'STATUS_ACTIVE', b'STATUS_ACTIVE'), (b'STATUS_DONE', b'STATUS_DONE'), (b'STATUS_FAILED', b'STATUS_FAILED'), (b'STATUS_SUSPENDED', b'STATUS_SUSPENDED'), (b'STATUS_UNDEFINED', b'STATUS_UNDEFINED')])),
                ('progress', models.IntegerField(default=0)),
                ('level', models.IntegerField()),
                ('assigned_to', models.ManyToManyField(to='gantt.Resource', through='gantt.Assignment')),
                ('depends_on', models.ManyToManyField(to='gantt.Task', through='gantt.Dependency')),
                ('parent', models.ForeignKey(related_name='grafted_task_set', blank=True, to='gantt.Task', null=True)),
                ('project', models.ForeignKey(to='gantt.Project')),
            ],
            options={
                'ordering': ['row_index'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='project',
            name='resources',
            field=models.ManyToManyField(related_name='work_on', to='gantt.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dependency',
            name='finish_task',
            field=models.ForeignKey(related_name='+', to='gantt.Task'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dependency',
            name='start_task',
            field=models.ForeignKey(related_name='dependency_set', to='gantt.Task'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='dependency',
            unique_together=set([('start_task', 'finish_task')]),
        ),
        migrations.AddField(
            model_name='assignment',
            name='resource',
            field=models.ForeignKey(to='gantt.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignment',
            name='task',
            field=models.ForeignKey(to='gantt.Task'),
            preserve_default=True,
        ),
    ]
