from clingo import Control, Number as N
                   Function as F
def main(instance, base_code, encoding):
 ctl = Control()
 ctl.load(instance)
 ctl.load(encoding)
 ctl.add("base", [], base_code)
 ctl.ground([("base", ())])
 t = 0
 while True: 
  ctl.ground([("updateState",[N(t)])]) 
  p_win = (F("end",[N(t),F("p")]),True) 
  res = ctl.solve(assumptions=[p_win], 
                  on_model=print) 
  if res.satisfiable:
    return True
  o_win = (F("end",[N(t),F("o")]),False) 
  res = ctl.solve(assumptions=[o_win])  
  if res.unsatisfiable: 
    return False
  t += 1 
  ctl.ground([("step",[N(t)])])