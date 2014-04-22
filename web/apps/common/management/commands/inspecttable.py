from __future__ import unicode_literals

import keyword
import re
from optparse import make_option

from django.core.management.base import  CommandError, BaseCommand
from django.db import connections, DEFAULT_DB_ALIAS
from django.utils import six
from django.core.management.base import BaseCommand
import apps
import inspect
import pyclbr
import os

class Command(BaseCommand):
    help = "Introspects the database tables in the given database and outputs a Django model module."

    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a database to '
                'introspect.  Defaults to using the "default" database.'),
        make_option('--table', action='store', dest='table',  help='table name to inspect'),
    )

    requires_model_validation = False

    db_module = 'django.db'

    def handle(self, tableName, **options):
        
        try:
            result = self.handle_inspection(tableName,options)
            self.stdout.write(result['header'])
            self.stdout.write(result['model'])
        except NotImplementedError:
            raise CommandError("Database inspection isn't supported for the currently selected database backend.")


    def handle_inspection(self, tableName, options):

        connection = connections[options.get('database')]
        # 'table_name_filter' is a stealth option
        table_name_filter = options.get('table_name_filter')

        table2model = lambda table_name: table_name.title().replace('_', '').replace(' ', '').replace('-', '')
        strip_prefix = lambda s: s.startswith("u'") and s[1:] or s

        cursor = connection.cursor()
        options["header"] = 'from %s import models\n' % self.db_module

        known_models = []
        #for table_name in connection.introspection.table_names(cursor):
            #if table_name_filter is not None and callable(table_name_filter):
             #   if not table_name_filter(table_name):
             #       continue

        table_name = tableName


        options['modelClazz'] = table2model(table_name)
        options['model'] = '\nclass %s(models.Model):\n' % table2model(table_name)
        known_models.append(table2model(table_name))
        try:
            relations = connection.introspection.get_relations(cursor, table_name)
        except NotImplementedError:
            relations = {}
        try:
            indexes = connection.introspection.get_indexes(cursor, table_name)
        except NotImplementedError:
            indexes = {}
        used_column_names = [] # Holds column names used in the table so far
        for i, row in enumerate(connection.introspection.get_table_description(cursor, table_name)):
            comment_notes = [] # Holds Field notes, to be displayed in a Python comment.
            extra_params = {}  # Holds Field parameters such as 'db_column'.
            column_name = row[0]
            is_relation = i in relations

            att_name, params, notes = self.normalize_col_name(
                column_name, used_column_names, is_relation)
            extra_params.update(params)
            comment_notes.extend(notes)


            comment = row[7]



            used_column_names.append(att_name)

            # Add primary_key and unique, if necessary.
            if column_name in indexes:
                if indexes[column_name]['primary_key']:
                    extra_params['primary_key'] = True
                elif indexes[column_name]['unique']:
                    extra_params['unique'] = True

            
            if att_name == "creator_id":
                att_name = att_name[0:-3]
                field_type = "ForeignKey(User, editable=False, verbose_name=u'%s'" % comment
                options["header"] += self.getImportStr('User')
            elif att_name.endswith("_id"):
                att_name = att_name[0:-3]
                rel_to = att_name.capitalize()

                field_type = "ForeignKey(%s, verbose_name=u'%s'" % (rel_to, comment)
                options["header"] += self.getImportStr(att_name)
            elif att_name.endswith("_file"):

                field_type = "FileField(u'%s', upload_to=get_file_path" % comment
                #options["header"] += self.getImportStr("FileField")
            elif att_name.endswith("_pic"):

                field_type = "ImageField(u'%s', upload_to=get_file_path" % comment
                #options["header"] += self.getImportStr("ImageField")
            elif att_name == "update_time" or att_name == "create_time":
                if att_name == "update_time":
                    field_type = "DateTimeField(u'%s', auto_now=True" % comment
                else:
                    field_type = "DateTimeField(u'%s', auto_now_add=True" % comment
                options["header"] += "from datetime import datetime\n"
            
            else:
                # Calling `get_field_type` to get the field type string and any
                # additional paramters and notes.
                field_type, field_params, field_notes = self.get_field_type(connection, table_name, row)
                extra_params.update(field_params)
                comment_notes.extend(field_notes)

                field_type += "(u'%s'" % comment

            # Don't output 'id = meta.AutoField(primary_key=True)', because
            # that's assumed if it doesn't exist.
            if att_name == 'id':
                continue

            # Add 'null' and 'blank', if the 'null_ok' flag was present in the
            # table description.
            if row[6]: # If it's NULL...
                extra_params['blank'] = True
                if not field_type in ('TextField(', 'CharField('):
                    extra_params['null'] = True

            field_desc = '%s = models.%s' % (att_name, field_type)
            if extra_params:
                if not field_desc.endswith('('):
                    field_desc += ', '
                field_desc += ', '.join([
                    '%s=%s' % (k, strip_prefix(repr(v)))
                    for k, v in extra_params.items()])
            field_desc += ')'
            if comment_notes:
                field_desc += ' # ' + ' '.join(comment_notes)
            options['model'] += '    %s\n' % field_desc


        options['model'] += "\n"

        for meta_line in self.get_meta(table_name):
            options['model'] += meta_line + "\n"

        return options

    def getImportStr(self, field):
        clazzMap = {}

        for name, obj in inspect.getmembers(apps):
            if inspect.ismodule(obj):
                try:
                    s = 'apps.'+name+'.models'
                    clazzList = pyclbr.readmodule(s).keys()
                    for clazz in clazzList:
                        clazzMap[clazz] = name
                except:
                    continue

        if field.capitalize() in clazzMap:
            package = clazzMap[field.capitalize()]
        else:
            package = field

        return "from apps.%s.models import %s\n" % (package, field.capitalize())



    def normalize_col_name(self, col_name, used_column_names, is_relation):
        """
        Modify the column name to make it Python-compatible as a field name
        """
        field_params = {}
        field_notes = []

        new_name = col_name.lower()
        if new_name != col_name:
            field_notes.append('Field name made lowercase.')

        if is_relation:
            if new_name.endswith('_id'):
                new_name = new_name[:-3]
            else:
                field_params['db_column'] = col_name

        new_name, num_repl = re.subn(r'\W', '_', new_name)
        if num_repl > 0:
            field_notes.append('Field renamed to remove unsuitable characters.')

        if new_name.find('__') >= 0:
            while new_name.find('__') >= 0:
                new_name = new_name.replace('__', '_')
            if col_name.lower().find('__') >= 0:
                # Only add the comment if the double underscore was in the original name
                field_notes.append("Field renamed because it contained more than one '_' in a row.")

        if new_name.startswith('_'):
            new_name = 'field%s' % new_name
            field_notes.append("Field renamed because it started with '_'.")

        if new_name.endswith('_'):
            new_name = '%sfield' % new_name
            field_notes.append("Field renamed because it ended with '_'.")

        if keyword.iskeyword(new_name):
            new_name += '_field'
            field_notes.append('Field renamed because it was a Python reserved word.')

        if new_name[0].isdigit():
            new_name = 'number_%s' % new_name
            field_notes.append("Field renamed because it wasn't a valid Python identifier.")

        if new_name in used_column_names:
            num = 0
            while '%s_%d' % (new_name, num) in used_column_names:
                num += 1
            new_name = '%s_%d' % (new_name, num)
            field_notes.append('Field renamed because of name conflict.')

        if col_name != new_name and field_notes:
            field_params['db_column'] = col_name

        return new_name, field_params, field_notes

    def get_field_type(self, connection, table_name, row):
        """
        Given the database connection, the table name, and the cursor row
        description, this routine will return the given field type name, as
        well as any additional keyword parameters and notes for the field.
        """
        field_params = {}
        field_notes = []

        try:
            field_type = connection.introspection.get_field_type(row[1], row)
        except KeyError:
            field_type = 'TextField'
            field_notes.append('This field type is a guess.')

        # This is a hook for DATA_TYPES_REVERSE to return a tuple of
        # (field_type, field_params_dict).
        if type(field_type) is tuple:
            field_type, new_params = field_type
            field_params.update(new_params)

        # Add max_length for all CharFields.
        if field_type == 'CharField' and row[3]:
            field_params['max_length'] = row[3]

        if field_type == 'DecimalField':
            field_params['max_digits'] = row[4]
            field_params['decimal_places'] = row[5]

        return field_type, field_params, field_notes

    def get_meta(self, table_name):
        """
        Return a sequence comprising the lines of code necessary
        to construct the inner Meta class for the model corresponding
        to the given database table name.
        """
        return ["    class Meta:",
                "        db_table = '%s'" % table_name,
                "        verbose_name = verbose_name_plural = u'%s'\n\n" % table_name,
                ""
                "    def __unicode__(self):",
                "        return self.name"


                ]
