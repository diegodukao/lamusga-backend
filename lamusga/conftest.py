from django.conf import settings

from lamusga import settings as lamusga_settings


def pytest_configure():
    settings.configure(lamusga_settings)
