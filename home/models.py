import os

from django.db import models
from django.urls import reverse
from moviepy.video.io.VideoFileClip import VideoFileClip

from account.models import User


class Comment(models.Model):
    comment = models.TextField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField(null=True, blank=True)


    class Meta:
        verbose_name_plural= "نظرات"

    def __str__(self):
        return self.name




class Category(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name='عنوان دسته بندی', help_text='عنوان دسته بندی را وارد کنید')
    slug = models.SlugField(null=True, verbose_name='اسلاگ', help_text='اسلاگ دسته بندی را وارد کنید')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'






class SeriesModel(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    image = models.ImageField(upload_to='series_courses', verbose_name='تصویر')
    is_compeleted = models.BooleanField(default=True, verbose_name='تکمیل شده')
    language_kinds = models.ForeignKey(Category,null=True,blank=True, on_delete=models.CASCADE, related_name='categories', verbose_name="زبان")
    seseaons = models.IntegerField(verbose_name='تعداد فصل', null=True,blank=True)
    hours = models.IntegerField(verbose_name='تعداد ساعت',null=True,blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author', verbose_name='مولف')
    main_price = models.CharField(max_length=20, verbose_name='قیمت اصلی', null=True, blank=True)
    discount_price = models.CharField(max_length=20, null=True, blank=True, verbose_name='قیمت تخفیف')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    introdution_course = models.TextField(null=True, blank=True, verbose_name='معرفی دوره')
    course_extra_des1 = models.TextField(blank=True, null=True, verbose_name='توضیحات اضافی 1')
    course_extra_des2 = models.TextField(blank=True, null=True, verbose_name='توضیحات اضافی 2')
    built_in = models.TextField(blank=True, null=True, verbose_name='ساختار')
    author_description = models.TextField(blank=True, null=True, verbose_name='توضیحات مولف')
    free = models.BooleanField(default=True, verbose_name='رایگان')







    def __str__(self):
        return self.title


    class Meta:
        verbose_name = "دوره"
        verbose_name_plural = 'دوره ها'






class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_courses')
    series = models.ForeignKey('SeriesModel', on_delete=models.CASCADE, related_name='series_users')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'series')














class Season(models.Model):
    class Meta:
        verbose_name = "فصل"
        verbose_name_plural= "فصل ها"

    series = models.ForeignKey(SeriesModel, on_delete=models.CASCADE, related_name='seasons', null=True, blank=True,
                               verbose_name='دوره ها')
    number = models.IntegerField(null=True, blank=True, verbose_name='شماره فصل')
    title = models.CharField(max_length=50, null=True, blank=True, verbose_name='عنوان فصل')



    def __str__(self):
        return self.title

    def total_duration_seconds(self):
        total_duration = 0
        for episode in self.episodes.all():
            total_duration += episode.get_duration_in_seconds()
        return total_duration

    def number_of_episodes(self):
        return self.episodes.count()



from django.core.files.temp import NamedTemporaryFile

class Episode(models.Model):
    season = models.ForeignKey('Season', on_delete=models.CASCADE, related_name='episodes', null=True, blank=True, verbose_name='فصل')
    episode_number = models.IntegerField(null=True, blank=True, verbose_name='شماره اپیزود')
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='عنوان')
    duration = models.CharField(max_length=20, null=True, blank=True, verbose_name='مدت زمان')
    video_file = models.FileField(upload_to='videos/', null=True, blank=True, verbose_name='فایل ویدئو')

    class Meta:
        verbose_name = 'اپیزود'
        verbose_name_plural = 'اپیزودها'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.video_file:
            # Create a temporary file to download the video content from the storage
            with NamedTemporaryFile() as temp_video:
                temp_video.write(self.video_file.read())
                temp_video.flush()

                # Calculate duration using the temporary video file
                clip = VideoFileClip(temp_video.name)
                duration_in_seconds = clip.duration
                self.duration = f"{int(duration_in_seconds // 60)}:{int(duration_in_seconds % 60):02d}"  # Convert to mm:ss format
                clip.close()  # Close the clip to free up resources

                # Save duration after the initial save
                super().save(update_fields=['duration'])

    def get_duration_in_seconds(self):
        """ Convert the duration stored in mm:ss to seconds. """
        if self.duration:
            parts = self.duration.split(':')
            if len(parts) == 2:  # format is mm:ss
                return int(parts[0]) * 60 + int(parts[1])
        return 0  # Default to 0 if duration is not set

    def __str__(self):
        return f"{self.title} (Episode {self.episode_number})"

class CategoryBlog(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name='عنوان دسته بندی', help_text='عنوان دسته بندی را وارد کنید')
    slug = models.SlugField(null=True, verbose_name='اسلاگ', help_text='اسلاگ دسته بندی را وارد کنید')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی بلاگ ها'


from django.utils.text import slugify

class ArticleBlogModel(models.Model):
    title = models.CharField(max_length=100)
    language_kinds = models.ForeignKey(CategoryBlog, null=True, blank=True, on_delete=models.CASCADE,
                                       related_name='article_categories', verbose_name="زبان")
    image = models.ImageField(upload_to='articles_blog')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article')
    reading_time = models.IntegerField()
    article_excerpt = models.TextField(blank=True, null=True)
    article_description = models.TextField(blank=True, null=True)
    built_in = models.TextField(blank=True, null=True)
    article_extra_des1 = models.TextField(blank=True, null=True)
    article_extra_des2 = models.TextField(blank=True, null=True)
    author_description = models.TextField(blank=True, null=True)
    author_image = models.ImageField(upload_to='images',blank=True, null=True)
    slug = models.SlugField(unique=True,blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



    class Meta:
        verbose_name = 'وبلاگ'
        verbose_name_plural ='وبلاگ ها'



    def __str__(self):
        return self.title






class CommentSectionModel(models.Model):
    series = models.ForeignKey(SeriesModel, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        if self.user:
            return f"Comment by {self.user.fullname} on {self.series.title}"
        else:
            return f"Comment by Anonymous on {self.series.title}"


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(CommentSectionModel, on_delete=models.CASCADE, related_name='reply_set')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "ریپلای"
        verbose_name_plural = "ریپلای ها"

    def __str__(self):
        return f"Reply by {self.user.fullname} on {self.comment.series.title}"




class Footer(models.Model):
    about_us = models.TextField(verbose_name='درباره ما')
    phone_number = models.CharField(max_length=20, verbose_name='شماره تلفن', blank=True, null=True)
    working_hours = models.CharField(max_length=50, verbose_name='ساعات کاری',blank=True, null=True)
    address = models.TextField(verbose_name='آدرس', blank=True)
    email = models.EmailField(verbose_name='ایمیل', blank=True)
    copyright_year = models.IntegerField(verbose_name=  'سال کپی رایت',blank=True, null=True)
    show_social_media = models.BooleanField(verbose_name='نمایش شبکه های اجتماعی', default=True,blank=True, null=True)
    social_media = models.JSONField(verbose_name='شبکه های اجتماعی', blank=True, null=True)

    class Meta:
        verbose_name = 'فوتر'
        verbose_name_plural = 'فوتر'

    def __str__(self):
        return 'پاورقی'











class AboutPage(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='about_images')

class Activity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='activity_images')

class Community(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='community_images')


class Counseling(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='counseling_images/')
    button_content = models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        verbose_name_plural = "بدنه"

    def __str__(self):
        return self.title




class DownContent(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()


    class Meta :
        verbose_name_plural = "بخش پایین سایت"




    def __str__(self):
        return self.title






















