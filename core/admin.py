"""
Minimal admin for the core app.
"""

from django.contrib import admin

# Core has no models by default; this file is a safe placeholder.

# Hide auth Group from admin index so the "Authentication" app doesn't
# appear on the admin homepage. This runs when admin modules are imported.
from django.contrib.auth.models import Group
try:
	admin.site.unregister(Group)
except Exception:
	pass


# Register SiteOption admin here if the model exists.
try:
	from .models import SiteOption

	@admin.register(SiteOption)
	class SiteOptionAdmin(admin.ModelAdmin):
		list_display = ('hero_heading', 'updated_at')
		readonly_fields = ('updated_at',)

		def has_add_permission(self, request):
			# Only allow a single SiteOption instance for simplicity.
			if SiteOption.objects.exists():
				return False
			return super().has_add_permission(request)
except Exception:
	# If the model isn't present (migrations not applied) skip registration.
	pass
