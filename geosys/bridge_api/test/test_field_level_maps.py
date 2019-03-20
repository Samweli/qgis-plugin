# coding=utf-8
"""Bridge API connection test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import unittest

from geosys.bridge_api.connection import ConnectionAPIClientV2
from geosys.bridge_api.default import IDENTITY_URLS, BRIDGE_URLS
from geosys.bridge_api.field_level_maps import FieldLevelMapsAPIClientV4

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


class BridgeAPIFieldLevelMapsTest(unittest.TestCase):
    """Test Bridge API field-level-maps works."""

    def setUp(self):
        """Runs before each test."""
        client = ConnectionAPIClientV2(IDENTITY_URLS['na']['test'])
        json = client.get_access_token('Bridge_US_Demo', 'Welcome12k18')
        self.assertTrue('access_token' in json)
        self.access_token = json['access_token']

    def tearDown(self):
        """Runs after each test."""
        pass

    def test_get_coverage(self):
        """Test we can successfully get the access token."""
        data = {
          "Geometry": "POLYGON(("
                      "-86.86701653386694 41.331532756357426,"
                      "-86.86263916875464 41.331532756357426,"
                      "-86.86263916875464 41.32450729144166,"
                      "-86.86701653386694 41.32450729144166,"
                      "-86.86701653386694 41.331532756357426))",
          "Crop": {
            "Id": "CORN"
          },
          "SowingDate": "2018-04-15"
        }

        filters = {
            "Image.Date": "$gte:2010-01-01",
            "coverageType": "CLEAR"
        }

        client = FieldLevelMapsAPIClientV4(
            self.access_token, endpoint_url=BRIDGE_URLS['na']['test'])
        response = client.get_coverage(data=data, filters=filters)
        self.assertIsInstance(response, list)

    def test_get_field_map(self):
        """Test we can successfully get the requested field map."""
        client = FieldLevelMapsAPIClientV4(
            self.access_token, endpoint_url=BRIDGE_URLS['na']['test'])

        # Test INSEASONFIELD_AVERAGE_NDVI map creation
        data = {
            "SeasonField": {
                "Id": "zgzmbrm"
            },
            "Image": {
                "Date": "2018-10-13"
            },
            "NPlanned": 48,
            "NMin": 20,
            "NMax": 70
        }
        response = client.get_field_map(
            'inseason-field-average-ndvi', data=data)
        self.assertTrue('seasonField' in response)


if __name__ == "__main__":
    suite = unittest.makeSuite(BridgeAPIFieldLevelMapsTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)