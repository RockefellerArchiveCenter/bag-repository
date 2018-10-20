import json
from os.path import isdir, join
from os import makedirs, listdir, remove
import shutil

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from .cron import BagStore
from .models import Accession, Bag
from .library import BagProcessor
from .views import AccessionViewSet
from ursa_major import settings

data_fixture_dir = join(settings.BASE_DIR, 'fixtures', 'json')
bag_fixture_dir = join(settings.BASE_DIR, 'fixtures', 'bags')


class BagTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        for d in [settings.TEST_LANDING_DIR, settings.TEST_STORAGE_DIR]:
            if isdir(d):
                shutil.rmtree(d)

    def createobjects(self):
        accession_count = 0
        transfer_count = 0
        for f in listdir(data_fixture_dir):
            with open(join(data_fixture_dir, f), 'r') as json_file:
                accession_data = json.load(json_file)
                request = self.factory.post(reverse('accession-list'), accession_data, format='json')
                response = AccessionViewSet.as_view(actions={"post": "create"})(request)
                self.assertEqual(response.status_code, 200, "Wrong HTTP code")
                print('Created accession')
                accession_count += 1
                transfer_count += len(accession_data['transfers'])
        self.assertEqual(len(Accession.objects.all()), accession_count, "Wrong number of accessions created")
        self.assertEqual(len(Bag.objects.all()), transfer_count, "Wrong number of transfers created")

    def processbags(self):
        shutil.copytree(bag_fixture_dir, settings.TEST_LANDING_DIR)
        processor = BagProcessor(dirs={"landing": settings.TEST_LANDING_DIR, "storage": settings.TEST_STORAGE_DIR})
        for bag in Bag.objects.all():
            run = processor.run(bag)
            self.assertTrue(run)

    def tearDown(self):
        for d in [settings.TEST_LANDING_DIR, settings.TEST_STORAGE_DIR]:
            if isdir(d):
                shutil.rmtree(d)

    def test_bags(self):
        self.createobjects()
        self.processbags()
