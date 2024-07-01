from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = "My Custom Administration"
    site_title = "My Site Admin"
    index_title = "Welcome to My Admin"

admin_site = MyAdminSite(name='myadmin')
