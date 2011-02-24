/* ADD mentor visibility to profile */
ALTER TABLE profiles_mentorprofile ADD visible_to_mentors BIT NOT NULL DEFAULT(0);
ALTER TABLE profiles_studentprofile DROP COLUMN mentor_expectations;
