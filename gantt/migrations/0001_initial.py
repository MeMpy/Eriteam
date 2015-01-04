# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table(u'gantt_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('duration', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'gantt', ['Project'])

        # Adding M2M table for field resources on 'Project'
        m2m_table_name = db.shorten_name(u'gantt_project_resources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'gantt.project'], null=False)),
            ('resource', models.ForeignKey(orm[u'gantt.resource'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'resource_id'])

        # Adding model 'Task'
        db.create_table(u'gantt_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('row_index', self.gf('django.db.models.fields.IntegerField')()),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('duration', self.gf('django.db.models.fields.FloatField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default=('OPN', 'OPEN'), max_length=50)),
            ('progress', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gantt.Project'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='grafted_task_set', null=True, to=orm['gantt.Task'])),
        ))
        db.send_create_signal(u'gantt', ['Task'])

        # Adding model 'Dependency'
        db.create_table(u'gantt_dependency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='start_task_set', to=orm['gantt.Task'])),
            ('finish_task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='finish_task_set', to=orm['gantt.Task'])),
            ('delay', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal(u'gantt', ['Dependency'])

        # Adding unique constraint on 'Dependency', fields ['start_task', 'finish_task']
        db.create_unique(u'gantt_dependency', ['start_task_id', 'finish_task_id'])

        # Adding model 'Resource'
        db.create_table(u'gantt_resource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'gantt', ['Resource'])

        # Adding model 'Assignment'
        db.create_table(u'gantt_assignment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gantt.Resource'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gantt.Task'])),
            ('effort', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'gantt', ['Assignment'])


    def backwards(self, orm):
        # Removing unique constraint on 'Dependency', fields ['start_task', 'finish_task']
        db.delete_unique(u'gantt_dependency', ['start_task_id', 'finish_task_id'])

        # Deleting model 'Project'
        db.delete_table(u'gantt_project')

        # Removing M2M table for field resources on 'Project'
        db.delete_table(db.shorten_name(u'gantt_project_resources'))

        # Deleting model 'Task'
        db.delete_table(u'gantt_task')

        # Deleting model 'Dependency'
        db.delete_table(u'gantt_dependency')

        # Deleting model 'Resource'
        db.delete_table(u'gantt_resource')

        # Deleting model 'Assignment'
        db.delete_table(u'gantt_assignment')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'gantt.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'effort': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gantt.Resource']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gantt.Task']"})
        },
        u'gantt.dependency': {
            'Meta': {'unique_together': "(('start_task', 'finish_task'),)", 'object_name': 'Dependency'},
            'delay': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'finish_task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'finish_task_set'", 'to': u"orm['gantt.Task']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'start_task_set'", 'to': u"orm['gantt.Task']"})
        },
        u'gantt.project': {
            'Meta': {'object_name': 'Project'},
            'duration': ('django.db.models.fields.FloatField', [], {}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'resources': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'work_on'", 'symmetrical': 'False', 'to': u"orm['gantt.Resource']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'gantt.resource': {
            'Meta': {'object_name': 'Resource'},
            'assigned_to': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gantt.Task']", 'through': u"orm['gantt.Assignment']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'gantt.task': {
            'Meta': {'object_name': 'Task'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'depends_on': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gantt.Task']", 'through': u"orm['gantt.Dependency']", 'symmetrical': 'False'}),
            'duration': ('django.db.models.fields.FloatField', [], {}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'grafted_task_set'", 'null': 'True', 'to': u"orm['gantt.Task']"}),
            'progress': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gantt.Project']"}),
            'row_index': ('django.db.models.fields.IntegerField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "('OPN', 'OPEN')", 'max_length': '50'})
        }
    }

    complete_apps = ['gantt']