from enums import DarkRitualsAmount
from classes.CalculationModel import CalculationModel

# хранит модели игроков(каждая модель рассчета связана с чатом)
class ModelStore:
  model_dict: dict[int, CalculationModel] = {}
  total_calculations: int = 0

  def __init__(self):
    file = open('./calc_count.txt', 'r')
    self.total_calculations = int(file.read())
    file.close()

  def add_model(self, key: int, model: DarkRitualsAmount):
    self.model_dict[key] = model
  
  # вернет существующую модель или создаст новую и вернет, в случае отсутствия модели для этого пользователя 
  def get_model_by_id(self, id: int) -> CalculationModel:
    model = self.model_dict.get(id)
    if (model):
      return model
    else:
      self.add_model(id, CalculationModel())
      return self.get_model_by_id(id)
  
  def delete_model_by_id(self, id: int):
    return self.model_dict.pop(id, None)
  
  def increase_calc_counter(self):
    self.total_calculations += 1
    # открываем/создаем файл рядом с папкой проекта
    file = open('./calc_count.txt', 'w')
    file.write(str(self.total_calculations))
    file.close()