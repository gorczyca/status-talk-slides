comS(t,S,p) :- def(_,D).  % complete statement  
comS(t,H,p) :- stR(_,R,H,p), comS(t,S,p) : body(R, S).  
unbloComS(t,S,o) :- stS(_,S,o), assumption(S), not cul(_,S). % unblocked complete
unbloComS(t,H,o) :- stS(_,H,o), not stBloS(t,H,o), unbloComR(t,_,H,o).
unbloComR(t,R,H,o) :-  stR(_,R,H,o), not stBloR(t,R,H,o), unbloComS(t,B,o) : body(R, B).
unbloSupSS(t,S,o) :- stS(_,S,o), contrary(D,S), def(t,D), not stBloS(t,S,o).
unbloSupSS(t,S,o) :- stS(_,S,o), not stBloS(t,S,o), unbloSupSR(t,R,_,o), body(R, S).
unbloSupSR(t,R,H,o) :- stR(_,R,H,o), not stBloR(t,R,H,o), unbloSupSS(t,H,o).
culCan(t,C) :- assumption(C), unbloSupSS(t,C,o). % culprit candidate  

pm(t,p,pb1,R) :- remR(t,R,H,p), not remBloR(_,R,H,p), unexpS(t,H,p). % possible moves 
pm(t,p,pb2,R) :- remR(t,R,H,p), not remBloR(_,R,H,p), culCan(t,C), contrary(C, H), 
  not stS(_,H,p), not contrary(D, H) : def(_,D). 
pm(t,p,pf1,R) :- remR(t,R,H,p), not remBloR(_,R,H,p), comS(t,B,p) : body(R, B). 
pm(t,p,pf2,A) :- culCan(t,C), contrary(C,A), assumption(A), not stS(_,A,p), 
  not contrary(A,A), not cul(_,A),  not contrary(D,A) : def(_,D). 
pm(t,o,ob1,R) :- remR(t,R,H,o), not remBloR(_,R,H,o), unbloSupSS(t,H,o). 
pm(t,o,ob2,R) :- remR(t,R,H,o), not remBloR(_,R,H,o), contrary(D, H), def(_,D). 
pm(t,o,of1,R) :- remR(t,R,H,o), not remBloR(_,R,H,o), unbloComS(t,B,o) : body(R, B).
pm(t,o,of2,A) :- contrary(D,A), def(_,D), assumption(A), not stS(_,A,o). 