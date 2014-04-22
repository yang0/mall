from __future__ import unicode_literals

import keyword
import re
import os
from optparse import make_option

from django.core.management.base import  CommandError, BaseCommand
from django.db import connections, DEFAULT_DB_ALIAS
from django.utils import six
from django.core.management.templates import TemplateCommand
from apps.common.management.commands.inspecttable import Command


class Command(TemplateCommand, Command):
    help = "Introspects the database table in the given database and outputs a Django model module."

    option_list = TemplateCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a database to '
                'introspect.  Defaults to using the "default" database.'),
        make_option('--table', action='store', dest='table',  help='table name to inspect'),
    )

    requires_model_validation = False

    db_module = 'django.db'
    templateRoot = "./templates/app_template/"
    targetRoot = "./"


    targets = ["apps/", "templates/"]


    def handle(self, appName, tableName, **options):
        for targetName in self.targets:

            templatePath = self.templateRoot + targetName
            options['template'] = templatePath

            targetPath = self.targetRoot + targetName + appName
            directory = os.path.join(os.getcwd(), targetPath)
            print directory
            if not os.path.exists(directory):
                os.makedirs(directory)
            else:
                print 'error=============:folder exist'
                raise


            self.handle_model(appName, tableName, targetPath,  **options)




    def handle_model(self, appName, tableName, target=None,  **options):
        try:
            options = self.handle_inspection(tableName,options)
            
            super(Command, self).handle('app', appName, target, **options)
        except NotImplementedError:
            raise CommandError("Database inspection isn't supported for the currently selected database backend.")

    
