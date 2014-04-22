import json
from django.http import HttpResponse
from django.db.models.query import ValuesQuerySet
from django.forms.models import model_to_dict

class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        
        if "object_list" in context:
            objList = context["object_list"]
            if objList is not None:
                if type(objList) is not ValuesQuerySet:
                    objList = objList.values()
                return json.dumps(list(objList))
            else:
                return "[]"
        elif "object" in context:
            obj = context["object"]
            if obj is not None:
                return json.dumps(model_to_dict(obj))
            else:
                return "{}"

        del context["view"]
        return json.dumps(context)