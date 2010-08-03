# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Metadata'
        db.create_table('creators_metadata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('creators', ['Metadata'])

        # Adding model 'Asset'
        db.create_table('creators_asset', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('creators', ['Asset'])

        # Adding model 'Floor'
        db.create_table('creators_floor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['creators.Asset'], null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
        ))
        db.send_create_signal('creators', ['Floor'])

        # Adding model 'Room'
        db.create_table('creators_room', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['creators.Asset'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('room_type', self.gf('django.db.models.fields.CharField')(default='normal', max_length=8)),
            ('x', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('y', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('width', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('height', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('floor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['creators.Floor'])),
        ))
        db.send_create_signal('creators', ['Room'])

        # Adding model 'Creator'
        db.create_table('creators_creator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['creators.Asset'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('theme', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('creators', ['Creator'])

        # Adding model 'EventType'
        db.create_table('creators_eventtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('is_static', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('creators', ['EventType'])

        # Adding model 'Event'
        db.create_table('creators_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['creators.Asset'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['creators.Creator'])),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['creators.Room'])),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['creators.EventType'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('detail_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('creators', ['Event'])

        # Adding model 'Status'
        db.create_table('creators_status', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='dead', max_length=5)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 8, 3, 14, 12, 24, 149025))),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('creators', ['Status'])

        # Adding unique constraint on 'Status', fields ['status', 'author']
        db.create_unique('creators_status', ['status', 'author'])

        # Adding model 'PartyUser'
        db.create_table('creators_partyuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('api_key', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('checkin_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('x', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('y', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('current_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['creators.Status'], null=True, blank=True)),
            ('current_floor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['creators.Floor'], null=True, blank=True)),
            ('current_room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['creators.Room'], null=True, blank=True)),
        ))
        db.send_create_signal('creators', ['PartyUser'])

        # Adding M2M table for field friends on 'PartyUser'
        db.create_table('creators_partyuser_friends', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_partyuser', models.ForeignKey(orm['creators.partyuser'], null=False)),
            ('to_partyuser', models.ForeignKey(orm['creators.partyuser'], null=False))
        ))
        db.create_unique('creators_partyuser_friends', ['from_partyuser_id', 'to_partyuser_id'])

        # Adding M2M table for field events on 'PartyUser'
        db.create_table('creators_partyuser_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partyuser', models.ForeignKey(orm['creators.partyuser'], null=False)),
            ('event', models.ForeignKey(orm['creators.event'], null=False))
        ))
        db.create_unique('creators_partyuser_events', ['partyuser_id', 'event_id'])

        # Adding model 'Photo'
        db.create_table('creators_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(default='dead', max_length=4)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
        ))
        db.send_create_signal('creators', ['Photo'])


    def backwards(self, orm):
        
        # Deleting model 'Metadata'
        db.delete_table('creators_metadata')

        # Deleting model 'Asset'
        db.delete_table('creators_asset')

        # Deleting model 'Floor'
        db.delete_table('creators_floor')

        # Deleting model 'Room'
        db.delete_table('creators_room')

        # Deleting model 'Creator'
        db.delete_table('creators_creator')

        # Deleting model 'EventType'
        db.delete_table('creators_eventtype')

        # Deleting model 'Event'
        db.delete_table('creators_event')

        # Deleting model 'Status'
        db.delete_table('creators_status')

        # Removing unique constraint on 'Status', fields ['status', 'author']
        db.delete_unique('creators_status', ['status', 'author'])

        # Deleting model 'PartyUser'
        db.delete_table('creators_partyuser')

        # Removing M2M table for field friends on 'PartyUser'
        db.delete_table('creators_partyuser_friends')

        # Removing M2M table for field events on 'PartyUser'
        db.delete_table('creators_partyuser_events')

        # Deleting model 'Photo'
        db.delete_table('creators_photo')


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
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'creators.event': {
            'Meta': {'object_name': 'Event'},
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
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 8, 3, 14, 12, 24, 149025)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'dead'", 'max_length': '5'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        }
    }

    complete_apps = ['creators']
