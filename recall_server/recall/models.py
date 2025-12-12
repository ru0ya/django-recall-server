"""
This module defines models for the `recall` Django app.
"""


from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from recall_server.common.mixins import OwnerlessAbstract

User = get_user_model()


STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('gathering_signatures', 'Gathering Signatures'),
       ('under_review', 'Under Review'),
       ('approved', 'Approved'),
       ('rejected', 'Rejected')
    ]



class Recall(OwnerlessAbstract):
    """
    Custom model to represent a recall for the `recall` Django app.
    """
    
    recaller = models.ForeignKey(
        User,
        related_name="initiated_recalls",
        on_delete=models.CASCADE,
    )
    recalled_mp = models.ForeignKey(
        'mps.MemberOfParliament',
        related_name="recalls",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    recalled_senator = models.ForeignKey(
        'county.Senator',
        related_name="recalls",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    recalled_mca = models.ForeignKey(
        'county.MCA',
        related_name="recalls",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    recall_supporters = models.ManyToManyField(
        User,
        related_name="supported_recalls",
        blank=True,
    )
    recall_reasons = models.TextField()
    constituency = models.ForeignKey(
        'county.Constituency',
        related_name="recalls",
        on_delete=models.CASCADE,
    )
    county = models.ForeignKey(
        'county.County',
        related_name="recalls",
        on_delete=models.CASCADE,
    )
    ward = models.ForeignKey(
        'county.Ward',
        related_name="recalls",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='initiated'
    )
    signature_threshold = models.PositiveIntegerField(default=0)
    current_signature_count = models.PositiveIntegerField(default=0)
    
    
    def update_signature_count(self):
        self.current_signature_count = self.recall_supporters.count()
        self.save()
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # ensures that only one of recalled_mp, recalled_senator, or recalled_mca is set
        
        # Count how many legislator fields are set
        legislators_set = sum([
            bool(self.recalled_mp),
            bool(self.recalled_senator),
            bool(self.recalled_mca)
        ])
        
        if legislators_set == 0:
            raise ValidationError("You must specify legislator to recall (MP, Senator, or MCA)")
        
        if legislators_set > 1:
            raise ValidationError("You can only recall one legislator at a time")
        
        if self.recaller and hasattr(self.recaller, 'voter_profile'):
            profile = self.recaller.voter_profile
            
            if self.recalled_mp and profile.constituency != self.constituency:
                    raise ValidationError("You can only recall an MP from your constituency")
            if self.recalled_senator and profile.county != self.county:
                    raise ValidationError("You can only recall a Senator from your county")
        
            if self.recalled_mca and profile.ward != self.ward:
                    raise ValidationError("You can only recall an MCA from your ward")
        
    def get_recalled_legislator(self):
        """Return the legislator being recalled"""
        if self.recalled_mp:
            return self.recalled_mp
        elif self.recalled_senator:
            return self.recalled_senator
        elif self.recalled_mca:
            return self.recalled_mca
        return None
    
    def  get_legislator_type(self):
        """Returns the type of legislator being recalled"""
        if self.recalled_mp:
            return 'MP'
        elif self.recalled_senator:
            return 'Senator'
        elif self.recalled_mca:
            return 'MCA'
        return None
    
    def can_add_supporter(self, user):
        """Check if a user can support this recall"""
        if not hasattr(user, 'voter_profile'):
            return False
        
        profile = user.voter_profile
        
        if self.recalled_mp:
            return profile.constituency == self.constituency
        elif self.recalled_senator:
            return profile.county == self.county
        elif self.recalled_mca:
            return profile.ward == self.ward
        return False
        


    def __str__(self):
        if self.recalled_mp:
            return f"{self.recalled_mp} recalled by {self.recaller}"
        elif self.recalled_senator:
            return f"{self.recalled_senator} recalled by {self.recaller}"
        elif self.recalled_mca:
            return f"{self.recalled_mca} recalled by {self.recaller}"
        
    
    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['constituency']),
            models.Index(fields=['county']),
            models.Index(fields=['ward']),
            models.Index(fields=['recaller']),
        ]
