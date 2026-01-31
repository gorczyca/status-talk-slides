#program step(t). 
m(t,P,T,X) :- pm(t-1,P,T,X), not branchMT(T), t > 0. 
{ m(t,P,T,X) : pm(t-1,P,T,X) } = 1 :- t > 0, branchMT(T) : pm(t-1,_,T,_). 
#show m/4.