from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "rk1" ADD "answer_image" BYTEA;
        ALTER TABLE "rk2" ADD "answer_image" BYTEA;
        ALTER TABLE "tests" ADD "answer_image" BYTEA;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "rk1" DROP COLUMN "answer_image";
        ALTER TABLE "rk2" DROP COLUMN "answer_image";
        ALTER TABLE "tests" DROP COLUMN "answer_image";"""
