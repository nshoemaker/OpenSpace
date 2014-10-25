from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from room_reservation_app.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'room_reservation.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^createReservation/$', chooseBuilding),
    url(r'^createReservation/([0-9]+)/$', chooseRoom),
    url(r'^createReservation/([0-9]+)/([0-9]+)/$', createReserveration),
    url(r'^saveEvent/$', saveEvent),
    url(r'^myReservations/$', myReservations),
    url(r'^deleteEvent/([0-9]+)/$', deleteEvent),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'room_reservation_app/signin.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/myReservations'}),
    url(r'^registration/$',register),
    url(r'^confirm/$',confirmCred),
    url(r'^$',myReservations),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
