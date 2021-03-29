#!/usr/bin/env python3
import copy
import datetime
import json
import inspect
# from dateutil.relativedelta import relativedelta
# import sys
import func.db.json_tofrom.bills_json_reader as bill_read

def transpose_dict_to_obj(obj, pdict):
  for k in pdict:
    value = pdict[k]
    setattr(obj, k, value)

class BillingItemTypes: # (collections.MutableMapping)

  BI_TYPES_SHORTDESCR = []
  K_IBALANCE = 0; BI_TYPES_SHORTDESCR.append('Saldo Inicial')
  K_RENTVAL  = 1; BI_TYPES_SHORTDESCR.append('Aluguel')
  K_CONDFEE  = 2; BI_TYPES_SHORTDESCR.append('Condomínio')
  K_PROPTAX  = 3; BI_TYPES_SHORTDESCR.append('IPTU')
  K_FDEPTAR  = 4; BI_TYPES_SHORTDESCR.append('Tx Funesbom')
  K_EXTRAIM  = 5; BI_TYPES_SHORTDESCR.append('Extra mês c/incid.')
  K_EXTRAOM  = 6; BI_TYPES_SHORTDESCR.append('Extra mês s/incid.')
  K_PAYMENT  = 7; BI_TYPES_SHORTDESCR.append('Pagamento')
  K_INTNMOCO = 8; BI_TYPES_SHORTDESCR.append('Juros&Corr.Monet.')
  K_INCIDENCE= 9; BI_TYPES_SHORTDESCR.append('Multa Incidência')
  K_FBALANCE =10; BI_TYPES_SHORTDESCR.append('Saldo Final')

  @classmethod
  def get_short_description(cls, typeindex): # self
    try:
      return cls.BI_TYPES_SHORTDESCR[typeindex]
    except KeyError:
      pass
    return 's/inf'

  @classmethod
  def is_inmonth(cls, typeindex):
    '''
      is_inmonth are rentval, condfee, proptax, fdeptar & extraim
    :param typeindex:
    :return:
    '''
    if typeindex == cls.K_RENTVAL:
      return True
    elif typeindex == cls.K_CONDFEE:
      return True
    elif typeindex == cls.K_PROPTAX:
      return True
    elif typeindex == cls.K_FDEPTAR:
      return True
    elif typeindex == cls.K_EXTRAIM:
      return True
    return False

  @classmethod
  def is_grouper(cls, typeindex):
    '''
      is_grouper are int_n_monetcorr & payment
    :param typeindex:
    :return:
    '''
    if typeindex == cls.K_PAYMENT:
      return True
    elif typeindex == cls.K_INTNMOCO:
      return True
    return False

class BillingItem:
  '''

  {'contract_id': 'HLB01', 'refmonthdate': '2019-09-01', 'duedate': '2019-10-10', 'status': 'closed', 'ini_balance': 0,
   'total_when_open': 2919.38, 'total_paid': 2919.38, 'fin_balance': 0,
   'billingitems': [
    {'seq':None, 'itdate':None, 'description':None, 'ittype':None, 'itvalue':None, 'itobs':None, 'itformula':None, 'is_inmonth':None, 'is_grouper':None},
   ]
   'quad_payment_namedtuplelist': [
   (paydatetime='2019-10-10 12:00:00', payvalue=None, payauthstring=None, payobs=None),
   ]

  '''

  base_attrib_dict = {
    'seq':None,
    'itdate':None,
    'description':None,
    'ittype':None,
    'itvalue':None,
    'itobs':None,
    'itformula':None,
    'is_inmonth':None, # is_inmonth's are rentval, condfee, proptax, fdeptar & extraim
    'is_grouper':None  # groups are int_n_monetcorr & payment
  }

  def __init__(self, billing_item_dict):
    self.instance_attrib_dict = copy.copy(self.base_attrib_dict)
    transpose_dict_to_obj(self, self.instance_attrib_dict)
    transpose_dict_to_obj(self, billing_item_dict)
    self.complement_isinmonth_n_isgrouper()
    self.sync_dict_with_obj()

  def complement_isinmonth_n_isgrouper(self):
    if self.is_inmonth is None:
      self.is_inmonth = BillingItemTypes.is_inmonth(self.ittype)
    if self.is_grouper is None:
      self.is_grouper = BillingItemTypes.is_grouper(self.ittype)


  def sync_dict_with_obj(self):
    for strkey in self.instance_attrib_dict:
      value = None
      try:
        value = getattr(self, strkey)
      except AttributeError:
        pass
      if value is None:
        continue
      if self.instance_attrib_dict[strkey] != value:
        self.instance_attrib_dict[strkey] = value

  def __getitem__(self, fieldname):
    try:
      return getattr(self, fieldname)
    except AttributeError:
      pass
    if fieldname in self.instance_attrib_dict:
      setattr(self, fieldname, self.instance_attrib_dict[fieldname])
      return self.instance_attrib_dict[fieldname]
    return None

  def __lt__(self, other):
    if self.ittype == other.ittype:
      if self.itdate < other.itdate:
        return True
    if self.ittype < other.ittype:
      return True
    return False

  def __gt__(self, other):
    if self.ittype == other.ittype:
      if self.itdate > other.itdate:
        return True
    if self.ittype > other.ittype:
      return True
    return False

  def __eq__(self, other):
    if self.ittype == other.ittype and self.itdate == other.itdate:
      return True
    return False

  def to_json(self):
    self.sync_dict_with_obj()
    instance_attrib_dict = copy.copy(self.instance_attrib_dict)
    for k in instance_attrib_dict:
      value = instance_attrib_dict[k]
      if type(value) in [datetime.date, datetime.datetime]:
        value = str(value)
        instance_attrib_dict[k]=value
    return json.dumps(instance_attrib_dict, ensure_ascii=False)

  def __str__(self):
    outlist = [self.seq, self.ittype, self.description, self.itvalue]
    outstr = '%s' %(self.instance_attrib_dict)
    return outstr

class BillingItems(list):

  def __init__(self):
    super().__init__()

  def __add__(self, other):
    pass

  def verify(self):
    for e in self:
      if type(e) != BillingItem:
        error_msg = 'element in BillingItems (list) is not a BillingItem (instanced)'
        raise Exception(error_msg)

  def __str__(self):
    return self.pretty_print_bill()

lambdainspect = lambda x : not inspect.ismethod(x)
fnotstartswithunderline = lambda s : not s.startswith('_')
def pick_up_attribs(obj):
  fields = list(filter(lambdainspect, dir(obj)))
  print('after lambdainspect', fields)
  fields = list(filter(fnotstartswithunderline, fields))
  print ('after fnotstartswithunderline', fields)

def create_adhoctest_bill():
  base_attrib_dict = {
    'seq':1,
    'itdate':datetime.date.today(),
    'description':None,
    'ittype':'RENTVAL',
    'itvalue':3000,
    'itobs':None,
    'itformula':None,
    'is_inmonth':True,
    'is_grouper':False
  }
  bitem = BillingItem(base_attrib_dict)
  print (bitem)
  print ('='*50)
  print (bitem.to_json())
  attribs = pick_up_attribs(bitem)
  print(attribs)

def read_bill_from_json():
  bill_id = '20190901HLB01'
  bill_read.get_bill_by_id(bill_id)

def test1():
  integerset = list(range(10))
  print (integerset)
  lambdaeven = lambda x : x % 2 == 0
  evenlist = list(filter(lambdaeven, integerset))
  print (evenlist)


def process():
  #test1()
  #return
  create_adhoctest_bill()
  for i in range(11):
    print (BillingItemTypes.get_short_description(i))

if __name__ == '__main__':
  process()
