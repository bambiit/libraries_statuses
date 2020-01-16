
from django.core.management.base import BaseCommand
import json
from crawling_libraries.models import Libraries


class Command(BaseCommand):

    help = "To crawl the information from library status file"

    @staticmethod
    def get_libraries_status_path():
        return '/var/lib/dpkg/status'

    def handle(self, **options):
        file_path = self.get_libraries_status_path()
        with open(file_path, "r", encoding='UTF-8') as file:

            name = ''
            description = ''
            depends = []
            reverse_depends = []
            input_description = False

            for line in file:
                if input_description:
                    if description and line[:1] == " ":
                        description += "\n" + line
                    else:
                        input_description = False

                if "Package:" in line:
                    if name:
                        self.insert_update_library(depends, description, name, reverse_depends)

                        description = ''
                        depends = []
                        reverse_depends = []

                    name = line.split(":", 1)[1].strip()

                if "Depends:" in line or "Pre-Depends:" in line:
                    depend_library = line.split(":", 1)[1].strip()
                    depends = json.dumps(self.assign_relevant_libraries(depend_library))

                if "Suggests:" in line:
                    reverse_depend_library = line.split(":", 1)[1].strip()
                    reverse_depends = json.dumps(self.assign_relevant_libraries(reverse_depend_library))

                if "Description:" in line:
                    input_description = True
                    description = line.split(":", 1)[1].strip()

        # Insert last library
        if name:
            self.insert_update_library(depends, description, name, reverse_depends)

    def insert_update_library(self, depends, description, name, reverse_depends):
        try:
            library = Libraries.objects.get(name=name)
        except Libraries.DoesNotExist:
            library = Libraries()
            library.name = name
        library.description = description
        library.depends = depends
        library.reverse_depends = reverse_depends
        library.save()
        return library

    def assign_relevant_libraries(self, line):
        depends_list = line.split(",")
        depends = []
        for depend_library in depends_list:
            # remove version
            depend_library = depend_library.split("(", 1)[0].strip()
            try:
                library = Libraries.objects.get(name=depend_library)
            except Libraries.DoesNotExist:
                library = Libraries()
                library.name = depend_library
                library.save()

            # assign to an array
            depends.append({"id": library.id, "name": depend_library})
        return depends

