from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "admin" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "years" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "year_name" INT NOT NULL
);
CREATE TABLE IF NOT EXISTS "student_groups" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "group_name" VARCHAR(12) NOT NULL,
    "year_id" INT NOT NULL REFERENCES "years" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "students" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(32) NOT NULL,
    "surname" VARCHAR(32) NOT NULL,
    "patronymic" VARCHAR(32),
    "email" VARCHAR(64) NOT NULL,
    "rk1_start_time" VARCHAR(64),
    "rk1_finish_time" VARCHAR(64),
    "rk2_start_time" VARCHAR(64),
    "rk2_finish_time" VARCHAR(64),
    "test_start_time" VARCHAR(64),
    "test_finish_time" VARCHAR(64),
    "group_id" INT NOT NULL REFERENCES "student_groups" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "rk1" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "index" INT,
    "question" TEXT,
    "student_answer" TEXT,
    "correct_answer" TEXT,
    "score" INT,
    "image_url" VARCHAR(64),
    "student_id" INT NOT NULL REFERENCES "students" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "rk2" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "index" INT,
    "question" TEXT,
    "student_answer" TEXT,
    "correct_answer" TEXT,
    "score" INT,
    "image_url" VARCHAR(64),
    "student_id" INT NOT NULL REFERENCES "students" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "tests" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "index" INT,
    "question" TEXT,
    "student_answer" TEXT,
    "correct_answer" TEXT,
    "score" INT,
    "image_url" VARCHAR(64),
    "student_id" INT NOT NULL REFERENCES "students" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
