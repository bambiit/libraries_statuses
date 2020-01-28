
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
            input_description = False
            current_library = None

            for line in file:
                if input_description:
                    if description and line[:1] == " ":
                        description += "\n" + line
                    else:
                        input_description = False

                if "Package:" in line:
                    if current_library:
                        self.insert_or_update_library(current_library, name, depends, description)
                        description = ''
                        depends = []
                        current_library = None

                    name = line.split(":", 1)[1].strip()
                    current_library = self.insert_or_update_library(current_library, name)

                if "Depends:" in line:
                    depend_library = line.split(":", 1)[1].strip()
                    depends = json.dumps(self.assign_relevant_libraries(current_library, depend_library))

                if "Description:" in line:
                    input_description = True
                    description = line.split(":", 1)[1].strip()

        # Insert last library
        if name:
            self.insert_or_update_library(current_library, name, depends, description)

    @staticmethod
    def insert_or_update_library(library, name, depends = None, description =''):

        if not library:
            try:
                library = Libraries.objects.get(name=name)
            except Libraries.DoesNotExist:
                library = Libraries()
                library.name = name

        if depends:
            library.depends = depends

        if description:
            library.description = description

        library.save()
        return library

    @staticmethod
    def assign_relevant_libraries(current_library, line):
        depends_list = line.split("[,|]")
        depends = []
        for depend_library in depends_list:
            # remove version
            depend_library = depend_library.split("(", 1)[0].strip()
            try:
                # get depends library
                library = Libraries.objects.get(name=depend_library)
            except Libraries.DoesNotExist:
                library = Libraries()
                library.name = depend_library

            # Update reverse depends list
            reverse_depends_array = []
            if library.reverse_depends:
                reverse_depends_array = json.loads(library.reverse_depends)

            reverse_depends_array.append({"id": current_library.id, "name": current_library.name})
            library.reverse_depends = json.dumps(reverse_depends_array)
            library.save()

            # assign depends to an array
            depends.append({"id": library.id, "name": depend_library})
        return depends

