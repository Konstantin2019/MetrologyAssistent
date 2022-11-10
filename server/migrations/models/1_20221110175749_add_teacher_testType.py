from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "teachers" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "teacher_name" VARCHAR(32) NOT NULL,
    "rk1_time" INT,
    "rk2_time" INT,
    "test_time" INT
);;
        CREATE TABLE IF NOT EXISTS "test_types" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "test_name" VARCHAR(12) NOT NULL
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "teachers";
        DROP TABLE IF EXISTS "test_types";"""
