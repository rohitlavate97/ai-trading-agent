import asyncio
from db.database import async_session_factory
from services.user_service import get_user_by_email, create_user
from schemas.user import UserCreate
from models.user import RoleEnum
from core.config import settings

async def seed_users():
    async with async_session_factory() as db:
        # Seed Admin
        admin_email = "admin@example.com"
        admin = await get_user_by_email(db, email=admin_email)
        if not admin:
            print(f"Creating admin user {admin_email}...")
            await create_user(
                db, 
                UserCreate(
                    email=admin_email, 
                    password="adminpassword", 
                    role=RoleEnum.ADMIN
                )
            )
        else:
            print(f"Admin {admin_email} already exists.")

        # Seed standard user
        user_email = "user@example.com"
        user = await get_user_by_email(db, email=user_email)
        if not user:
            print(f"Creating standard user {user_email}...")
            await create_user(
                db, 
                UserCreate(
                    email=user_email, 
                    password="userpassword", 
                    role=RoleEnum.USER
                )
            )
        else:
            print(f"User {user_email} already exists.")

async def main():
    print("Starting database seeding...")
    await seed_users()
    print("Database seeding completed.")

if __name__ == "__main__":
    asyncio.run(main())
