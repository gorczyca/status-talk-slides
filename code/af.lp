#program base.
% initialize
m(0,p,G) :- g(G), not att(G,G), arg(G). 

#program updateState(t).
defeat(t,C) :- m(_,p,P), att(P,C). % defeated
pm(t,p,P) :- m(_,o,O), att(P,O), not defeat(_,P), 
  not m(_,p,P), not att(P,P),                   
  not att(P,D1) : m(_,p,D1). % possible p. move
pm(t,o,O) :- m(_,p,P), att(O,P), not defeat(_,O), 
  not m(_,o,O). % possible o. move
end(t,p) :- g(G), m(_,p,G), not pm(t,o,_),     
  defeat(_,O1) : m(_,o,O1). % p. won
end(t,o) :- not pm(t,p,_), m(_,o,O),              
  not defeat(_, O). % opp. won

#program step(t). 
m(t,o,A) :- pm(t-1,o,A). 
{ m(t,p,A) : pm(t-1,p,A) } = 1 :- not pm(t-1,o,_). 
  
#show m/3.
#show end/2.