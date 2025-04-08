from constants import mines
from math import *

def calculate_emeralds_per_cycle(level, heroes, mode):
  # кол-во шахт, которые будут заполнены
  filled_mines = heroes // 4

  # считаем количество больших шахт
  if (level >= 4000):
    big_mines_amount = (level - 3000) // 1000
  else:
    big_mines_amount = 0

  # количество малых
  small_mines_amount = filled_mines - big_mines_amount

  emeralds = 0
  
  # сперва считаем изумруды с больших шахт
  if (big_mines_amount > 0):
    emeralds += big_mines_amount * 500
    
  
  counter = 1
  next_mine_level = level
  emeralds_from_small_mines = 0
  while counter <= small_mines_amount:
    # тут посчитаем сколько изумрудов получим за малый круг тт(64 часа)
    next_mine = mines[next_mine_level]
    is_small_mine = next_mine['nominal'] < 500
    if (is_small_mine):
      emeralds_from_small_mines += next_mine['emeralds_per_hour'] * 64
      counter += 1


    # определяем следующую шахту   
    if (next_mine_level > 1000):
      next_mine_level = next_mine_level - 250
    elif (next_mine_level <= 1000 and next_mine_level >= 700):
      next_mine_level = next_mine_level - 100
    elif (next_mine_level == 600):
      next_mine_level = 450
    elif (next_mine_level <= 450 and next_mine_level >= 350):
      next_mine_level = next_mine_level - 100
    elif (next_mine_level == 250):
      next_mine_level = 175
    elif (next_mine_level == 175):
      next_mine_level = 125
    elif (next_mine_level == 125):
      next_mine_level = 35
    elif (next_mine_level == 35):
      next_mine_level = 0

  # за большой круг(192 часа) успеваем проходить 3 маленьких круга 
  emeralds += mode * emeralds_from_small_mines
  
  return ceil(emeralds)




  

  

