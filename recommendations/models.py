from django.db import models

from contracts.models import Contract
from tenders.models import Tender
from hupleruser.models import HuplerUser


# Create your models here.
class RecommendedContracts(models.Model):
    """
    List of recommended contracts for the given user
    """
    contracts = models.ManyToManyField(Contract, related_name='recommended_contracts')
    user = models.ForeignKey(HuplerUser, related_name='recommended_contracts', on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f"{self.user.username}'s recommended contracts"


class RecommendedTenders(models.Model):
    """
    List of recommended tenders for the given user
    """
    tenders = models.ManyToManyField(Tender, related_name='recommended_tenders')
    user = models.ForeignKey(HuplerUser, related_name='recommended_tenders', on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f"{self.user.username}'s recommended tenders"
