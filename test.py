import os
import unittest
from digital_ocean import DigitalOceanApi

digital_ocean = DigitalOceanApi()


class TestApi(unittest.TestCase):
  def testDroplets(self):
    self.failUnless(len(digital_ocean.droplets())>0)

  def testImages(self):
    self.failUnless(len(digital_ocean.images())>0)

  def testRegions(self):
    self.failUnless(len(digital_ocean.regions())>0)

  def testSizes(self):
    self.failUnless(len(digital_ocean.sizes())>0)

  def testKeys(self):
    self.failUnless(len(digital_ocean.ssh_keys())>0)


def main():
  digital_ocean.debug       = True
  digital_ocean.client_id   = os.environ['DO_CLIENT_ID']
  digital_ocean.api_key     = os.environ['DO_API_KEY']
  unittest.main()


if __name__ == '__main__':
  main()