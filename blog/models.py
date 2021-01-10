from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
# Create your models here.
DEFAULT = 'software'
CATEGORY = (
    ('software', 'yazilim'),
    ('product', 'urun'),
    ('game', 'oyun'),
    ('book', 'kitap'),
    ('movie', 'film'),
)
class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, default="")
    #status = models.CharField(choices=CATEGORY,max_length=10,default=DEFAULT)
    image = models.ImageField(null=True, blank=True, upload_to="category")

    def __str__(self):
        return self.title

class Post(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='post', on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name='Başlık')
    content = models.TextField(verbose_name='İçerik')
    publishing_date =models.DateTimeField(verbose_name='Yayınlanma Tarihi', auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to='post')
    slug = models.SlugField(editable=False, unique=True)
    read = models.IntegerField(default = 0) #popüler post için


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})

    def get_unique_slug(self):
        slug = slugify(self.title.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug
            

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering  = ['-publishing_date', 'id']



class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, verbose_name='Ad Soyad')
    content = models.TextField(max_length=500, verbose_name='Yorum')
    created_date = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.name