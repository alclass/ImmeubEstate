#!/usr/bin/env python3

import func.db.json_tofrom.json_readers as jreader

COUNTRIES2LETTER_TO_N_DICT = {
  'br' : 55,
  'us' : 1,
}
COUNTRIES_NAME_LANG_DICT = {
  'br': {
    'EN': 'Brazil',
    'FR': 'Brésil',
    'PT': 'Brasil',
  },
  'us': {
    'EN': 'United States',
    'FR': 'États Unis',
    'PT': 'Estados Unidos',
  }
}

class City:

  def __init__(self, city_id, cityname=None, state2letter=None, country2letter=None):
    self.city_id        = city_id
    self.cityname       = cityname
    self.state2letter   = state2letter
    self.country2letter = country2letter
    self._country_id = None
    self.find_n_set_country_id()

  @classmethod
  def fetch_city_by_id_from_json(cls, city_id):
    '''
    Temporary presence. This method should not be here, just the one below.  This class should be not know how a dict is fetched, ie, coupling here should be weak,
      so that any souce of dict's only then send dict's to cls.create_city_by_dict(city_dict) below
    :param cls:
    :param city_id:
    :return:
    '''
    oreader = jreader.DataGroupJsonReader(jreader.DG_CITY)
    city_dict = oreader.get_dict_by_id_from_json(city_id)
    return cls.create_city_by_dict(city_dict)

  @classmethod
  def create_city_by_dict(cls, city_dict):
    city_id = city_dict['city_id']
    cityobj = cls(city_id)
    for k in city_dict:
      if k == 'city_id':
        continue
      setattr(cityobj, k, city_dict[k])
    return cityobj

  def find_n_set_country_id(self):
    if self._country_id is not None:
      return self._country_id
    try:
      self._country_id = COUNTRIES2LETTER_TO_N_DICT[self.country2letter]
      return self._country_id
    except (KeyError): # , ValueError
      pass
    return 's/i'

  @property
  def country_id(self):
    return self.find_n_set_country_id()

  def get_country_name_by_lang(self, plang2letter='PT'):
    lang2letter = plang2letter.upper()
    try:
      return COUNTRIES_NAME_LANG_DICT[self.country2letter][lang2letter]
    except KeyError:
      pass
    return 's/inf'

  def __str__(self):
    return 'City ' + self.cityname

# ADDRESS_TYPES not yet used
ADDRESS_TYPES = ['Avenida', 'Beco', 'Praça', 'Rua']

class Address:
  '''

  Attributes:
{
  "address_id": "20550045", "zipcode": "20550045",
  "addressname": "Carmela Dutra", "neighbourhood": "Tijuca", address_type='Rua', city_id='rjrj',
  n_in_address=76, address_complement=201 location_ref=None,
},

  '''

  def __init__(self, address_id, zipcode=None,
      addressname=None, neighbourhood=None, address_type='Rua', city_id='rjrj',
       n_in_address=None, address_complement=None, location_ref=None
    ):
    '''

    :param address_id:
    :param zipcode:
    :param address_type:
    :param addressname:
    :param neighbourhood:
    :param city_id:
    :param n_in_address:
    :param address_complement:
    '''
    self.address_id   = address_id
    self.zipcode      = zipcode
    self.address_type = address_type
    self.addressname  = addressname
    self.neighbourhood= neighbourhood
    self.city_id      = city_id
    self.cityobj      = None # fetchable
    self.n_in_address = n_in_address # set later by user object
    self.address_complement = address_complement # idem
    self.location_ref       = location_ref # idem
    #self.complement_city()

  def expand_attributes_from_json_if_needed(self):
    '''
    This method should not be called from __init__()
    DO NOT call this method from __init__(), otherwise classmethods that instance its objects will not function correctly
    :return:
    '''
    if self.address_id is None:
      return
    oreader = jreader.DataGroupJsonReader(jreader.DG_ADDRESS)
    pdict = oreader.get_dict_by_id_from_json(self.address_id)
    if pdict is None:
      return
    for k in pdict:
      if k == 'address_id':
        continue
      setattr(self, k, pdict[k])
    self.find_n_set_cityobj()

  @classmethod
  def fetch_address_from_json_by_id(cls, address_id):
    '''
    Temporary presence. This method should not be here, just the one below.  This class should be not know how a dict is fetched, ie, coupling here should be weak,
      so that any souce of dict's only then send dict's to cls.create_city_by_dict(city_dict) below
    :param cls:
    :param city_id:
    :return:
    '''
    oreader = jreader.DataGroupJsonReader(jreader.DG_ADDRESS)
    pdict = oreader.get_dict_by_id_from_json(address_id)
    address = cls.create_address_by_dict(pdict)
    address.find_n_set_cityobj()
    return address

  @classmethod
  def create_address_by_dict(cls, pdict):
    '''
    Consider this method a private static one (ie, it's static and should only be called from fetch_address_from_json_by_id(cls, address_id) above
    :param pdict:
    :return:
    '''
    address_id = pdict['address_id']
    if address_id is None:
      return None
    obj = cls(address_id)
    for k in pdict:
      if k == 'address_id':
        continue
      setattr(obj, k, pdict[k])
    return obj

  def find_n_set_cityobj(self):
    if self.cityobj is not None:
      return self.cityobj
    self.cityobj = City.fetch_city_by_id_from_json(self.city_id)
    return self.cityobj

  @property
  def city(self):
    if self.find_n_set_cityobj() is None:
      return 's/inf'
    return self.cityobj.cityname

  @property
  def state2letter(self):
    if self.cityobj is not None:
      return self.cityobj.state2letter
    return 's/inf'

  @property
  def country2letter(self):
    c2letter = None
    if self.cityobj is not None:
      return self.cityobj.country2letter
    return 's/inf'

  def get_country_name(self):
    countryname = ''
    if self.cityobj is not None:
      countryname = self.cityobj.get_country_name_by_lang()
    if countryname == 's/inf':
      countryname = ''
    return countryname


  def str_as_lines(self):
    lines = []
    line = '%(address_type)s %(addressname)s, %(n_in_address)s / %(complement)s' %{
      'address_type' : self.address_type,
      'addressname'  : self.addressname,
      'n_in_address' : self.n_in_address,
      'complement'   : self.address_complement,
    }
    lines.append(line)
    line = '%(neighbourhood)s - %(city)s - %(state)s' %{
      'neighbourhood': self.neighbourhood,
      'city' : self.city,
      'state': self.state2letter,
    }
    countryname =  self.get_country_name()
    if countryname != '':
      line += ' - ' + countryname
    lines.append(line)
    line = '%(zipcode)s' %{
      'zipcode': self.zipcode,
    }
    lines.append(line)
    return lines

  def __str__(self):
    return '\n'.join(self.str_as_lines())

def print_address(address_id, n_in_address, address_complement):
  print ('-'*50)
  print ('Fetching', address_id)
  print ('-'*50)
  address = Address.fetch_address_from_json_by_id(address_id)
  address.n_in_address = n_in_address
  address.address_complement = address_complement
  address.expand_attributes_from_json_if_needed()
  print (address)

def adhost_test():
  # Cdutr
  address_id = zipcode = '20550045'
  print_address(address_id, 76, 201)

  # Hlobo
  address_id = zipcode = '20260142'
  print_address(address_id, 385, 405)

  # Jacum
  address_id = zipcode = '20260320'
  print_address(address_id, 76, 202)

if __name__ == '__main__':
  adhost_test()