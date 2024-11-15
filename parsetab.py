
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'EQUALS ID NEWLINE PAINT STRINGprogram : program command\n               | commandcommand : PAINT expressioncommand : ID EQUALS expressionexpression : IDexpression : STRING'
    
_lr_action_items = {'PAINT':([0,1,2,5,6,7,8,10,],[3,3,-2,-1,-3,-5,-6,-4,]),'ID':([0,1,2,3,5,6,7,8,9,10,],[4,4,-2,7,-1,-3,-5,-6,7,-4,]),'$end':([1,2,5,6,7,8,10,],[0,-2,-1,-3,-5,-6,-4,]),'STRING':([3,9,],[8,8,]),'EQUALS':([4,],[9,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'command':([0,1,],[2,5,]),'expression':([3,9,],[6,10,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> program command','program',2,'p_program','yacc.py',9),
  ('program -> command','program',1,'p_program','yacc.py',10),
  ('command -> PAINT expression','command',2,'p_paint','yacc.py',23),
  ('command -> ID EQUALS expression','command',3,'p_assign','yacc.py',37),
  ('expression -> ID','expression',1,'p_load','yacc.py',46),
  ('expression -> STRING','expression',1,'p_expression_string','yacc.py',50),
]
