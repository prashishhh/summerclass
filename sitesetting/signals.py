from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from . models import SiteSetting
from utils.media_cleanup import delete_file_on_delete, delete_old_file_on_update

@receiver(pre_save, sender=SiteSetting)
def blog_image_update_cleanup(sender, instance, **kwargs):
    delete_old_file_on_update(instance, SiteSetting, 'logo')
    delete_old_file_on_update(instance, SiteSetting, 'favicon')


@receiver(post_delete, sender=SiteSetting)
def blog_image_delete_cleanup(sender, instance, **kwargs):
    delete_file_on_delete(instance, 'logo')
    delete_file_on_delete(instance, 'favicon')