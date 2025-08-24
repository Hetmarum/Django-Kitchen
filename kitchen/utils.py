from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

def resize_image(image_field, size=(400, 200), quality=80):
    """
    Resize and compress uploaded image.
    - size: max width/height
    - quality: JPEG compression (lower = smaller file)
    """
    img = Image.open(image_field)
    img = img.convert("RGB")
    img.thumbnail(size, Image.Resampling.LANCZOS)

    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=quality, optimize=True)
    return ContentFile(buffer.getvalue())
