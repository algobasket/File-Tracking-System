import os
from django.http import HttpResponse, FileResponse
from django.conf import settings

def download_file(file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = FileResponse(file)
            # Set the content type for the response based on the file's extension
            _, file_extension = os.path.splitext(file_path)
            content_type = 'application/octet-stream'  # Default content type
            if file_extension.lower() == '.pdf':
                content_type = 'application/pdf'
            elif file_extension.lower() in ['.doc', '.docx']:
                content_type = 'application/msword'
            elif file_extension.lower() == '.png':
                content_type = 'image/png'
            elif file_extension.lower() == '.jpg':
                content_type = 'image/jpeg'

            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            response['Content-Type'] = content_type
            return response
    else:
        # File does not exist
        return HttpResponse("File not found", status=404)