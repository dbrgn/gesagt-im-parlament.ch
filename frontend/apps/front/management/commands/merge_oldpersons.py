import psycopg2
import psycopg2.extras
from django.core.management.base import NoArgsCommand
from apps.front import models

class Command(NoArgsCommand):
    help = 'Merge in additional data from old person database'

    def printO(self, message):
        """Print to stdout"""
        self.stdout.write(message + '\n')

    def printE(self, message):
        """Print to stderr"""
        self.stderr.write(message + '\n')

    def handle_noargs(self, **options):
        # Connect to old db
        conn = psycopg2.connect("dbname=parlament")
        cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute('SELECT pe.*, pa.full_name AS party, fa.full_name AS faction \
                     FROM front_person pe \
                     JOIN front_party pa ON pe.party_id = pa.short_name \
                     JOIN front_faction fa ON pe.faction_id = fa.short_name')

        # Iterate persons
        for row in cur:
            try:
                person = models.Person.objects.get(id=row.id)
            except models.Person.DoesNotExist:
                self.prontO('Person %s not found.' % row.name)
                continue
            if row.number and not person.number:
                person.number = row.number
                person.council = row.council
                person.canton = row.canton
                person.function = row.function
                party, created = models.Party.objects.get_or_create(pk=row.party_id)
                if created:
                    party.full_name = row.party
                    party.save()
                person.party = party
                faction, created = models.Faction.objects.get_or_create(pk=row.faction_id)
                if created:
                    faction.full_name = row.faction
                    faction.save()
                person.biography_url = row.biography_url
                try:
                    person.save()
                except Exception:
                    self.printE('Failed to save person %s.' % person.name)
                else:
                    self.printO('Updated person %s.' % person.name)

        # Close connection
        cur.close()
        conn.close()
