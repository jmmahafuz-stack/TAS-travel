"""Core site models.

This module contains a small `SiteOption` model used to manage simple
site-wide settings editable via the admin UI (homepage hero image, texts,
and search placeholder).
"""

from django.db import models


class SiteOption(models.Model):
	"""Simple singleton settings for the public site.

	Admins can add/edit a single `SiteOption` instance to customize the
	homepage hero background image, heading, subheading and search
	placeholder text.
	"""
	hero_image = models.ImageField(upload_to='site/', blank=True, null=True)
	hero_heading = models.CharField(max_length=200, blank=True, default='Travel better with MyTrip')
	hero_subheading = models.TextField(blank=True, default='Search flights, hotels and curated travel packages — plan and book in a few clicks.')
	search_placeholder = models.CharField(max_length=200, blank=True, default='Search destinations, flights, hotels...')
	# Optional footer background image editable via admin
	footer_image = models.ImageField(upload_to='site/', blank=True, null=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return 'Site Settings'

	class Meta:
		verbose_name = 'Site Setting'
		verbose_name_plural = 'Site Settings'
