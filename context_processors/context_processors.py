from django.shortcuts import render

from cart.models import Order
from home.models import ArticleBlogModel, SeriesModel, Category, Footer, CategoryBlog
from django.db.models import Count, Sum

from django.db import models
# context_processors.py

def blogs_processor(request):
   article = CategoryBlog.objects.all()

   return {'article':article}

def article_blog(request):
    blog = ArticleBlogModel.objects.all()
    course = SeriesModel.objects.all()

    return {'blog':blog, 'course':course,}



# def series_info(request):
#     series_info = {}
#
#     if request.user.is_authenticated:
#         series_list = SeriesModel.objects.all()
#         for series in series_list:
#             total_duration_seconds = 0
#             total_episodes_count = 0
#
#             # Fetch all seasons for this series
#             seasons = series.seasons.all()
#
#             for season in seasons:
#                 total_duration_seconds += season.total_duration_seconds()
#                 total_episodes_count += season.number_of_episodes()
#
#             # Store calculated total duration and episodes
#             series_info[series.id] = {
#                 'total_duration': format_duration(total_duration_seconds),
#                 'total_episodes': total_episodes_count
#             }
#
#     return {'series_info': series_info}
#




def format_duration(total_seconds):
    """ Helper function to format seconds into mm:ss. """
    minutes, seconds = divmod(total_seconds, 60)
    return f"{int(minutes)}:{int(seconds):02d}"






def footer_context_processor(request):
    footer = Footer.objects.first()
    return {
        'footer': footer,
    }







def categories(request):
    return {'catgory': Category.objects.all()}


