import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poco_terminal.settings')

# Important: We assign it to 'app' because Vercel looks for this variable
app = get_wsgi_application()