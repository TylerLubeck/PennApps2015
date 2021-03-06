
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """ A general profile for a user
    Contains information to store from Facebook
    """

    MALE = 'M'
    FEMALE = 'F'
    EUNUCH = 'E'
    GENDER_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female'),
        (EUNUCH, 'eunuch'),
    )

    UNKNOWN = 'UN'
    SINGLE = 'SI'
    RELATIONSHIP = 'RE'
    ENGAGED = 'EN'
    MARRIED = 'MA'
    CIVIL_UNION = 'CI'
    DOMESTIC_PARTNERSHIP = 'DO'
    OPEN_RELATIONSHIP = 'OP'
    COMPLICATED = 'CO'
    SEPARATED = 'SE'
    DIVORCED = 'DI'
    WIDOWED = 'WI'

    RELATIONSHIP_CHOICES = (
        (UNKNOWN, 'Unknown'),
        (SINGLE, 'Single'),
        (RELATIONSHIP, 'In a relationship'),
        (ENGAGED, 'Engaged'),
        (MARRIED, 'Married'),
        (CIVIL_UNION, 'In a civil union'),
        (DOMESTIC_PARTNERSHIP, 'In a domestic partnership'),
        (OPEN_RELATIONSHIP, 'In an open relationship'),
        (COMPLICATED, "It's complicated"),
        (SEPARATED, 'Separated'),
        (DIVORCED, 'Divorced'),
        (WIDOWED, 'Widowed'),
    )

    user = models.OneToOneField(User)
    age = models.IntegerField(null=True)
    location = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=10,
                              default=EUNUCH)
    education = models.CharField(max_length=20,
                                 default='High School')
    relationship_status = models.CharField(max_length=100,
                                           default=UNKNOWN)

    comments = models.ForeignKey('Comment', blank=True, null=True)

    def __unicode__(self):
        return self.user.get_full_name()


class Rating(models.Model):
    """ Represents what a User thinks of a Product.
    Is used as a through-table for the M2M relationship from Product to
    UserProfile
    """
    product = models.ForeignKey('Product')
    rater = models.ForeignKey(UserProfile)
    liked = models.BooleanField(default=False)


class Product(models.Model):
    """ Represents the product that will be rated by users.
    Could be expanded to have images and other things
    """

    creator = models.ForeignKey(UserProfile, related_name='my_products')
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=160)
    product_link = models.URLField(blank=True)
    video_link = models.CharField(max_length=100)
    raters = models.ManyToManyField(UserProfile,
                                    through=Rating,
                                    related_name='my_rated_products')

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    """ Represents a comment on a product """

    product = models.ForeignKey(Product)
    text = models.TextField(max_length=200)
    comment_time = models.DateTimeField()
    author = models.ForeignKey(UserProfile)
