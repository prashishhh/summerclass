from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Account
from utils.media_cleanup import delete_old_file_on_update, delete_file_on_delete

@receiver(pre_save, sender=Account)
def profile_picture_update_cleanup(sender, instance, **kwargs):
    delete_old_file_on_update(instance, Account, 'profile_picture')

@receiver(post_delete, sender=Account)
def profile_picture_delete_cleanup(sender, instance, **kwargs):
    delete_file_on_delete(instance, 'profile_picture')
