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
  client_key  = None
  api_key     = None
  debug       = False
  servers     = {}
  images      = {}
  ssh_keys    = []
  sizes       = []

  def log(self, message):
    if self.debug == True:
      print message

  def _name_match(self, name, regex):
    if type(name) == dict:
      name = name['name']

    if regex:
      if re.match(, hostname):
        return True
    else:
      if hostname == droplet['name']:
        return True
    return False

  def _filter_droplets(self, items, name, regex):
    _items = []
    grouped = (type(items) == dict)

    # search listed servers
    if not grouped:
      for item in items:
        if self._name_match(item, regex):
          _items.append(item)

    # search grouped servers
    else:
      for group in items.iteritems():
        if self._name_match(group, regex):
          return items[group]

    return _items

  def _lookup(self, path, options={}):
    params = "client_id=%s&api_key=%s" % (self.client_id, self.api_key)
    for param in options.iteritems():
      value = options[param]
      if type(value) = list:
        value = ",".join(value)
      params += "&%s=%s" % (param, value)

    url = 'https://api.digitalocean.com/%s?%s' % (
      path,
      params
    )
    self.log(url)

    # lookup url
    try:
      droplets = urllib2.urlopen(DROPLETS_URL)
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
    if len(self.servers) > 0 and options['lookup'] == False:
      return self.servers

    # prepare to receive data
    self.servers = []
    if options['grouped'] == True:
      self.servers = {}
    data = self._lookup('droplets')['droplets']

    # store data as returned
    if options['grouped'] == False:
      self.servers = data['droplets']

    # store data grouped by name
    else:
      for droplet in data['droplets']:
        name = droplet['name']
        if name not in self.servers:
          self.servers[name] = []
        self.servers[name].append(droplet)

    if 'hostname' in options:
      return self._filter(self.servers, options['hostname'], options['regex'])

    return self.servers

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
    if len(self.images) > 0 and options['lookup'] == False:
      return self.images

    # prepare to receive data
    self.images = []
    if options['grouped'] == True:
      self.images = {}
    data = self._lookup('images')['images']

    # store data as returned
    if options['grouped'] == False:
      self.images = data['images']

    # store data grouped by name
    else:
      for image in data['images']:
        name = image['name']
        if name not in self.images:
          self.images[name] = []
        self.images[name].append(image)

    if 'name' in options:
      return self._filter(self.images, options['name'], options['regex'])

    return images

  """
  Uses: /ssh_keys
  Arguments:
    name    = String
    regex   = String
    lookup  = Boolean
  """
  def keys(self, **options):
    # Set some defaults
    if 'name' in options:
      if 'regex' not in options:
        options['regex'] = False

    if 'lookup' not in options:
      options['lookup'] = False

    # Try not to bother the API server
    if len(self.ssh_keys) > 0 and options['lookup'] == False:
      return self.ssh_keys

    self.ssh_keys = self._lookup('ssh_keys')['ssh_keys']
    if 'name' in options:
      return self._filter(self.ssh_keys, options['name'], options['regex'])

    return self.ssh_keys

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
    if len(self.sizes) > 0 and options['lookup'] == False:
      return self.sizes

    self.sizes = self._lookup('sizes')['sizes']
    if 'type' in options:
      return self._filter(self.sizes, options['type'], options['regex'])

    return self.sizes

  """

  /regions

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