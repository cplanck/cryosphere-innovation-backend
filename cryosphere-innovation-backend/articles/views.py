from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

import articles
from articles.models import Article
from articles.serializers import *


# this view is for the article page
class ArticleDetailView(DetailView):

    model = Article
    template_name = 'articles/article.html'

    def get_context_data(self, **kwargs):
        # Add in a QuerySet of all the books
        # context = super(DetailView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        article = Article.objects.get(slug=slug)
        context = {'article': article}
        return context


class EditArticle(TemplateView):
    template_name = 'articles/edit_article.html'


# this view is for the article API endpoint
class GetArticle(viewsets.ModelViewSet):

    """ API endpoint for fetching articles """

    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):

        print('REQUEST METHOD:')
        print(self.request.method)

        slug = self.request.query_params.get('article')

        if slug:
            article_status = Article.objects.filter(
                slug=slug).values_list('status', flat=True)[0]

        if slug and article_status != 'Internal':
            queryset = Article.objects.filter(
                slug=slug).order_by('-published_date')
            return queryset

        elif slug and article_status == 'Internal' and self.request.user.is_staff:
            queryset = Article.objects.filter(
                slug=slug).order_by('-published_date')
            return queryset

        elif slug and article_status == 'Internal' and not self.request.user.is_staff:
            raise Http404

        else:
            if self.request.user.is_staff:
                queryset = Article.objects.all().order_by('-published_date')
                return queryset
            else:
                queryset = Article.objects.filter(
                    status='Published').order_by('-published_date')
                return queryset

    def create(self, request):

        article = request.data['slug']

        if self.request.user.is_staff:
            try:  # update existing row if possible
                row = Article.objects.get(slug=article)
                serializer = ArticleSerializer(
                    row, data=request.data, partial=True)

            except:  # or create record if it doesnt exists
                serializer = ArticleSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                error = Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST)
                print(error.data)
