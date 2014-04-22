# encoding: utf-8

from django.forms import widgets
from django.utils.safestring import mark_safe

class CitySelect(widgets.MultiWidget):
    def __init__(self, attrs=None):
        # create choices for days, months, years
        # example below, the rest snipped for brevity.
        years = [(year, year) for year in (2011, 2012, 2013)]

        _widgets = (
            widgets.Select(attrs=attrs, choices=[]),
            widgets.Select(attrs=attrs, choices=[]),
            widgets.Select(attrs=attrs, choices=[]),
            widgets.HiddenInput(attrs=attrs),
        )
        super(CitySelect, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [None, None, None]
        return [None, None, None]

    def render(self, name, value, attrs=None):
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        ng_model = ''
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_ and i < 3:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
                if i == 0:
                    ng_model = final_attrs['ng-model']
                final_attrs['ng-model'] = '%s_%s' % (ng_model,i)
                final_attrs['ng-options'] = "city.id as city.name for city in cityList%s" % (i)
                final_attrs['ng-change'] = "selectCity(%s, %s)" % (final_attrs['ng-model'],i)
                final_attrs['ng-required'] = 'false'
            else:
                del final_attrs['ng-options']
                del final_attrs['ng-change']
                final_attrs['ng-model'] = ng_model
                final_attrs['ng-required'] = 'true'
                
            output.append(widget.render(name + '_%s' % i, widget_value, final_attrs))
        return mark_safe(self.format_output(output))



    def value_from_datadict(self, data, files, name):
        cityList = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        print cityList
        return cityList[0]


class NewSelect(widgets.Select):

    def render(self, name, value, attrs=None):
        t = super(NewSelect, self).render(name, value)

        output = u"%s <a href='' ng-click='newOption()'><i class='icon-plus-sign'></i></a> "   % t
        optionForm = u'<input type="text" ng-model="newOptionValue">'
        button = u'<a ng-click="saveOption(newOptionValue)" class="btn btn-site btn-small">保存</a> '
        button += u'<a ng-click="newOption()" class="btn btn-site btn-small">取消</a>'
        output += u'<p><div ng-hide="showOptionForm">%s  %s</div>' % (optionForm, button)


        return mark_safe(output)



"""
        try:
            D = date(day=int(datelist[0]), month=int(datelist[1]),
                    year=int(datelist[2]))
        except ValueError:
            return ''
        else:
            return str(D)
"""