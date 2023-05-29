from data.dynamodb import *
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Deployment, Instrument


@receiver(post_save, sender=Instrument)
def create_simb3_deployment_instrument_creation(sender, instance, created, **kwargs):
    """
    This signal automatically creates a deployment instance when an instrument
    is created with instrument_type = 'SIMB3' and the user is_staff. Note: if we
    add internal instruments in the future that need an automatic deployment, this 
    will need to be modified.
    """
    if created and instance.instrument_type == 'SIMB3' and instance.internal:
        Deployment.objects.create(
            instrument=instance, deployment_number=0, name=instance.name + ' Deployment #1')


@receiver(post_save, sender=Deployment)
def create_dynamo_db_table_for_deployment(sender, instance, created, **kwargs):
    """
    Add a DynamoDB table when a new deployment is added
    """
    if created and not check_if_dynamodb_table_exists(str(instance.data_uuid)):
        response = create_dynamodb_table(str(instance.data_uuid))


@receiver(post_delete, sender=Deployment)
def delete_dynamo_db_table_for_deployment(sender, instance, **kwargs):
    """
    Remove the DynamoDB table when a deployment is deleted
    """
    response = delete_dynamodb_table(str(instance.data_uuid))
