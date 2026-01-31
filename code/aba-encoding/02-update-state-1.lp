#program updateState(t).
def(t,D) :- stS(_,D,p), assumption(D). % defence 
cul(t,C) :- stS(_,S,p), contrary(C,S). % culprit 
defCtr(t,DC) :- def(_,D), contrary(D,DC). % defence contrary 
culCtr(t,CC) :- cul(_,C), contrary(C,CC). % culprit contrary 

remR(t,R,H,P) :- not stR(_,R,H,P), head(R,H), plr(P). % remaining player's rule  
remBloR(t,R,H,P) :- remR(t,R,H,P), body(R,B), cul(_,B), plr(P). % block. rem. P. rules       
remBloR(t,R,H,p) :- remR(t,R,H,p), rS(R,S), defCtr(_,S). % blocked remaining p.'s rule              

unexpS(t,H,p) :- stS(_,H,p), not stR(_,_,H,p). % unexpanded statement  
stExpS(t,H,o) :- stS(_,H,o), remBloR(_,R,H,o) : remR(t,R,H,o). % fully expanded
stBloS(t,S,o) :- stS(_,S,o), cul(_,S). % state blocked statement  
stBloS(t,S,o) :- stExpS(t,S,o), not assumption(S), stBloR(t,R,S,o) : stR(_,R,S,o).  
stBloR(t,R,H,o) :- stR(_,R,H,o), body(R,B), stBloS(t,B,o). % state blocked rule  
