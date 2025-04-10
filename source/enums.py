import enum

class Strategy(enum.Enum):
  bottles = 'bottles'
  emeralds = 'emeralds'

class DarkRitualsAmount(enum.IntEnum):
  Three = 3,
  Two = 2,
  One = 1

class CalculatorSteps(enum.Enum):
  start = 'start'
  last_mine_level = 'last_mine_level'
  heroes_amount ='heroes_amount'
  emeralds = 'emeralds'
  bottles = 'bottles'
  dr_amount = 'dr_amount'
  result = 'result',

  