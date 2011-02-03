/* ADD mentor visibility to profile */
ALTER TABLE profiles_mentorprofile ADD visible_to_mentors BIT NOT NULL DEFAULT(0);
