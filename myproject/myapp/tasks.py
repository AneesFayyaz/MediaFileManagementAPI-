from celery import shared_task
from .models import mediaFileData
import time

@shared_task
def save_media_file_properties(media_file_data_id): 
    print('inside the tasks.py')
    time.sleep(300)
    try:
        print('inside the try block tasks.py')
        # Fetch the media file data instance
        media_file_data = mediaFileData.objects.get(id=media_file_data_id)
        file = media_file_data.media_file.file
        print('after getting file of  try block tasks.py')

        # Extract file properties
        media_file_data.name = file.name
        media_file_data.size = file.size
        media_file_data.extension = file.name.split('.')[-1]

        # Save the extracted properties
        media_file_data.save()
        print('after saving try block tasks.py')

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise e