/* ADD mentor visibility to profile */
ALTER TABLE profiles_mentorprofile ADD visible_to_mentors BIT NOT NULL DEFAULT(0);
ALTER TABLE profiles_studentprofile DROP COLUMN mentor_expectations;
/* ADDS foreign key relation to MentoringAgreement in Friendship */
ALTER TABLE friends_friendship ADD COLUMN mentoring_agreement_id INT UNIQUE;
ALTER TABLE friends_friendship ADD CONSTRAINT fk_1 FOREIGN KEY (mentoring_agreement_id) REFERENCES friends_mentoringagreement (id); 
