import datetime

class A:
  def __init__(self):
    self.attr = 'class A'
    print (self.attr)
    self.x = 1

  def __eq__(self, other):
    if self.x == other.x:
      return True
    return False

class B(A):
  def __init__(self):
    super().__init__()
    self.attr = 'class B'
    print (self.attr)
    self.x = 1

class C(A):
  def __init__(self):
    super().__init__()
    self.attr = 'class B'
    print (self.attr)
    self.x = 2

def adhoc_test1():
  a = A()
  b = B()
  c = C()
  print (a == c)

def adhoc_test2():
  d = datetime.date(2019, 9, 1)
  print(d)

def process():
  adhoc_test2()

if __name__ == '__main__':
  process()