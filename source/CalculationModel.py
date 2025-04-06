class CalculationModel:
  level = 0
  heroes = 0
  emeralds = 0

  @staticmethod
  def set_level(level: int):
    CalculationModel.level = (level // 250) * 250

  @staticmethod
  def set_heroes(heroes: int):
    CalculationModel.heroes = (heroes // 4) * 4
  
  @staticmethod
  def set_emeralds(emeralds: int):
    CalculationModel.emeralds = emeralds

  @staticmethod
  def reset_model():
    CalculationModel.level = 0
    CalculationModel.heroes = 0
    CalculationModel.emeralds = 0