import json
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError, CommandParser
from common.models import Seller

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(file)