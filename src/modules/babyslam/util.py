
""" 
 list with limited length.
 when the list is full and an element is added, the oldest element is removed
 the return value of the 'append' method is the removed element (or None if there is none)
""" 
class Fifo(object):
  def __init__(self, maxsize):
    self.data = []
    self.maxsize = maxsize

  def append(self, obj):
    self.data.append(obj)
    if len(self.data) >= self.maxsize:
        return self.data.pop(0)
    return None

  def __len__(self):
    return len(self.data)

  def __iter__(self):
    return self.data.__iter__()
