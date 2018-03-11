CREATE TABLE "questions" (
  id SERIAL NOT NULL PRIMARY KEY,
  question_text VARCHAR(200) NOT NULL,
  pub_date TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE "choices" (
  id SERIAL NOT NULL PRIMARY KEY,
  choice_text VARCHAR(200) NOT NULL,
  votes INTEGER NOT NULL,
  question_id INTEGER,
  CONSTRAINT fk_questions FOREIGN KEY (question_id) REFERENCES questions (id)
);
