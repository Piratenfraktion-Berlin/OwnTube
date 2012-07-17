# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Video'
        db.create_table('videoportal_video', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from=None, unique_with=())),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('protocolURL', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('kind', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('torrentURL', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('mp4URL', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('mp4Size', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('webmURL', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('webmSize', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('mp3URL', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('mp3Size', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('oggURL', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('oggSize', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('videoThumbURL', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('duration', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('encodingDone', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('assemblyid', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('originalFile', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('videoportal', ['Video'])

        # Adding model 'Comment'
        db.create_table('videoportal_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('moderated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timecode', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['videoportal.Video'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('videoportal', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'Video'
        db.delete_table('videoportal_video')

        # Deleting model 'Comment'
        db.delete_table('videoportal_comment')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        },
        'videoportal.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'timecode': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['videoportal.Video']"})
        },
        'videoportal.video': {
            'Meta': {'object_name': 'Video'},
            'assemblyid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'duration': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'encodingDone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'mp3Size': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mp3URL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'mp4Size': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mp4URL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'oggSize': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'oggURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'originalFile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'protocolURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'torrentURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'videoThumbURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'webmSize': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'webmURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['videoportal']