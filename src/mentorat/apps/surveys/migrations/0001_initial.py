# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Survey'
        db.create_table('surveys_survey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('for_students', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('for_mentors', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('surveys', ['Survey'])

        # Adding model 'TextField'
        db.create_table('surveys_textfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('index', self.gf('django.db.models.fields.IntegerField')()),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.Survey'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('surveys', ['TextField'])

        # Adding model 'BooleanField'
        db.create_table('surveys_booleanfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('index', self.gf('django.db.models.fields.IntegerField')()),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.Survey'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('surveys', ['BooleanField'])

        # Adding model 'ChoiceField'
        db.create_table('surveys_choicefield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('index', self.gf('django.db.models.fields.IntegerField')()),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.Survey'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('multichoice', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('surveys', ['ChoiceField'])

        # Adding model 'Choice'
        db.create_table('surveys_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.ChoiceField'])),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('surveys', ['Choice'])

        # Adding model 'TextFieldAnswer'
        db.create_table('surveys_textfieldanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.TextField'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('answer', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('surveys', ['TextFieldAnswer'])

        # Adding model 'BooleanFieldAnswer'
        db.create_table('surveys_booleanfieldanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.BooleanField'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('surveys', ['BooleanFieldAnswer'])

        # Adding model 'UserChoice'
        db.create_table('surveys_userchoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.Choice'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('surveys', ['UserChoice'])

        # Adding model 'CompletedSurvey'
        db.create_table('surveys_completedsurvey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.Survey'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('surveys', ['CompletedSurvey'])


    def backwards(self, orm):
        
        # Deleting model 'Survey'
        db.delete_table('surveys_survey')

        # Deleting model 'TextField'
        db.delete_table('surveys_textfield')

        # Deleting model 'BooleanField'
        db.delete_table('surveys_booleanfield')

        # Deleting model 'ChoiceField'
        db.delete_table('surveys_choicefield')

        # Deleting model 'Choice'
        db.delete_table('surveys_choice')

        # Deleting model 'TextFieldAnswer'
        db.delete_table('surveys_textfieldanswer')

        # Deleting model 'BooleanFieldAnswer'
        db.delete_table('surveys_booleanfieldanswer')

        # Deleting model 'UserChoice'
        db.delete_table('surveys_userchoice')

        # Deleting model 'CompletedSurvey'
        db.delete_table('surveys_completedsurvey')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'surveys.booleanfield': {
            'Meta': {'object_name': 'BooleanField'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['surveys.Survey']"})
        },
        'surveys.booleanfieldanswer': {
            'Meta': {'object_name': 'BooleanFieldAnswer'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['surveys.BooleanField']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'surveys.choice': {
            'Meta': {'object_name': 'Choice'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['surveys.ChoiceField']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'surveys.choicefield': {
            'Meta': {'object_name': 'ChoiceField'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'multichoice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['surveys.Survey']"})
        },
        'surveys.completedsurvey': {
            'Meta': {'object_name': 'CompletedSurvey'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['surveys.Survey']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'surveys.survey': {
            'Meta': {'object_name': 'Survey'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'for_mentors': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'for_students': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'surveys.textfield': {
            'Meta': {'object_name': 'TextField'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['surveys.Survey']"})
        },
        'surveys.textfieldanswer': {
            'Meta': {'object_name': 'TextFieldAnswer'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['surveys.TextField']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'surveys.userchoice': {
            'Meta': {'object_name': 'UserChoice'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['surveys.Choice']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['surveys']
