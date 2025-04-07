from enums import CalculatorSteps;

class StepsController:
  current_step = CalculatorSteps.start

  @staticmethod
  def go_to_step(step: CalculatorSteps):
    StepsController.current_step = step
