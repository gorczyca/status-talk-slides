stS(t,S,P) :- m(_,p,T,R), rMT(T), rS(R,S), plr(P). % new state statement  
stS(t,A,P) :- m(_,p,T,A), not rMT(T), plr(P).
stS(t,S,o) :- m(_,o,T,R), rMT(T), rS(R,S).
stS(t,A,o) :- m(_,o,T,A), not rMT(T).
stR(t,R,H,P) :- m(_,p,T,R), head(R,H), rMT(T), plr(P). % new state rule
stR(t,R,H,o) :- m(_,o,T,R), head(R,H), rMT(T).  

term(t) :-  tt(ta), g(G), comS(_,G,p), comS(_,CC,p) : culCtr(_,CC); 
  not unbloComS(t,DC,o) : defCtr(_,DC).  
end(t,p) :- term(t), not pm(t,o,_,_). % p. won
end(t,o) :- not term(t), not pm(t,p,_,_). % o won