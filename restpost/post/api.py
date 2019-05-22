import short_url

from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import serializers, viewsets, permissions

from post.models import Post, Like


class IsAuthorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class AutopopulateAuthorMixin:
    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except IntegrityError:
            raise serializers.ValidationError('You can like post only once!')


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(
        source='get_likes_count',
        read_only=True
    )
    short_url = serializers.SerializerMethodField()
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'url', 'title', 'text', 'author', 'created', 'likes',
                  'short_url')
        read_only_fields = ('created', 'id')

    def get_short_url(self, obj):
        return self.context['request'].build_absolute_uri(reverse('short_url', kwargs={
            'hash': short_url.encode_url(obj.pk)
        }))


class PostViewSet(AutopopulateAuthorMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorPermission)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'url', 'post', 'created')
        read_only_fields = ('id', 'created')

    def get_queryset(self):
        return Like.objects.filter(author=self.request.user)


class LikeViewSet(AutopopulateAuthorMixin, viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorPermission)
