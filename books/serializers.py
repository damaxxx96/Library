from rest_framework import serializers


class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=30)
    author = serializers.CharField(max_length=50)
    genre = serializers.CharField(max_length=20)
    pub_date = serializers.DateTimeField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("bookshelf", None)
        representation.pop("user", None)
        return representation
