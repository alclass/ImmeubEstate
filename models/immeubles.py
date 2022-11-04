#!/usr/bin/env python3
import fs.db.json_tofrom.json_readers as jreader

import models.addresses

def get_corr_monet_percent_for_month_year(month_year=None):
  return 0.38

class User:

  def __init__(self, name, cpf, address):
    self.name = name
    self.address = address
    self.cpf = cpf

  def __str__(self):
    outstr = '''name = %(name)s
    cpf = %(cpf)s
    _address = %(_address)s
    '''
    return outstr


class Immeuble:

  def __init__(self, immeuble5letter, address_id=None,
      inscr_munic=None, inscr_funesbom=None, inscr_rgi=None, immeuble_type=None,
      area_m2=None, n_quartos=None, n_banheiros=None, construction_year=None,
      n_in_address=None, address_complement=None, location_ref=None,
      floor=None, floors_in_building=None,
    ):
    self.immeuble5letter = immeuble5letter.upper()
    self.address_id      = address_id
    self._address         = None
    self.inscr_munic     = inscr_munic
    self.inscr_funesbom  = inscr_funesbom
    self.inscr_rgi       = inscr_rgi
    self.immeuble_type   = None,
    self.area_m2         = area_m2
    self.n_quartos       = n_quartos
    self.n_banheiros     = n_banheiros
    self.construction_year = construction_year
    self.n_in_address    = n_in_address
    self.address_complement = address_complement
    self.location_ref       = location_ref
    self.floor              = floor
    self.floors_in_building = floors_in_building

  def expand_attributes_from_json(self):
    '''
    This method should not be called from __init__() but is called outside after construction
    :return:
    '''
    if self.immeuble5letter is None:
      error_msg = 'self.immeuble5letter is None in class Immeuble method expand_attributes_from_json_if_needed()'
      raise ValueError(error_msg)
    oreader = jreader.DataGroupJsonReader(jreader.DG_ADDRESS)
    pdict = oreader.get_dict_by_id_from_json(self.immeuble5letter)
    if pdict is None:
      error_msg = 'immeuble5letter %s does not exist in db' %self.immeuble5letter
      raise ValueError(error_msg)
    for k in pdict:
      if k == 'immeuble5letter':
        continue
      setattr(self, k, pdict[k])
    self.set_address()

  @property
  def address(self):
    if self._address is not None:
      return self._address
    return self.find_n_set_address()

  def find_n_set_address(self):
    if self._address is None:
      self.set_address()
    return self._address

  def set_address(self):
    '''

    :return:
    '''
    if self.immeuble5letter is None:
      error_msg = 'self.immeuble5letter is None in set_address() in Immeuble'
      raise ValueError(error_msg)
    if self.address_id is None:
      # avoid using the expand function, because something might already have been changed by its moment
      oreader = jreader.DataGroupJsonReader(jreader.DG_ADDRESS)
      pdict = oreader.get_dict_by_id_from_json(self.immeuble5letter)
      if pdict is None:
        return
      try:
        self.address_id = pdict['address_id']
      except KeyError:
        return
      if self.address_id is None:
        self._address = None
        return
    self._address = models.addresses.addresses.Address.fetch_address_from_json_by_id(self.address_id)
    if self._address is None:
      return
    self._address.n_in_address = self.n_in_address
    self._address.address_complement = self.address_complement
    self._address.location_ref = self.location_ref

  def find_n_set_address(self):
    if self.address_id is None:
      return None
    if self._address is None:
      self.find_n_set_address()
    # it may be None at this point, ie find_n_set_address() may not find it and will set None
    return self._address

  @classmethod
  def fetch_address_by_id(cls, address_id):
    '''
    Temporary presence. This method should not be here, just the one below.  This class should be not know how a dict is fetched, ie, coupling here should be weak,
      so that any souce of dict's only then send dict's to cls.create_city_by_dict(city_dict) below
    :param cls:
    :param city_id:
    :return:
    '''
    oreader = jreader.DataGroupJsonReader(jreader.DG_ADDRESS)
    pdict = oreader.get_dict_by_id_from_json(address_id)
    if pdict is None:
      return None
    return cls.create_address_by_dict(pdict)

  @classmethod
  def fetch_immeuble_by_5letter(cls, immeuble5letter):
    '''
    Temporary presence. This method should not be here, just the one below.  This class should be not know how a dict is fetched, ie, coupling here should be weak,
      so that any souce of dict's only then send dict's to cls.create_city_by_dict(city_dict) below
    :param cls:
    :param city_id:
    :return:
    '''
    oreader = jreader.DataGroupJsonReader(jreader.DG_ADDRESS)
    pdict = oreader.get_dict_by_id_from_json(immeuble5letter)
    return cls.create_address_by_dict(pdict)

  @classmethod
  def create_address_by_dict(cls, pdict):
    address_id = pdict['address_id']
    obj = cls(address_id)
    for k in pdict:
      if k == 'address_id':
        continue
      setattr(obj, k, pdict[k])
    return obj

  def str_as_lines(self):
    lines = []
    line = 'Imóvel %(immeuble5letter)s Características:' %{
      'immeuble5letter' : self.immeuble5letter,
    }
    lines.append(line)
    area_m2 = 's/inf'
    if self.area_m2 is not None:
      area_m2 = self.area_m2
    n_quartos = 's/inf'
    if self.n_quartos is not None:
      n_quartos = self.n_quartos
    line = 'Tipo %(immeuble_type)s | área (m2) %(area_m2)s | n. quartos %(n_quartos)s' %{
      'immeuble_type' : self.immeuble_type,
      'area_m2': str(area_m2),
      'n_quartos': str(n_quartos),
    }
    lines.append(line)
    line = 'Ano Construção %(construction_year)s | RGI %(inscr_rgi)s | Inscr. Munic. %(inscr_munic)s' %{
      'construction_year' : self.construction_year,
      'inscr_rgi': self.inscr_rgi,
      'inscr_munic': self.inscr_munic,
    }
    lines.append(line)
    self.find_n_set_address()
    if self._address is not None:
      address_lines = self._address.str_as_lines()
      lines = lines + address_lines
    return lines

  def __str__(self):
    return '\n'.join(self.str_as_lines())

def print_immeuble(immeuble5letter):
  print('-'*50)
  try:
    immeuble = Immeuble(immeuble5letter)
    immeuble.expand_attributes_from_json()
    print(immeuble)
  except ValueError:
    print(immeuble5letter, 'does not exist in json db.')

def adhoc_test():
  immeuble5letter = 'CDUTR'

  print_immeuble(immeuble5letter)
  immeuble5letter = 'CDUTRA'
  print_immeuble(immeuble5letter)
  immeuble5letter = 'hlobo'
  print_immeuble(immeuble5letter)
  immeuble5letter = 'jacum'
  print_immeuble(immeuble5letter)


if __name__ == '__main__':
  adhoc_test()