# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Task.description'
        db.add_column(u'gantt_task', 'description',
                      self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Task.level'
        db.add_column(u'gantt_task', 'level',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Task.description'
        db.delete_column(u'gantt_task', 'description')

        # Deleting field 'Task.level'
        db.delete_column(u'gantt_task', 'level')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'gantt.task': {
            'Meta': {'object_name': 'Task'},
            'assigned_to': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gantt.Resource']", 'through': u"orm['gantt.Assignment']", 'symmetrical': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'depends_on': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gantt.Task']", 'through': u"orm['gantt.Dependency']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.FloatField', [], {}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
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