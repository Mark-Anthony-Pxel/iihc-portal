from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import os

def validate_file(file):
    # Define the allowed extensions for images and attachments
    allowed_image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    allowed_attachment_extensions = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.txt']

    # Get the file extension
    ext = os.path.splitext(file.name)[1].lower()

    # Check if the file is an image
    if ext in allowed_image_extensions:
        # Check for image file size (e.g., limit to 10 MB)
        if file.size > 10 * 1024 * 1024:  # 10 MB
            raise ValidationError(_('Image file size must be under 10 MB.'))

    # Check if the file is an attachment
    elif ext in allowed_attachment_extensions:
        # Check for attachment file size (e.g., limit to 20 MB)
        if file.size > 20 * 1024 * 1024:  # 20 MB
            raise ValidationError(_('Attachment file size must be under 20 MB.'))

    else:
        raise ValidationError(_('Unsupported file type. Allowed types: JPG, JPEG, PNG, GIF for images; PDF, DOC, DOCX, PPT, PPTX, TXT for attachments.'))