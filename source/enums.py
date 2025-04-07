import enum

class CalculationMode(enum.IntEnum):
  Three = 3,
  Two = 2,
  One = 1

class CalculatorSteps(enum.Enum):
  start = 'start'
  last_mine_level = 'last_mine_level'
  heroes_amount ='heroes_amount'
  emeralds = 'emeralds'
  mode = 'mode'
  result = 'result',
  end = 'end'

  