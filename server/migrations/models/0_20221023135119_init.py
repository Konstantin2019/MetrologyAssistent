from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "admin" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "token" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "teachers" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "teacher_name" VARCHAR(32) NOT NULL
);
CREATE TABLE IF NOT EXISTS "test_types" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "test_name" VARCHAR(16) NOT NULL
);
CREATE TABLE IF NOT EXISTS "years" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "year_name" INT NOT NULL
);
CREATE TABLE IF NOT EXISTS "student_groups" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "group_name" VARCHAR(12) NOT NULL,
    "year_id" INT NOT NULL REFERENCES "years" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "students" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
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
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "index" INT,
    "question" TEXT,
    "student_answer" TEXT,
    "correct_answer" TEXT,
    "score" INT,
    "image_url" VARCHAR(64),
    "student_id" INT NOT NULL REFERENCES "students" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "rk2" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "index" INT,
    "question" TEXT,
    "student_answer" TEXT,
    "correct_answer" TEXT,
    "score" INT,
    "image_url" VARCHAR(64),
    "student_id" INT NOT NULL REFERENCES "students" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "tests" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "index" INT,
    "question" TEXT,
    "student_answer" TEXT,
    "correct_answer" TEXT,
    "score" INT,
    "image_url" VARCHAR(64),
    "student_id" INT NOT NULL REFERENCES "students" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
