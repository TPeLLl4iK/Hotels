import asyncio
import os
from time import sleep

from PIL import Image

from src.api.dependencies import DBManager
from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance


@celery_instance.task
def test_task():
    sleep(5)
    print('Done')

@celery_instance.task
def resize_and_save_image(source_path: str) -> list[str]:

    output_dir = 'src/static/images'
    widths = (1000, 500, 200)

    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.basename(source_path)
    name, ext = os.path.splitext(filename)

    saved_paths = []

    with Image.open(source_path) as img:
        if img.mode in ("RGBA", "P") and ext.lower() in (".jpg", ".jpeg"):
            img = img.convert("RGB")

        original_width, original_height = img.size

        for width in widths:
            target_width = min(width, original_width)
            ratio = target_width / original_width
            target_height = round(original_height * ratio)

            resized_img = img.resize((target_width, target_height), Image.LANCZOS)

            output_path = os.path.join(output_dir, f"{name}_{width}{ext}")
            resized_img.save(output_path)
            saved_paths.append(output_path)

    return saved_paths

async def get_booking_with_today_checkin_helper():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.bookings.get_booking_with_today_checkin()


@celery_instance.task(name='booking_today_checkin')
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_booking_with_today_checkin_helper)