# coding=utf-8
import os
from django.db import models
from django.conf import settings


class Faction(models.Model):
    short_name = models.CharField(max_length=10, primary_key=True)
    full_name = models.CharField(max_length=63, blank=True, null=True)
    
    def __unicode__(self):
        return self.short_name


class Party(models.Model):
    short_name = models.CharField(max_length=10, primary_key=True)
    full_name = models.CharField(max_length=63, blank=True, null=True)

    def __unicode__(self):
        return self.short_name


class Person(models.Model):
    COUNCIL_TYPES = (
        ('N', 'Nationalrat'),
        ('S', 'Ständerat'),
        ('B', 'Vereinigte Bundesversammlung'),
    )
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    number = models.IntegerField(blank=True, null=True)
    council = models.CharField(max_length=1, choices=COUNCIL_TYPES, blank=True, null=True)
    canton = models.CharField(max_length=2, blank=True, null=True)
    party = models.ForeignKey(Party, related_name=u'persons', null=True)
    faction = models.ForeignKey(Faction, related_name=u'persons', null=True)
    function = models.CharField(max_length=63, blank=True, null=True)
    biography_url = models.CharField(max_length=255, blank=True, null=True)
    
    def photo(self, size):
        relpath = os.path.join('img', 'portraits', '%s-%ux%u.jpg' % (self.number, size, size))
        if os.path.exists(os.path.join(settings.STATIC_ROOT, relpath)):
            #return os.path.join(settings.STATIC_URL + relpath)
            return 'https://github.com/gwrtheyrn/gesagt-im-parlament.ch/raw/master/frontend/apps/front/static/%s' % relpath
        return None

    def photo_large(self):
        return self.photo(225)

    def photo_small(self):
        return self.photo(120)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Affair(models.Model):
    id = models.CharField(max_length=7, primary_key=True)
    title = models.CharField(max_length=255)
    involved = models.ManyToManyField(Person, through='PersonAffair')
    type = models.CharField(max_length=255)
    congress = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    submission_date = models.DateField()
    content = models.TextField(blank=True)

    def __unicode__(self):
        return '[%s] %s' % (self.id, self.title)

    class Meta:
        get_latest_by = 'submission_date'


class PersonAffair(models.Model):

    AFFAIR_PERSON_TYPES = (
        (0, 'Submitter'),
        (1, 'Involved'),
    )
    person = models.ForeignKey(Person)
    affair = models.ForeignKey(Affair)
    type = models.IntegerField(choices=AFFAIR_PERSON_TYPES)

    def __unicode__(self):
        return '%s: %s' % (self.person.name, self.affair.id)
