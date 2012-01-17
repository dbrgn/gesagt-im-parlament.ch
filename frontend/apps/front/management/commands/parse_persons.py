import requests
import json
from django.core.management.base import NoArgsCommand
from apps.front import models

BASE_URL = 'http://ws.parlament.ch'

class Command(NoArgsCommand):
    help = 'Get person data from parlament.ch web service and process it'

    def printO(self, message):
        """Print to stdout"""
        self.stdout.write(message + '\n')

    def printE(self, message):
        """Print to stderr"""
        self.stderr.write(message + '\n')

    def handle_noargs(self, **options):
        # Get list of councillors from ws.parlament.ch
        headers = {'Accept': 'text/json', 'Accept-Language': 'de-CH, de-DE;q=0.8, de;q=0.6'}
        resource = BASE_URL + '/councillors/basicdetails'
        response = requests.get(resource, headers=headers)
        councillors = json.loads(response.content)
        self.printO('Fetched data from %s' % resource)
        for c in councillors:
            try:
                person = models.Person.objects.get(id=c['id'])
            except models.Person.DoesNotExist:
                person = models.Person()
                person.id = c['id']
            person.number = c['number']
            person.council = c['council']
            person.canton = c['canton']
            # Note: Cut off party short names after a hyphen (e.g. FDP-Liberale -> FDP)
            party, created = models.Party.objects.get_or_create(pk=c['party'].split('-', 1)[0])
            if created:
                party.full_name = c['partyName']
                party.save()
            person.party = party
            faction, created = models.Faction.objects.get_or_create(pk=c['faction'])
            if created:
                faction.full_name = c['factionName']
                faction.save()
            person.faction = faction
            person.function = c['function']
            person.biography_url = c['biographyUrl']
            try:
                person.save()
            except Exception as e:
                self.printE('Failed to parse Person %s (%s %s)' % (person['id'], person['firstName'], person['lastName']))
            else:
                self.printO('Parsed Person [%s] %s' % (person.id, person.name))
