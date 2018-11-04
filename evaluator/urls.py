from django.urls import path, re_path
from . import views
import oauth2_provider.views as oauth2_views
from django.conf import settings
app_name = 'evaluator'
oauth2_endpoint_views = [
    re_path(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    re_path(r'^token/$', oauth2_views.TokenView.as_view(), name="token"),
    re_path(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        re_path(r'^applications/$', oauth2_views.ApplicationList.as_view(), name="list"),
        re_path(r'^applications/register/$', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        re_path(r'^applications/(?P<pk>\d+)/$', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        re_path(r'^applications/(?P<pk>\d+)/delete/$', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        re_path(r'^applications/(?P<pk>\d+)/update/$', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        re_path(r'^authorized-tokens/$', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        re_path(r'^authorized-tokens/(?P<pk>\d+)/delete/$', oauth2_views.AuthorizedTokenDeleteView.as_view(),
            name="authorized-token-delete"),
    ]

urlpatterns = [
    re_path(r'^api/submit', views.OAuthProtectedEndpoints.as_view()),
    path('task/<id>', views.task, name='task'),
]