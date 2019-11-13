from django.db import models

from contracts.models import Contract
from tenders.models import Tender
from hupleruser.models import HuplerUser


# Create your models here.
class BookmarkedContract(models.Model):
    """
    When a user saves a contract, it creates a bookmark. If the user deletes
    a bookmark, the bookmark is set to inactive.
    """
    contract = models.ForeignKey(Contract, related_name='bookmarked_contracts', on_delete=models.CASCADE)
    user = models.ForeignKey(HuplerUser, related_name='contract_bookmarks', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('contract', 'user',)

    def __str__(self):
        return "{0}'s bookmark on {1}".format(self.user, self.contract)


class BookmarkedTender(models.Model):
    tender = models.ForeignKey(Tender, related_name='bookmarked_tender', on_delete=models.CASCADE)
    user = models.ForeignKey(HuplerUser, related_name='tender_bookmarks', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('tender', 'user',)

    def __str__(self):
        return "{0}'s bookmark on {1}".format(self.user, self.tender)
