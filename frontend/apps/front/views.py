import json
import re
from itertools import chain
from collections import defaultdict
from django.http import HttpResponse
from django.db.models import Count, Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView, ListView, DetailView
from apps.front import models
from apps.front.stopwords import stopwords


class Persons(ListView):
    queryset = models.Faction.objects.annotate(person_count=Count('persons')).order_by('-person_count')
    context_object_name = 'factions'
    template_name = 'persons.html'

    def get_context_data(self, **kwargs):
        context = super(Persons, self).get_context_data(**kwargs)
        nofaction_persons = models.Person.objects.all().filter(faction__isnull=True)
        context['nofaction_persons'] = nofaction_persons
        return context


class Person(DetailView):
    model = models.Person
    context_object_name = 'person'
    template_name = 'person.html'

    def get_context_data(self, object, **kwargs):
        context = super(Person, self).get_context_data(**kwargs)
        
        # Minimum of times a word must appear to be in the final list
        min_word_count = 3
        max_words = 30

        affairs = object.affair_set.all()

        # Get all content words
        contents = [a.content.split(' ') for a in affairs]
        # Flatten "list in list"
        wordlist_contents = sum(contents, [])  

        # Get all title words
        titles = [a.title.split(' ') for a in affairs]
        # Flatten "list in list"
        wordlist_titles = sum(titles, [])  

        def process_wordlist(wordlist, weight=1):
            # Strip all non-letters and convert to lowercase
                #pattern = re.compile('[\W]+')
                #words_clean = map(lambda x: pattern.sub('', x).lower(), words)
            words_semiclean = map(lambda x: filter(lambda y: y.isalnum() or y.isdigit(), x).lower(), wordlist)
            words_clean = filter(lambda w: not w.isdigit(), words_semiclean)
            # Remove all empty words
            words_filtered = filter(None, words_clean)
            # Remove stopwords
            words_relevant = filter(lambda x: x not in stopwords, words_filtered)

            # Create map with words as key and count as value
            word_counts = {}
            for word in words_relevant:
                if word in word_counts:
                    word_counts[word] += weight
                else:
                    word_counts[word] = weight
            return word_counts

        # Process both sets with different weights
        processed_contents = process_wordlist(wordlist_contents, 1)
        processed_titles = process_wordlist(wordlist_titles, 3)
        
        # Combine both dictionaries, adding values
        words = defaultdict(int)
        for k, v in chain(processed_contents.iteritems(), processed_titles.iteritems()):
            words[k] += v

        # Sort words
        words_sorted = sorted(words.items(), key=lambda x: x[1], reverse=True)

        # Put words that appear enough times in final map
        final = {}
        for word, count in words_sorted[:max_words]:
            if count >= min_word_count:
                final[word] = count
            else:
                break

        # Update context
        context['affair_count'] = affairs.count()
        context['words'] = json.dumps(final)

        return context


class Search(ListView):
    context_object_name = 'persons'
    model = models.Person
    template_name = 'search_results.html'

    def get_queryset(self):
        self.q = filter(lambda c: c.isalnum() or c.isspace(), self.request.GET.get('q', u''))
        if self.q:
            result = self.model.objects
            for word in self.q.split():
                result = result.filter(Q(name__icontains=word) | Q(party__short_name__istartswith=word))
            return result
        return None

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['q'] = self.q
        return context
