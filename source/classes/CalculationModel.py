from enums import DarkRitualsAmount, CalculatorSteps, Strategy
from constants import mines 
class CalculationModel:

  def __init__(self):
    self.level = None
    self.heroes = None
    self.emeralds = None
    self.bottles = None
    self.dark_ritual_amount = DarkRitualsAmount.Three
    self.strategy = None
    self.current_step: CalculatorSteps = CalculatorSteps.start

  def set_level(self, level: int):
    if (level >= 20000):
      # 20000 - самая последняя шахта
      self.level = 20000
    else:
      self.level = 0
      for key, value in mines.items():
        if (key <= level):
          self.level = key
          break
      
  def set_heroes(self, heroes: int):
    self.heroes = (heroes // 4) * 4
  
  def set_bottles(self, bottles: int):
    self.bottles = bottles

  def set_emeralds(self, emeralds: int):
    self.emeralds = emeralds

  def set_dr_amount(self, dark_ritual_amount: DarkRitualsAmount):
    self.dark_ritual_amount = dark_ritual_amount
  
  def set_strategy(self, strategy: Strategy):
    self.strategy = strategy

  def reset_model(self):
    self.level = None
    self.heroes = None
    self.emeralds = None
    self.bottles = None
    self.dark_ritual_amount = DarkRitualsAmount.Three
  
  def go_to_step(self, step: CalculatorSteps):
    self.current_step = step