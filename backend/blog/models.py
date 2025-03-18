from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class BlogPost(models.Model):
    """
    Model for blog posts in the herbalist website.
    Stores all information related to a single blog post.
    """

    # The main title of the blog post
    title = models.CharField(max_length=200)

    # URL-friendly version of the title (e.g., "my-blog-post")
    slug = models.SlugField(max_length=200, unique=True)

    # Links the post to the user who wrote it
    # If user is deleted, their posts will also be deleted (CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )

    # The main content/body of the blog post
    content = models.TextField()

    # Optional image for the blog post
    # Will be stored in a 'blog_images' directory
    featured_image = models.ImageField(
        upload_to="blog_images/",
        null=True,  # Database can store NULL
        blank=True,  # Form can be submitted empty
    )

    # Date when the post was first created
    created_date = models.DateField(default=timezone.now)

    # Date when the post was/will be published
    # Can be empty (for drafts)
    published_date = models.DateField(blank=True, null=True)

    # Current status of the post (draft or published)
    status = models.CharField(
        max_length=10,
        choices=[("draft", "Draft"), ("published", "Published")],
        default="draft",
    )

    # Category of the blog post for organization
    categories = models.CharField(
        max_length=100,
        choices=[
            ("herbs", "Herbal Medicine"),
            ("wellness", "Wellness Tips"),
            ("recipes", "Herbal Recipes"),
            ("health", "Health Insights"),
            ("treatments", "Treatment Information"),
        ],
    )

    class Meta:
        """
        Meta options for BlogPost model.
        Orders posts by published date (newest first)
        """

        ordering = ["-published_date"]

    def publish(self):
        """
        Method to publish a blog post:
        - Sets the published date to today
        - Changes status to 'published'
        - Saves the changes
        """
        self.published_date = timezone.now().date()
        self.status = "published"
        self.save()

    def __str__(self):
        """
        String representation of the blog post
        Returns the title when the object is printed
        """
        return self.title
