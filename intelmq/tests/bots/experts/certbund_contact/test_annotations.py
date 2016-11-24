# -*- coding: utf-8 -*-

"""
Testing annotations
"""

import json

import unittest

from intelmq.bots.experts.certbund_contact.annotations import from_json, \
     AnnotationError


class TestAnnotations(unittest.TestCase):

    def test_tag(self):
        tag = from_json(json.loads('{"type": "tag", "value": "daily"}'))
        self.assertEqual(tag.value, "daily")

    def test_tag_no_value(self):
        with self.assertRaises(AnnotationError):
            from_json(json.loads('{"type": "tag"}'))

    def test_tag_non_string_value(self):
        with self.assertRaises(AnnotationError):
            from_json(json.loads('{"type": "tag", "value": 123}'))

    def test_inhibition(self):
        tag = from_json(json.loads('{"type": "inhibition"'
                                   ',"condition":'
                                   '["eq"'
                                   ', ["event_field"'
                                   '  , "classification.identifier"'
                                   '  ]'
                                   ', "openportmapper"]'
                                   '}'))
        self.assertTrue(tag.matches({"classification.identifier":
                                     "openportmapper"}))
        self.assertFalse(tag.matches({"classification.identifier":
                                      "openmongodb"}))

    def test_inhibition_unknown_function(self):
        with self.assertRaises(AnnotationError):
            from_json(json.loads('{"type": "inhibition"'
                                 ',"condition": ["some_function", 1, "value"]'
                                 '}'))

    def test_inhibition_eq_missing_parameters(self):
        with self.assertRaises(AnnotationError):
            from_json(json.loads('{"type": "inhibition"'
                                   ',"condition":'
                                 '["eq", "openportmapper"]'
                                 '}'))



if __name__ == "__main__":
    unittest.main()
