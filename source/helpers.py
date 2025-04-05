from constants import mines_values

def calculate_emeralds_per_cycle(level, heroes):
  # кол-во шахт, которые будут заполнены
  filled_mines = heroes // 4

  # считаем количество больших шахт
  if (level > 4000):
    big_mines_amount = (level - 3000) // 1000
    last_big_mine = (level // 1000) * 1000
  else:
    big_mines_amount = 0
    last_big_mine = 0

  # количество малых
  small_mines_amount = filled_mines - big_mines_amount

  emeralds = 0
  # сперва считаем изумруды с больших шахт
  if (last_big_mine > 0):
    emeralds += big_mines_amount * 500
    
  emeralds_from_small_mines = 0
  
  counter = 0
  while counter <= small_mines_amount:
    next_mine_level = level - counter * 250
    if (next_mine_level % 1000 == 0):
      # если попали на большую шахту, то просто идем дальше
      counter += 1
    else:
      emeralds_from_small_mines += mines_values[next_mine_level]
      counter += 1

  # за большой круг успеваем проходить 3 маленьких круга 
  emeralds += 3 * emeralds_from_small_mines
  
  return emeralds




  

  

