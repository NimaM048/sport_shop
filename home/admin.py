from django.contrib import admin

from home import models
from home.models import Comment, SeriesModel, ArticleBlogModel, Episode, Season, Footer, CommentSectionModel, Reply, \
    Counseling, AboutPage, Activity, Community, DownContent,CategoryBlog


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'episode_number', 'season')  # Display these fields in the list view
    search_fields = ('title',)  # Allows search by title
    list_filter = ('season',)    # Allows filtering by season
admin.site.register(Episode,EpisodeAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')

admin.site.register(Comment, CommentAdmin)

class SeriesModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_compeleted', 'free')
    search_fields = ('title', 'author__username')
    list_filter = ('is_compeleted', 'free')
admin.site.register(SeriesModel, SeriesModelAdmin)

class ArticleBlogModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'reading_time')
    search_fields = ('title', 'author__username')
    list_filter = ('reading_time',)

admin.site.register(ArticleBlogModel, ArticleBlogModelAdmin)

class SeasonAdmin(admin.ModelAdmin):
    list_display = ('title', 'series', 'number')
    search_fields = ('title', 'series__title')
    list_filter = ('series',)

admin.site.register(Season, SeasonAdmin)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug' : ('title',)}




class FooterAdmin(admin.ModelAdmin):
    list_display = ('about_us', 'phone_number', 'email', 'working_hours', 'address')
    fieldsets = (
        ('About Us', {
            'fields': ('about_us',),
            'classes': ('wide',),
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email', 'address', 'working_hours'),
            'classes': ('wide',),
        }),
        ('Social Media', {
            'fields': ('show_social_media', 'social_media'),
            'classes': ('wide',),
        }),
        ('Copyright', {
            'fields': ('copyright_year',),
            'classes': ('wide',),
        }),
    )
admin.site.register(Footer, FooterAdmin)


class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 1

class CommentSectionModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at')
    inlines = [ReplyInline]
    search_fields = ('text', 'user__fullname', 'eries__title')
    list_filter = ('created_at',)

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at')
    search_fields = ('text', 'user__fullname')
    list_filter = ('created_at',)

admin.site.register(CommentSectionModel, CommentSectionModelAdmin)
admin.site.register(Reply, ReplyAdmin)


class CounselingAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle')  # List the fields you want to show in the admin panel
    search_fields = ('title', 'subtitle')  # Enable search for these fields

admin.site.register(Counseling, CounselingAdmin)



class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')

class CommunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')

admin.site.register(AboutPage, AboutPageAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Community, CommunityAdmin)
admin.site.register(DownContent)
admin.site.register(CategoryBlog)



