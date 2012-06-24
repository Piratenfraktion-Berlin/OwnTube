# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'FunctionTask.function_name'
        db.alter_column('djangotasks_functiontask', 'function_name', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True))


    def backwards(self, orm):
        
        # Changing field 'FunctionTask.function_name'
        db.alter_column('djangotasks_functiontask', 'function_name', self.gf('django.db.models.fields.CharField')(max_length=400, primary_key=True))


    models = {
        'djangotasks.functiontask': {
            'Meta': {'object_name': 'FunctionTask'},
            'function_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        },
        'djangotasks.task': {
            'Meta': {'object_name': 'Task'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'defined'", 'max_length': '200'})
        }
    }

    complete_apps = ['djangotasks']
