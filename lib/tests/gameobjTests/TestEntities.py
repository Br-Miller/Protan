"""
Test module for module entities
"""


import os, sys
import unittest
if __name__ == '__main__': sys.path.append( os.path.abspath('./../../') )
from gameobj import entities


class test_Action(unittest.TestCase):
  """Test class for Action"""
  def test_applyEffect(self):
    #Initialise objects
    actionAttack = entities._Ability('DebugAction', 
                                {}, 
                                {'mp':2}, 
                                {'damage': 'physical'}, 
                                {'damage': lambda e: e.strn})
    actionHeal = entities._Ability('DebugAction', 
                                {}, 
                                {'mp':2}, 
                                {'heal': 'physical'}, 
                                {'heal': lambda e: e.strn})

    #Test Damage
    caster = entities.TurnFightEntity({'hp': 10, 'mp': 10, 'str': 5})
    target = entities.TurnFightEntity({'hp': 10, 'mp': 10, 'str': 5})
    actionAttack.applyEffect(caster, [target])
    self.assertEqual(caster.mp, 8)
    self.assertEqual(target.hp, 5)

    #Test Heal
    caster = entities.TurnFightEntity({'hp': 10, 'mp': 10, 'str': 5})
    target = entities.TurnFightEntity({'hp': 10, 'mp': 10, 'str': 5})
    target.hp = 5
    actionHeal.applyEffect(caster, [target])
    self.assertEqual(caster.mp, 8)
    self.assertEqual(target.hp, 10)

  def test_effect(self):
    #Initialise objects
    actionAttack = entities._Ability('DebugAction', 
                                {}, 
                                {'mp':2}, 
                                {'damage': 'physical'}, 
                                {'damage': lambda e: e.strn})
    actionHeal = entities._Ability('DebugAction', 
                                {}, 
                                {'mp':2}, 
                                {'heal': 'physical'}, 
                                {'heal': lambda e: e.strn})
    #test damage
    caster = entities.TurnFightEntity({'hp': 10, 'mp': 10, 'str': 5})
    target = entities.TurnFightEntity({'hp': 10, 'mp': 10, 'str': 5})
    actionAttack.effect(caster, [target], 'damage', lambda e: e.strn)
    self.assertEqual(target.hp, 5)
    actionAttack.effect(caster, [target], 'heal', lambda e: e.strn)
    self.assertEqual(target.hp, 10)


def starting_test():
  tb_line = 70 * '-'
  midline = '|' + (27 * ' ') + ('Starting Test') + (28 * ' ') + '|'
  print '\n'.join([tb_line, midline,tb_line])


Action_tests = unittest.TestLoader().loadTestsFromTestCase(test_Action)
alltests = unittest.TestSuite([Action_tests])


if __name__ == '__main__':
  starting_test()
  unittest.TextTestRunner(verbosity=2).run(alltests)