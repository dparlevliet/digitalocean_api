"""
@fileoverview Digital Ocean API
@author David Parlevliet
@version 20131208
@preserve Copyright 2013 David Parlevliet.

Digital Ocean API
=================
Class to get the server details via the Digital Ocean API.
"""
import urllib2
import json
import re
from copy import copy

class DigitalOceanApi():
  client_id             = None
  api_key               = None
  debug                 = False
  account_droplets      = {}
  account_images        = []
  account_ssh_keys      = []
  droplet_sizes         = []
  digitalocean_regions  = []

  def log(self, message):
    if self.debug == True:
      print message

  def _name_match(self, name, pattern, regex):
    if type(name) == dict:
      name = name['name']

    if regex:
      if re.match(name, pattern):
        return True
    else:
      if pattern == name:
        return True
    return False

  def _filter(self, items, name, regex):
    _items = []
    grouped = (type(items) == dict)

    # search listed servers
    if not grouped:
      for item in items:
        if self._name_match(item, name, regex):
          _items.append(item)

    # search grouped servers
    else:
      for groupname in items.iteritems():
        if self._name_match(groupname, name, regex):
          return items[groupname]

    return _items

  def _lookup(self, path, options={}):
    params = "client_id=%s&api_key=%s" % (self.client_id, self.api_key)
    for param in options.iteritems():
      value = options[param]
      if type(value) == list:
        value = ",".join(value)
      params += "&%s=%s" % (param, value)

    url = 'https://api.digitalocean.com/%s?%s' % (
      path,
      params
    )
    self.log(url)

    # lookup url
    try:
      droplets = urllib2.urlopen(url)
    except urllib2.URLError:
      self.log(urllib2.URLError)
      raise Exception("Fatal error: Unable to connect to API")

    # read response
    try:
      data = droplets.read()
    except:
      raise Exception("Fatal error: Unable to read data returned.")
    finally:
      self.log(data)
    
    # parse data
    data = json.loads(data)
    self.log(data)
    return data

  """
  Uses: /droplets
  Arguments:
    hostname = String
    regex    = Boolean
    lookup   = Boolean
    grouped  = Boolean
  """
  def droplets(self, **options):
    # Set some defaults
    if 'name' in options:
      if 'regex' not in options:
        options['regex'] = False

    if 'lookup' not in options:
      options['lookup'] = False

    if 'grouped' not in options:
      options['grouped'] = False

    # Try not to bother the API server
    if len(self.account_droplets) > 0 and options['lookup'] == False:
      return self.account_droplets

    # prepare to receive data
    self.account_droplets = []
    if options['grouped'] == True:
      self.account_droplets = {}
    data = self._lookup('droplets')['droplets']

    # store data as returned
    if options['grouped'] == False:
      self.account_droplets = data

    # store data grouped by name
    else:
      for droplet in data:
        name = droplet['name']
        if name not in self.account_droplets:
          self.account_droplets[name] = []
        self.account_droplets[name].append(droplet)

    if 'hostname' in options:
      return self._filter(self.account_droplets, options['hostname'], options['regex'])

    return self.account_droplets

  """
  Uses: /droplets/new
  """
  def droplet_new(self, **options):
    return self._lookup('droplets/new', options)

  """
  Uses: /droplets/[droplet_id]
  """
  def droplet_status(self, id):
    return self._lookup('droplets/%s' % id)

  """
  Uses: /droplets/[droplet_id]/<action>
  Available actions:
    reboot
    power_cycle
    shutdown
    power_off
    power_on
    password_reset
    resize
    snapshot
    restore
    rebuild
    enable_backups
    disable_backups
    rename
    destroy
  """
  def droplet_action(self, id, action, **options):
    return self._lookup('droplets/%s/%s' % (id, action), options)

  """
  Uses: /images
  Arguments:
    name    = String
    regex   = String
    grouped = Boolean
    lookup  = Boolean
  """
  def images(self, **options):
    # Set some defaults
    if 'name' in options:
      if 'regex' not in options:
        options['regex'] = False

    if 'lookup' not in options:
      options['lookup'] = False

    if 'grouped' not in options:
      options['grouped'] = False

    # Try not to bother the API server
    if len(self.account_images) > 0 and options['lookup'] == False:
      return self.account_images

    # prepare to receive data
    self.account_images = []
    if options['grouped'] == True:
      self.account_images = {}
    data = self._lookup('images')['images']

    # store data as returned
    if options['grouped'] == False:
      self.account_images = data

    # store data grouped by name
    else:
      for image in data:
        name = image['name']
        if name not in self.account_images:
          self.account_images[name] = []
        self.account_images[name].append(image)

    if 'name' in options:
      return self._filter(self.account_images, options['name'], options['regex'])

    return self.account_images

  """
  Uses: /ssh_keys
  Arguments:
    name    = String
    regex   = String
    lookup  = Boolean
  """
  def ssh_keys(self, **options):
    # Set some defaults
    if 'name' in options:
      if 'regex' not in options:
        options['regex'] = False

    if 'lookup' not in options:
      options['lookup'] = False

    # Try not to bother the API server
    if len(self.account_ssh_keys) > 0 and options['lookup'] == False:
      return self.account_ssh_keys

    self.account_ssh_keys = self._lookup('ssh_keys')['ssh_keys']
    if 'name' in options:
      return self._filter(self.account_ssh_keys, options['name'], options['regex'])

    return self.account_ssh_keys

  """
  Uses: /sizes
  Arguments:
    type    = String
    regex   = String
    lookup  = Boolean
  """
  def sizes(self, **options):
    # Set some defaults
    if 'name' in options:
      if 'regex' not in options:
        options['regex'] = False

    if 'lookup' not in options:
      options['lookup'] = False

    # Try not to bother the API server
    if len(self.droplet_sizes) > 0 and options['lookup'] == False:
      return self.droplet_sizes

    self.droplet_sizes = self._lookup('sizes')['sizes']
    if 'type' in options:
      return self._filter(self.droplet_sizes, options['type'], options['regex'])

    return self.droplet_sizes

  """
  Uses: /regions
  Arguments:
    name    = String
    regex   = String
    lookup  = Boolean
  """
  def regions(self, **options):
    # Set some defaults
    if 'name' in options:
      if 'regex' not in options:
        options['regex'] = False

    if 'lookup' not in options:
      options['lookup'] = False

    # Try not to bother the API server
    if len(self.digitalocean_regions) > 0 and options['lookup'] == False:
      return self.digitalocean_regions

    self.digitalocean_regions = self._lookup('regions')['regions']
    if 'name' in options:
      return self._filter(self.digitalocean_regions, options['name'], options['regex'])

    return self.digitalocean_regions



  """
  /images/[image_id]
  /images/[image_id]/destroy
  /images/[image_id]/transfer

  /ssh_keys/new
  /ssh_keys/[ssh_key_id]
  /ssh_keys/[ssh_key_id]/edit
  /ssh_keys/[ssh_key_id]/destroy
  
  /domains
  /domains/new
  /domains/[domain_id]
  /domains/[domain_id]/destroy
  /domains/[domain_id]/records
  /domains/[domain_id]/records/new
  /domains/[domain_id]/records/[record_id]
  /domains/[domain_id]/records/[record_id]/edit
  /domains/[domain_id]/records/[record_id]/destroy

  /events/[event_id]
  """

digital_ocean = DigitalOceanApi()