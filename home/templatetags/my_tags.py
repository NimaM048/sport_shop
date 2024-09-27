from django import template
import jdatetime
from django import template
from datetime import datetime
register = template.Library()

@register.simple_tag
def calculate_episodes_and_duration(series):
    total_duration_seconds = 0
    total_episodes_count = 0

    for season in series.seasons.all():
        total_duration_seconds += season.total_duration_seconds()
        total_episodes_count += season.number_of_episodes()

    total_duration_formatted = format_duration(total_duration_seconds)

    return {
        'total_duration': total_duration_formatted,
        'total_episodes': total_episodes_count
    }


def format_duration(total_seconds):
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f"{int(hours)}:{int(minutes):02d}:{int(seconds):02d}"
    else:
        return f"{int(minutes)}:{int(seconds):02d}"


@register.filter
def to_jalali(date):
    if date:
        jalali_date = jdatetime.datetime.fromgregorian(datetime=date)
        return jalali_date.strftime('%Y/%m/%d')  # Customize the format as needed
    return ''




@register.filter
def extract_discount_amount(message):
    return message.split(' ')[1]

















# @register.simple_tag
# def calculate_episodes_and_duration(series):
#     total_duration_seconds = 0
#     total_episodes_count = 0
#
#     for season in series.seasons.all():
#         total_duration_seconds += season.total_duration_seconds()
#         total_episodes_count += season.number_of_episodes()
#
#     total_duration_formatted = format_duration(total_duration_seconds)
#
#     return {
#         'total_duration': total_duration_formatted,
#         'total_episodes': total_episodes_count
#     }
