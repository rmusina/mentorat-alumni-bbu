# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Profile'
        db.create_table('profiles_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('previous_surname', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('CNP', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('home_town', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('graduated_college', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('hobbies', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('self_evaluation', self.gf('django.db.models.fields.TextField')()),
            ('extra_info', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('profiles', ['Profile'])

        # Adding model 'StudentProfile'
        db.create_table('profiles_studentprofile', (
            ('profile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['profiles.Profile'], unique=True, primary_key=True)),
            ('birthplace', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('faculty', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('current_degree', self.gf('django.db.models.fields.CharField')(default='bs', max_length=10)),
            ('year_of_study', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('major', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('town_of_study', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('employer_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('employer_address', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('employee_position', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('employee_duties', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('future_plans', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('how_mentor_can_help', self.gf('django.db.models.fields.TextField')()),
            ('mentor_expectations', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('profiles', ['StudentProfile'])

        # Adding model 'MentorProfile'
        db.create_table('profiles_mentorprofile', (
            ('profile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['profiles.Profile'], unique=True, primary_key=True)),
            ('graduated_faculty', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('graduated_major', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('graduation_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2010, 11, 17, 13, 22, 33, 500395), null=True)),
            ('employer_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('employer_address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('employee_position', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('employee_duties', self.gf('django.db.models.fields.TextField')()),
            ('mentorship_place', self.gf('django.db.models.fields.TextField')()),
            ('post_bachelors_studies', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('professional_experience', self.gf('django.db.models.fields.TextField')()),
            ('other_mentorship_activities', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('profiles', ['MentorProfile'])

        # Adding model 'FieldOfInterest'
        db.create_table('profiles_fieldofinterest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('profiles', ['FieldOfInterest'])

        # Adding model 'FieldOfInterest_Profile'
        db.create_table('profiles_fieldofinterest_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fields_of_interest', to=orm['profiles.Profile'])),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(related_name='profile', to=orm['profiles.FieldOfInterest'])),
        ))
        db.send_create_signal('profiles', ['FieldOfInterest_Profile'])

        # Adding model 'VolunteerOrganization'
        db.create_table('profiles_volunteerorganization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='volunteer', null=True, to=orm['profiles.Profile'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('profiles', ['VolunteerOrganization'])

        # Adding model 'StudentEmployment'
        db.create_table('profiles_studentemployment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(related_name='work_experience', to=orm['profiles.StudentProfile'])),
            ('internship', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('employer_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('duties', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('profiles', ['StudentEmployment'])

        # Adding model 'StudentResearch'
        db.create_table('profiles_studentresearch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(related_name='research', to=orm['profiles.StudentProfile'])),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('duties', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('profiles', ['StudentResearch'])

        # Adding model 'MentorshipActivities'
        db.create_table('profiles_mentorshipactivities', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('profiles', ['MentorshipActivities'])

        # Adding model 'MentorshipActivities_Mentor'
        db.create_table('profiles_mentorshipactivities_mentor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mentor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mentorship_activities', to=orm['profiles.MentorProfile'])),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mentor', to=orm['profiles.MentorshipActivities'])),
        ))
        db.send_create_signal('profiles', ['MentorshipActivities_Mentor'])

        # Adding model 'CommunicationMethod'
        db.create_table('profiles_communicationmethod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('profiles', ['CommunicationMethod'])

        # Adding model 'CommunicationRating'
        db.create_table('profiles_communicationrating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='communication_ratings', to=orm['profiles.Profile'])),
            ('ratting', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('method', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ratings', to=orm['profiles.CommunicationMethod'])),
        ))
        db.send_create_signal('profiles', ['CommunicationRating'])

        # Adding model 'Event'
        db.create_table('profiles_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 11, 17, 13, 22, 33, 512673))),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('profiles', ['Event'])

        # Adding model 'StudentEvent'
        db.create_table('profiles_studentevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(related_name='student_events', to=orm['profiles.StudentProfile'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='student_events', to=orm['profiles.Event'])),
        ))
        db.send_create_signal('profiles', ['StudentEvent'])


    def backwards(self, orm):
        
        # Deleting model 'Profile'
        db.delete_table('profiles_profile')

        # Deleting model 'StudentProfile'
        db.delete_table('profiles_studentprofile')

        # Deleting model 'MentorProfile'
        db.delete_table('profiles_mentorprofile')

        # Deleting model 'FieldOfInterest'
        db.delete_table('profiles_fieldofinterest')

        # Deleting model 'FieldOfInterest_Profile'
        db.delete_table('profiles_fieldofinterest_profile')

        # Deleting model 'VolunteerOrganization'
        db.delete_table('profiles_volunteerorganization')

        # Deleting model 'StudentEmployment'
        db.delete_table('profiles_studentemployment')

        # Deleting model 'StudentResearch'
        db.delete_table('profiles_studentresearch')

        # Deleting model 'MentorshipActivities'
        db.delete_table('profiles_mentorshipactivities')

        # Deleting model 'MentorshipActivities_Mentor'
        db.delete_table('profiles_mentorshipactivities_mentor')

        # Deleting model 'CommunicationMethod'
        db.delete_table('profiles_communicationmethod')

        # Deleting model 'CommunicationRating'
        db.delete_table('profiles_communicationrating')

        # Deleting model 'Event'
        db.delete_table('profiles_event')

        # Deleting model 'StudentEvent'
        db.delete_table('profiles_studentevent')


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
        'profiles.communicationmethod': {
            'Meta': {'object_name': 'CommunicationMethod'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profiles.communicationrating': {
            'Meta': {'object_name': 'CommunicationRating'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'to': "orm['profiles.CommunicationMethod']"}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'communication_ratings'", 'to': "orm['profiles.Profile']"}),
            'ratting': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'profiles.event': {
            'Meta': {'object_name': 'Event'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 11, 17, 13, 22, 33, 512673)'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'profiles.fieldofinterest': {
            'Meta': {'object_name': 'FieldOfInterest'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profiles.fieldofinterest_profile': {
            'Meta': {'object_name': 'FieldOfInterest_Profile'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'to': "orm['profiles.FieldOfInterest']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fields_of_interest'", 'to': "orm['profiles.Profile']"})
        },
        'profiles.mentorprofile': {
            'Meta': {'object_name': 'MentorProfile', '_ormbases': ['profiles.Profile']},
            'employee_duties': ('django.db.models.fields.TextField', [], {}),
            'employee_position': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'employer_address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'employer_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'graduated_faculty': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'graduated_major': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'graduation_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2010, 11, 17, 13, 22, 33, 500395)', 'null': 'True'}),
            'mentorship_place': ('django.db.models.fields.TextField', [], {}),
            'other_mentorship_activities': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'post_bachelors_studies': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'professional_experience': ('django.db.models.fields.TextField', [], {}),
            'profile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['profiles.Profile']", 'unique': 'True', 'primary_key': 'True'})
        },
        'profiles.mentorshipactivities': {
            'Meta': {'object_name': 'MentorshipActivities'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profiles.mentorshipactivities_mentor': {
            'Meta': {'object_name': 'MentorshipActivities_Mentor'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mentor'", 'to': "orm['profiles.MentorshipActivities']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mentor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mentorship_activities'", 'to': "orm['profiles.MentorProfile']"})
        },
        'profiles.profile': {
            'CNP': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'Meta': {'object_name': 'Profile'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'extra_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'graduated_college': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'hobbies': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'home_town': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'previous_surname': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'self_evaluation': ('django.db.models.fields.TextField', [], {}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'profiles.studentemployment': {
            'Meta': {'object_name': 'StudentEmployment'},
            'duties': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'employer_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internship': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'work_experience'", 'to': "orm['profiles.StudentProfile']"})
        },
        'profiles.studentevent': {
            'Meta': {'object_name': 'StudentEvent'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student_events'", 'to': "orm['profiles.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student_events'", 'to': "orm['profiles.StudentProfile']"})
        },
        'profiles.studentprofile': {
            'Meta': {'object_name': 'StudentProfile', '_ormbases': ['profiles.Profile']},
            'birthplace': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'current_degree': ('django.db.models.fields.CharField', [], {'default': "'bs'", 'max_length': '10'}),
            'employee_duties': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'employee_position': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'employer_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'employer_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'faculty': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'future_plans': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'how_mentor_can_help': ('django.db.models.fields.TextField', [], {}),
            'major': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mentor_expectations': ('django.db.models.fields.TextField', [], {}),
            'profile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['profiles.Profile']", 'unique': 'True', 'primary_key': 'True'}),
            'town_of_study': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'year_of_study': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'profiles.studentresearch': {
            'Meta': {'object_name': 'StudentResearch'},
            'duties': ('django.db.models.fields.TextField', [], {}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'research'", 'to': "orm['profiles.StudentProfile']"})
        },
        'profiles.volunteerorganization': {
            'Meta': {'object_name': 'VolunteerOrganization'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'volunteer'", 'null': 'True', 'to': "orm['profiles.Profile']"})
        }
    }

    complete_apps = ['profiles']
