class BoardAccessor:
  @classmethod
  def index(cls, x, y):
    return x + y * 7

  @classmethod
  def on(cls, val, x, y):
    idx = cls.index(x, y)
    val = val | (1 << idx)
    return val
  
  @classmethod
  def off(cls, val, x, y):
    idx = cls.index(x, y)
    val = val & (~(1 << idx))
    return val

  @classmethod
  def isOn(cls, val, x, y):
    idx = cls.index(x, y)
    return (val & (1 << idx)) != 0

  @classmethod
  def isOff(cls, val, x, y):
    return not cls.isOn(val, x, y)

  @classmethod
  def get(cls, val, x, y):
    if cls.isOn(val, x, y):
      return 1
    else:
      return 0

  @classmethod
  def count(cls, val):
    c = 0
    for x in range(7):
      for y in range(7):
        if cls.isOn(val, x, y):
          c += 1

    return c

  @classmethod
  def dump(cls, val):
    print("----------------")
    for x in range(7):
      for y in range(7):
        print('{0}'.format(cls.get(val, x, y)), end="")
        
      print("")

class Board:
  boardBuff = []

  def __init__(self):    
    initTable = [
      [-1, -1,  1,  1,  1, -1, -1],
      [-1, -1,  1,  1,  1, -1, -1],
      [ 1,  1,  1,  1,  1,  1,  1],
      [ 1,  1,  1,  0,  1,  1,  1],
      [ 1,  1,  1,  1,  1,  1,  1],
      [-1, -1,  1,  1,  1, -1, -1],
      [-1, -1,  1,  1,  1, -1, -1],
    ]
    val = 0
    for x in range(7):
      for y in range(7):
        if initTable[x][y] == 1:
          val = BoardAccessor.on(val, x, y)
    self.boardBuff.append(val)

  def getMovedGrid(self, x, y, d, l):
    if d == 0:
      return (x, y - l)
    elif d == 1:
      return (x + l, y)
    elif d == 2:
      return (x, y + l)
    else:
      return (x - l, y)

  def isInBoard(self, x, y):
    if x < 0 or x >= 7 or y < 0 or y >= 7:
      return False
    else:
      return abs(x - 3) <= 1 or abs(y - 3) <= 1

  def next(self, buff):
    val = buff[-1]

    if BoardAccessor.count(val) == 1:
      for b in buff:
        BoardAccessor.dump(b)
      return True

    for x in range(7):
      for y in range(7):
        if not self.isInBoard(x,y):
          continue

        v = BoardAccessor.get(val, x, y)
        if v == 0:
          continue

        for d in range(4):
          (nx2, ny2) = self.getMovedGrid(x, y, d, 2)

          if not self.isInBoard(nx2, ny2):
            continue

          n2 = BoardAccessor.get(val, nx2, ny2)
          if n2 != 0:
            continue

          (nx1, ny1) = self.getMovedGrid(x, y, d, 1)
          n1 = BoardAccessor.get(val, nx1, ny1)
          if n1 == 1:
            nextVal = val
            nextVal = BoardAccessor.off(nextVal, x, y)
            nextVal = BoardAccessor.off(nextVal, nx1, ny1)
            nextVal = BoardAccessor.on(nextVal, nx2, ny2)

            buff.append(nextVal)
            if self.next(buff):
              return True
            else:
              buff.pop()

    return False

  def calc(self):
    self.next(self.boardBuff)

board = Board()
board.calc()

