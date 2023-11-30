"""Base class for integration tests."""
from collective.portletmetadata.testing import PLONE_APP_PORTLETS_INTEGRATION_TESTING

import unittest
from plone.testing.zope import Browser
import gc
from gc import get_objects
from collections import Counter
import typing

def count_object_types():
    all_objects = get_objects()
    def hashable_objects():
        for o in all_objects:
            try:
                #hash(o)
                #o == ""
                yield type(o).__name__
            except:
                continue
    return Counter(o for o in hashable_objects())

class PortletsTestCase(unittest.TestCase):
    """Base class for integration tests for plone.app.portlets. This may
    provide specific set-up and tear-down operations, or provide convenience
    methods.
    """

    layer = PLONE_APP_PORTLETS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.folder = self.portal["folder"]
        self.request = self.layer["request"]

        self.afterSetUp()

    def afterSetUp(self):
        pass


    def test_render_portlet(self):
        b = Browser(self.layer['app'])
        b.open(self.portal.absolute_url())
        self.assertIn('class="myclass"', b.contents)
        # Was trying to find a memory leak but nothing showed up
        # self.assertMemorySame()
        # Browser(self.layer['app']).open(self.portal.absolute_url())
        # self.assertMemorySame()

    def assertMemorySame(self):
        gc.collect()
        self.assertListEqual(gc.garbage, [])
        # print(gc.get_stats())
        if not hasattr(self, '_savepoints'):
            self._savepoints = []
            self._counts = []
        self._counts.append( len(get_objects()) )
        self._savepoints.append(count_object_types())
        if len(self._savepoints) < 2:
            return
        #compare the savepoints
        for t in self._savepoints[-1]:
            was = self._savepoints[-2].get(t, 0)
            diff = self._savepoints[-1][t] - was
            if diff > 0:
                print('type {} increased by {} instances'.format(t, diff))
        for c1, c2 in zip(self._counts, self._counts[1:]):
            self.assertEqual(c2-c1, 0)
