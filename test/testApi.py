import cv2
import numpy as np
import os
import requests
import base64
import json
import pprint
import unittest
import time
import glob


TEST_HOST = "127.0.0.1"
TEST_PORT = "5003"

abspath = os.path.dirname(os.path.abspath(__file__))
jsonPath = os.path.join(abspath, '*.json')


def testApi():
    return True


class IDReaderTest(unittest.TestCase):
    def test(self):
        files = []
        for ext in ('*.json', ):
            files.extend(glob.glob(os.path.join(jsonPath, ext)))
        self.assertEqual(testApi(), len(files))
