# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Floor.touchscreen_floor'
        db.add_column('creators_floor', 'touchscreen_floor', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Floor.touchscreen_floor'
        db.delete_column('creators_floor', 'touchscreen_floor')


    models = {
        'creators.asset': {
            'Meta': {'object_name': 'Asset'},
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'})
        },
        'creators.creator': {
            'Meta': {'object_name': 'Creator'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['creators.Asset']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'video_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'})
        },
        'creators.event': {
            'Meta': {'object_name': 'Event'},
            'all_day': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['creators.Creator']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'detail_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['creators.EventType']"}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['creators.Asset']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['creators.Room']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        'creators.eventtype': {
            'Meta': {'object_name': 'EventType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_static': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'creators.floor': {
            'Meta': {'object_name': 'Floor'},
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['creators.Asset']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'touchscreen_floor': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'creators.metadata': {
            'Meta': {'object_name': 'Metadata'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'})
        },
        'creators.partyuser': {
            'Meta': {'object_name': 'PartyUser'},
            'api_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'checkin_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_floor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['creators.Floor']", 'null': 'True', 'blank': 'True'}),
            'current_room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['creators.Room']", 'null': 'True', 'blank': 'True'}),
            'current_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['creators.Status']", 'null': 'True', 'blank': 'True'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['creators.Event']", 'null': 'True', 'blank': 'True'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['creators.PartyUser']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'x': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'creators.photo': {
            'Meta': {'object_name': 'Photo'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'dead'", 'max_length': '4'})
        },
        'creators.room': {
            'Meta': {'object_name': 'Room'},
            'floor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['creators.Floor']"}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['creators.Asset']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'room_type': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '8'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'x': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'creators.status': {
            'Meta': {'unique_together': "(('status', 'author'),)", 'object_name': 'Status'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 15, 19, 58, 41, 129262)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'dead'", 'max_length': '5'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        }
    }

    complete_apps = ['creators']
