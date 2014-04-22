from rest_framework.renderers import  UnicodeJSONRenderer
from rest_framework.serializers import SortedDictWithMetadata
from django.http.multipartparser import parse_header
import json
from rest_framework.compat import six

class StatusJSONRenderer(UnicodeJSONRenderer):

	def render(self, data, accepted_media_type=None, renderer_context=None):
		if data is None:
			data = SortedDictWithMetadata({})


		response = renderer_context['response']
		if response.status_code == 204:
			response.status_code = 200
		if isinstance(data, dict):
			data.update({'status':response.status_code})

		return super(StatusJSONRenderer, self).render(data, accepted_media_type, renderer_context)


		
		