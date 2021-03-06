
import os
import types
import sys
from django.conf import settings
from django.db import connection
import arches.app.models.models as archesmodels
from arches.app.models.resource import Resource
import codecs
from format import Writer
import json
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
import csv


class JsonWriter(Writer):

    def __init__(self):
        super(JsonWriter, self).__init__()

    def write_resources(self, dest_dir):
        cursor = connection.cursor()
        cursor.execute("""select entitytypeid from data.entity_types where isresource = TRUE""")
        resource_types = cursor.fetchall()
        json_resources = []
        with open(dest_dir, 'w') as f:
            for resource_type in resource_types:
                resources = archesmodels.Entities.objects.filter(entitytypeid = resource_type)
                print "Writing {0} {1} resources".format(len(resources), resource_type[0])
                errors = []
                for resource in resources:
                    try:
                        a_resource = Resource().get(resource.entityid)
                        a_resource.form_groups = None
                        json_resources.append(a_resource)
                    except Exception as e:
                        if e not in errors:
                            errors.append(e)
                if len(errors) > 0:
                    print errors[0], ':', len(errors)
            f.write((JSONSerializer().serialize({'resources':json_resources}, separators=(',',':'))))


class JsonReader():

    def validate_file(self, archesjson, break_on_error=True):
        pass

    def load_file(self, archesjson):
        resources = []
        with open(archesjson, 'r') as f:
            resources = JSONDeserializer().deserialize(f.read())
        return resources['resources']