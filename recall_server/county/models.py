"""
Custom Database models for the `county` Django app.
"""
import uuid
from django.db import models


from recall_server.voting.models import Legislator, OfficialVote



class County(models.Model):
    """
    Keep track of county and number of constituencies.
    """

    name = models.CharField(unique=True, max_length=40)
    county_id= models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    county_number = models.CharField(max_length=3, unique=True, default=0)
    constituency_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}: {self.constituency_count}"


class Senator(Legislator):
    """ 
    Keep track of senators and their legislative activities
    """
    name = models.CharField(max_length=200)
    county = models.ForeignKey(
            County,
            on_delete=models.CASCADE,
            related_name='senators'
            )
    is_active = models.BooleanField(default=True)
    date_elected = models.DateField(null=True)
    term_end_date = models.DateField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_active'])
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['county', 'is_active'],
                condition=models.Q(is_active=True),
                name='unique_active_senator_per_county'
            )
        ]

    def __str__(self):
        return f"Senator {self.name} - {self.county}"

    @property
    def voting_history(self):
        return super().voting_history.select_related('bill')

    def is_term_active(self):
        from django.utils import timezone
        current_date = timezone.now().date()
        return self.is_active and self.date_elected <= current_date <= self.term_end_date


class Constituency(models.Model):
    """
    Keep track of constituency.
    """

    name = models.CharField(unique=True, max_length=20)
    constituency_id= models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registeredvoter_count = models.IntegerField(default=0)
    polling_station = models.ForeignKey(
        'polling_station.PollingStation',
        related_name="constituencies",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name} {self.registeredvoter_count} "


class Ward(models.Model):
    """
    Keep track of wards.
    """
    name = models.CharField(unique=True, max_length=20)
    ward_id= models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registeredvoter_count = models.IntegerField(default=0)
    polling_stations = models.ForeignKey(
        'polling_station.PollingStation',
        related_name="wards",
        on_delete=models.CASCADE,
    )   
    constituency = models.ForeignKey(
        'county.Constituency',
        related_name="wards",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name} {self.registeredvoter_count}"


class MCA(Legislator):
    """
    Keep track of MCAs and their ward representation
    """
    name = models.CharField(max_length=200)
    ward = models.CharField(max_length=200, unique=True)
    constituency = models.ForeignKey(
            Constituency,
            on_delete=models.CASCADE,
            related_name='mcas'
            )
    is_active = models.BooleanField(default=True)
    date_elected = models.DateField(null=True)
    term_end_date = models.DateField(null=True)

    class Meta:
        verbose_name = "MCA"
        verbose_name_plural = "MCAs"
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['ward']),
            models.Index(fields=['is_active'])
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['ward', 'is_active'],
                condition=models.Q(is_active=True),
                name='unique_active_mca_per_ward'
            )
        ]

    def __str__(self):
        return f"MCA {self.name} - {self.ward} ({self.constituency})"

    @property
    def voting_history(self):
        return super().voting_history.select_related('bill')

    def is_term_active(self):
        from django.utils import timezone
        current_date = timezone.now().date()
        return self.is_active and self.date_elected <= current_date <= self.term_end_date
