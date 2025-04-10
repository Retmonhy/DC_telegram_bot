from enums import DarkRitualsAmount

# хранит модели игроков(каждая модель рассчета связана с чатом)
class ModelStore:
  model_dict: dict[int, dict] = {}

  @staticmethod
  def add_model(key: int, model: DarkRitualsAmount):
    ModelStore.model_dict[key] = model
  
  @staticmethod
  def get_model_by_id(id: int):
    return ModelStore.model_dict.get(id)
  
  @staticmethod
  def delete_model_by_id(id: int):
    return ModelStore.model_dict.pop(id, None)