#program updateState(t).
% add another option to perform "PF2" move
pm(t,p,pf2,A) :- at(ds), assumption(A), not cul(_,A), not stS(_,A,p), 
  not contrary(A,A), not contrary(D,A) : def(_,D).
% define: remaining assumptions - neither defences, nor culprits
remA(t,A) :- tt(ts), assumption(A), not def(_,A), not cul(_,A).
% modify termination criteria:  require no assumption be remaining
term(t) :- tt(ts), g(G), comS(_,G,p), comS(_,CC,p) : culCtr(_,CC);
  not unbloComS(t,DC,o) : defCtr(_,DC); not remA(t,A) : assumption(A). 