import os
import sys

# Make project root importable so `travel` package can be found when run
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Ensure DJANGO_SETTINGS_MODULE is set to load project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel.settings')
import django

try:
    django.setup()
except Exception as e:
    print('Django setup error:', e)
    sys.exit(1)

from core.context_processors import site_options

# Call the context processor and print keys to confirm no exceptions
ctx = site_options(None)
print('site_option present:', bool(ctx.get('site_option')))
print('hero_image:', ctx.get('hero_image'))
print('footer_image:', ctx.get('footer_image'))
print('hero_heading:', ctx.get('hero_heading'))
print('search_placeholder:', ctx.get('search_placeholder'))
