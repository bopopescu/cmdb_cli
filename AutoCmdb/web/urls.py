from django.conf.urls import url, re_path
from django.conf.urls import include
from django.contrib import admin
from web.views import account
from web.views import home
from web.views import asset
from web.views import user
from web.views import database
from web.views import backup
from web.views import grant
from web.views import systeminit

urlpatterns = [
    url(r'^login.html$', account.LoginView.as_view()),
    re_path(r'^get_valid_img.png/', account.get_valid_img),
    url(r'^logout.html$', account.LogoutView.as_view()),
    re_path(r'^register.html', account.register_ajax),
    re_path(r'^username_exists_check/', account.username_exists_check),
    url(r'^index.html$', home.IndexView.as_view()),
    url(r'^cmdb.html$', home.CmdbView.as_view()),

    url(r'^asset.html$', asset.AssetListView.as_view()),
    url(r'^assets.html$', asset.AssetJsonView.as_view()),
    url(r'^asset-(?P<device_type_id>\d+)-(?P<asset_nid>\d+).html$', asset.AssetDetailView.as_view()),
    url(r'^add-asset.html$', asset.AddAssetView.as_view()),

    url(r'^users.html$', user.UserListView.as_view()),
    url(r'^user.html$', user.UserJsonView.as_view()),

    url(r'^databases.html$', database.DatabaseListView.as_view()),
    url(r'^database.html$', database.DatabaseJsonView.as_view()),
    url(r'^database-(?P<db_name>\w+)-(?P<db_id>\w+).html$', database.DatabaseDetailView.as_view()),
    url(r'^add-database.html$', database.AddDatabaseView.as_view()),

    url(r'^backups.html$', backup.BackupListView.as_view()),
    url(r'^backup.html$', backup.BackupJsonView.as_view()),
    url(r'^backup-(?P<db_name>\w+)-(?P<db_id>\w+).html$', backup.BackupDetailView.as_view()),
    url(r'^add-backup.html$', backup.AddBackupView.as_view()),

    url(r'^grants.html$', grant.GrantListView.as_view()),
    url(r'^grant.html$', grant.GrantJsonView.as_view()),
    url(r'^grant-agree/', grant.GrantAgreeView.as_view()),
    url(r'^grant-define$', grant.GrantDefineView.as_view()),
    url(r'^add-grant.html$', grant.AddGrantView.as_view()),

    url(r'^systems.html$', systeminit.SystemInitListView.as_view()),
    url(r'^system.html$', systeminit.SystemInitJsonView.as_view()),
    url(r'^add-system.html$', systeminit.SystemAddView.as_view()),


    url(r'^chart-(?P<chart_type>\w+).html$', home.ChartView.as_view()),
]
