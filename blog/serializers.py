from rest_framework import serializers
from blog.models import BlogPost, Category, Comment


class BlogSerializer(serializers.ModelSerializer):

    # Specify that category is a CharField instead of CategorySerializer
    category = serializers.CharField()

    class Meta:
        model = BlogPost
        fields = ('id', 'author', 'title',
                  'content', 'category', 'image',
                  'status', 'created_on', 'updated_on')
        read_only_fields = ('id', 'author', 'created_on', 'updated_on')

    def create(self, validated_data):
        # Get the category data from validated_data and remove it from the dict
        category_data = validated_data.pop('category')

        # Get or create the Category object using the category name
        category = Category.objects.get_or_create(name=category_data)[0]

        # Create the BlogPost object with the category and validated_data
        blog = BlogPost.objects.create(category=category, **validated_data)
        return blog

    def update(self, instance, validated_data):
        """
        Update the instance fields with the validated data,
        or leave them unchanged if not provided
        """
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.status = validated_data.get('status', instance.status)
        instance.image = validated_data.get('image', instance.image)

        # Retrieve the Category instance using the provided category name
        category_name = validated_data.get('category', instance.category.name)
        category = Category.objects.get_or_create(name=category_name)[0]
        instance.category = category

        # Save the updated instance
        instance.save()

        # Return the updated instance
        return instance


class CommentSerializer(serializers.ModelSerializer):
    # Specify the queryset for the `blog_post` field as all BlogPost objects
    blog_post = serializers.PrimaryKeyRelatedField(
                queryset=BlogPost.objects.all())

    class Meta:
        model = Comment
        # Specify the fields to include in the serializer
        fields = ['id', 'author', 'email',
                  'content', 'created_at', 'blog_post']
        # Specify the fields that should be read-only
        read_only_fields = ['id', 'created_at', 'blog_post']

    def create(self, validated_data):
        # Create a new Comment object using the validated data
        comment = Comment.objects.create(**validated_data)
        # Return the created Comment object
        return comment
