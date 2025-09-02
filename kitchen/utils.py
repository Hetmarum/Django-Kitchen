from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.views.generic.base import ContextMixin


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


class ConfirmDeleteMixin(ContextMixin):
    template_name = "confirm_delete.html"
    object_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_name"] = (
            self.object_name or self.model._meta.verbose_name.title()
        )
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", self.get_success_url()
        )
        return context


class FormTemplateMixin(ContextMixin):
    template_name = "kitchen/form.html"
    object_name = None
    multipart = False
    extra_scripts = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_name"] = (
            self.object_name or self.model._meta.verbose_name.title()
        )
        context["multipart"] = self.multipart
        context["extra_scripts"] = self.extra_scripts
        return context
