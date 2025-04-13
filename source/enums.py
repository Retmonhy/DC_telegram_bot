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
  level_input = 'level_input'
  heroes_input ='heroes_input'
  mode_selection = 'mode_selection'
  emeralds_input = 'emeralds_input'
  bottles_input = 'bottles_input'
  dr_amount_selection = 'dr_amount_selection'
  result = 'result',

  