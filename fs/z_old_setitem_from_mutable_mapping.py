
def __setitem__(self, key, value):
  '''
  Key, whatever it is, is not used.  The key will be changed in here to last_seq plus a random int 1 to 10
  IMPORTANT:  the dict implementation may change to a list implementation in the future.
  :param key:
  :return:
  '''

  current_key = self.seq
  # the 10-step is to protect against a very remote problem of two attempts to add a record at the same time
  self.seq = current_key + random.randint(1, 11)
  key = self.seq

  # Check that value has the type of the named tuple that stores a billing item
  if type(value) != self.billitem_ntuple_constr:
    error_msg = 'Value must be of type BillItemNamedTuple'
    raise ValueError(error_msg)

  # Set refmonthdate for the first time
  if self.refmonthdate is None:
    itdate = value.itdate
    self.refmonthdate = datetime.date(year=itdate.year, month=itdate.month, day=1)

  if value.ittype == self.KItemTypes.TK_IBALANCE:
    self.ini_balance = value.itvalue

  # Check that dates are the same month and year as refmonthdate
  if not dtfunc.are_same_year_n_same_month(value.itdate, self.refmonthdate):
    error_msg = 'Error: False to dtfunc.are_same_year_n_same_month(value.itdate (=%s), self.refmonthdate (=%s))' % (
    value.itdate, self.refmonthdate)
    raise Exception(error_msg)

    # self.store[self.__keytransform__(key)] = value
    self.ini_balance = value.itvalue
    self.store[key] = value

def __delitem__(self, key):
  del self.store[self.__keytransform__(key)]

def __iter__(self):
  return iter(self.store)

def __len__(self):
  return len(self.store)

def __keytransform__(self, key):
  return key

