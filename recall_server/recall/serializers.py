"""
Model serializers for the `recall` Django app.
"""

from recall_server.recall.models import Recall
from rest_framework import serializers


class RecallSerializer(serializers.ModelSerializer):
    """
    Serializer to serialize/deserialize instances of the `Recall` model.
    """
    legislator_type = serializers.SerializerMethodField()
    legislator_name = serializers.SerializerMethodField()

    class Meta:
        model = Recall
        fields = [
            "created_at",
            "updated_at",
            "recalled_mp",
            "recalled_senator",
            "recalled_mca",
            "recaller",
            "recall_supporters",
            "recall_reasons",
            "legislator_type",
            "legislator_name",
            "constituency",
            "county",
            "ward",
            "status",
            "current_signature_count"
        ]
        read_only_fields = ["created_at", "updated_at", "current_signature_count"]
        
    def get_legislator_type(self, obj):
        return obj.get_legislator_type()
    
    def get_legislator_name(self, obj):
        return obj.get_legislator_name()
    
    def validate(self, data):
        legislators = [data.get('recalled_mp'), data.get('recalled_senator'), data.get('recalled_mca')]
        if sum(bool(x) for x in legislators) != 1:
            raise serializers.ValidationError("You must specify exactly one legislator to recall")
        
        return data
