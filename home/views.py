from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView
from django.contrib import messages
from cart.models import Order, OrderItem
from home.forms import CommentForm, CommentSectionForm, ReplyForm
from .models import SeriesModel, ArticleBlogModel, CommentSectionModel, Episode, Category, Footer, Counseling, \
    UserCourse, AboutPage, Activity, Community, DownContent, CategoryBlog
from django.core.exceptions import ValidationError


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['items'] = SeriesModel.objects.all()
        context['categories'] = Category.objects.all()
        context['footer'] = Footer.objects.first()
        context["counseling_content"] = Counseling.objects.first()
        context['down_content'] = DownContent.objects.all()

        # Add blogs (articles) to context
        context['blogs'] = ArticleBlogModel.objects.all()
        context['article'] = CategoryBlog.objects.all()

        return context

def handle_form_submission(form, request):
    if form.is_valid():
        form.save()
        messages.success(request, 'پیام شما با موفقیت ارسال شد!')
        return True
    else:
        messages.error(request, 'خطا در ارسال پیام، لطفا دوباره تلاش کنید.')
        return False


def comment_view(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if handle_form_submission(form, request):
            return redirect('home:contact_us')  # Replace 'success_url' with the URL to redirect to.
    else:
        form = CommentForm()

    return render(request, 'home/contact-us.html', {'form': form})


class AboutView(TemplateView):
    template_name = 'home/about-us.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data()
        context['about_page'] = AboutPage.objects.first()
        context['activities'] = Activity.objects.all()
        context['communities'] = Community.objects.all()
        return context



class SeriesView(ListView):
    template_name = 'home/series.html'
    queryset = SeriesModel.objects.all()

    def get_context_data(self, **kwargs):
        request = self.request
        free = request.GET.get('free')
        category = request.GET.get('category')

        # Start with all series
        queryset = SeriesModel.objects.all()

        # Apply free filter
        if free is not None:  # Check if free is specified
            if free.lower() == 'true':
                queryset = queryset.filter(free=True)
            elif free.lower() == 'false':
                queryset = queryset.filter(free=False)

        # Apply category filter
        if category:
            queryset = queryset.filter(language_kinds__title=category)  # Removed icontains

        # Check if queryset is empty and set a message in Persian
        if not queryset.exists():  # If no results are found
            messages.warning(request, "نتیجه‌ای برای فیلترهای انتخاب شده پیدا نشد, لطفاً گزینه‌های دیگری امتحان کنید.")

        # Count the number of free and non-free courses
        courses_counts = SeriesModel.objects.values('free').annotate(count=Count('id'))
        free_courses_count = next((x['count'] for x in courses_counts if x['free']), 0)
        not_free_courses_count = next((x['count'] for x in courses_counts if not x['free']), 0)

        # Create context
        context = super(SeriesView, self).get_context_data(**kwargs)
        context['course'] = queryset  # Use `object_list` instead of 'free'
        context['free_courses_count'] = free_courses_count
        context['not_free_courses_count'] = not_free_courses_count
        context['categories'] = Category.objects.all()  # Assuming you have a model for categories
        return context


from django.shortcuts import get_object_or_404

class ArticleDetailView(DetailView):
    model = ArticleBlogModel
    template_name = 'home/article-detail.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(ArticleBlogModel, slug=slug)

    def get_context_data(self, **kwargs):
        # Get the default context from the superclass
        context = super().get_context_data(**kwargs)

        # Efficiently get only the current article
        context['current_article'] = self.object

        # Get a related article or similar articles for suggestions (if needed)
        context['related_articles'] = ArticleBlogModel.objects.exclude(id=self.object.id).all()

        return context

class SearchProductView(View):

    def render_response(self, request, search=None, product=None, error_message=None):
        context = {'search': search, 'product': product, 'error_message': error_message}
        return render(request, "home/search_course.html", context)

    def get(self, request):
        return self.render_response(request)

    def post(self, request):
        search = request.POST.get('search', '').strip()

        if not search:
            return self.render_response(request, error_message='لطفا دوره ای که به دنبال آن هستید را جست و جو کنید.')

        products = SeriesModel.objects.filter(title__icontains=search)
        if not products.exists():
            return self.render_response(request, search=search, error_message='دوره ای یافت نشد.')

        return self.render_response(request, search=search, product=products)


class CourseDetailView(DetailView):
    template_name = 'home/course-detail.html'
    model = SeriesModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the context for the main series object
        context['series_object'] = self.get_object()
        context['items'] = SeriesModel.objects.all()
        context['reply_form'] = ReplyForm()
        user = self.request.user

        # Check if user has purchased the course
        context['show_start_learning'] = user.is_authenticated and OrderItem.objects.filter(
            order__user=user, order__is_paid=True,
            product=self.get_object()).exists()

        # Count distinct users who have purchased the course
        purchased_users_count = OrderItem.objects.filter(
            order__is_paid=True,
            product=self.get_object()
        ).values_list('order__user', flat=True).distinct().count()

        # Count distinct users who have added the course to their profile
        added_users_count = UserCourse.objects.filter(series=self.get_object()).values_list('user',
                                                                                            flat=True).distinct().count()

        # Total users count, adding 50 to the sum
        total_users_count = purchased_users_count + added_users_count + 50

        # Pass the counts to the context
        context['purchased_users_count'] = purchased_users_count
        context['added_users_count'] = added_users_count
        context['total_users_count'] = total_users_count

        # Filter active comments and their replies
        active_comments = self.get_object().comments.filter(is_active=True)
        for comment in active_comments:
            comment.active_replies = comment.reply_set.filter(is_active=True)

        context['active_comments'] = active_comments

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentSectionForm()
        reply_form = ReplyForm()

        if 'comment_id' in request.POST:  # Check if it's a reply
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                comment = CommentSectionModel.objects.get(pk=request.POST.get('comment_id'))
                reply = reply_form.save(commit=False)
                reply.comment = comment
                reply.user = request.user
                reply.save()
                return redirect('home:course_detail', pk=self.object.pk)  # Redirect back
        else:  # Handle comment submission
            comment_form = CommentSectionForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.series = self.object
                comment.user = request.user
                comment.save()
                return redirect('home:course_detail', pk=self.object.pk)

        return self.render_to_response(self.get_context_data(form=comment_form, reply_form=reply_form))


class BlogView(TemplateView):
    template_name = 'home/blog.html'

    def get_context_data(self, **kwargs):
        request = self.request
        category = request.GET.get('category')

        queryset = ArticleBlogModel.objects.all()
        categories = CategoryBlog.objects.all()  # Fetch all categories

        # Apply category filter
        if category:
            queryset = queryset.filter(language_kinds__title__icontains=category)

        # Check if the filtered queryset is empty
        if not queryset.exists():
            messages.warning(request, "هیچ مقاله‌ای برای فیلترهای انتخاب شده پیدا نشد، لطفاً گزینه‌های دیگری را امتحان کنید.")

        context = super(BlogView, self).get_context_data(**kwargs)
        context['blog'] = queryset  # Pass the filtered queryset to the template
        context['categories'] = categories  # Add categories to context
        return context

class BlogProductView(View):
    def get(self, request):
        return render(request, "home/search_blog.html")

    def post(self, request):
        search = request.POST.get('search')
        if not search:
            error_message = 'لطفا مقاله ای که به دنبال آن هستید را جست و جو کنید.'
            return render(request, "home/search_blog.html", {'search': search, 'error_message': error_message})

        try:
            if len(search) > 255:
                raise ValidationError('Search query is too long.')
            if not search.isalnum():
                raise ValidationError('Search query contains invalid characters.')
            blog = ArticleBlogModel.objects.filter(title__icontains=search)
            if not blog:
                error_message = 'مقاله ای یافت نشد.'
                return render(request, "home/search_blog.html", {'search': search, 'error_message': error_message})
            else:
                return render(request, "home/search_blog.html", {'search': search, 'blog': blog, 'error_message': None})
        except ValidationError as e:
            error_message = 'خطایی در جستجوی مقاله رخ داد.'
            return render(request, "home/search_blog.html", {'search': search, 'error_message': error_message})
        except Exception as e:
            error_message = 'خطایی در جستجوی مقاله رخ داد.'
            return render(request, "home/search_blog.html", {'search': search, 'error_message': error_message})




class SeriesEpisodeDetailView(DetailView):
    model = SeriesModel
    template_name = 'home/course-episodes.html'

    def get(self, request, *args, **kwargs):
        series = self.get_object()
        if series.free:
            return super().get(request, *args, **kwargs)
        else:
            order = Order.objects.filter(user=request.user, is_paid=True, items__product=series).exists()
            if not order:
                raise Http404('You do not have access to this page')
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        series = self.get_object()

        # Fetch all seasons for this series
        seasons = series.seasons.all()

        # Initialize totals
        total_duration_seconds = 0
        total_episodes_count = 0

        # Calculate total duration and number of episodes
        for season in seasons:
            total_duration_seconds += season.total_duration_seconds()
            total_episodes_count += season.number_of_episodes()

        # Convert total duration seconds to formatted duration
        total_duration_formatted = self.format_duration(total_duration_seconds)

        # Pass the seasons and total values to the template context
        context['seasons'] = seasons
        context['total_duration'] = total_duration_formatted
        context['total_episodes'] = total_episodes_count

        # Add comment section context data
        context['series_object'] = series

        # Filter active comments and their replies
        active_comments = series.comments.filter(is_active=True)
        for comment in active_comments:
            comment.active_replies = comment.reply_set.filter(is_active=True)

        context['active_comments'] = active_comments
        context['reply_form'] = ReplyForm()

        # Check for user purchase
        user = self.request.user
        context['show_start_learning'] = user.is_authenticated and OrderItem.objects.filter(
            order__user=user, order__is_paid=True,
            product=series).exists()

        # Count distinct users who have purchased the series
        purchased_users_count = OrderItem.objects.filter(
            order__is_paid=True,
            product=series
        ).values_list('order__user', flat=True).distinct().count()

        # Count distinct users who have added the series to their profile
        added_users_count = UserCourse.objects.filter(series=series).values_list('user', flat=True).distinct().count()

        # Total users count, including 50 extra users
        total_users_count = purchased_users_count + added_users_count + 50

        # Pass the counts to the context
        context['purchased_users_count'] = purchased_users_count
        context['added_users_count'] = added_users_count
        context['total_users_count'] = total_users_count

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentSectionForm()
        reply_form = ReplyForm()

        if 'comment_id' in request.POST:  # Check if it's a reply
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                comment = CommentSectionModel.objects.get(pk=request.POST.get('comment_id'))
                reply = reply_form.save(commit=False)
                reply.comment = comment
                reply.user = request.user
                reply.save()
                return redirect('home:series_episod', pk=self.object.pk)  # Redirect back
        else:  # Handle comment submission
            comment_form = CommentSectionForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.series = self.object
                comment.user = request.user
                comment.save()
                return redirect('home:series_episod', pk=self.object.pk)

        return self.render_to_response(self.get_context_data(form=comment_form, reply_form=reply_form))

    def format_duration(self, total_seconds):
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            return f"{int(hours)}:{int(minutes):02d}:{int(seconds):02d}"
        else:
            return f"{int(minutes)}:{int(seconds):02d}"