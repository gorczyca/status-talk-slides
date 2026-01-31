graph(m).
graph((A,l),m) :- arg(A). 
node(A,(A,l)) :- arg(A).
edge((A,B),m) :- att(A,B).

attr(node,A,fillcolor,"green") :- m(_,p,A). 
attr(node,A,fillcolor,"yellow") :- m(_,o,A).
attr(graph,(A,l),label,T) :- m(T,_,A).

ldefeat(Tm,A) :- defeat(Tm,A), not m(_,_,A), 
  Tm = #min { T : defeat(T,A) }.
attr(graph,(A,l),label,Tm) :- ldefeat(Tm,A).
attr(node,A,fillcolor,"red") :- ldefeat(_,A).

lpm(Tm,P,A) :- pm(Tm,P,A), not m(_,_,A), not defeat(_,A), 
  Tm = #max { T : pm(T,_,A) }.
attr(graph,(A,l),label,T) :- lpm(T,_,A).
attr(node,A,fillcolor,"lightblue") :- lpm(_,_,A).