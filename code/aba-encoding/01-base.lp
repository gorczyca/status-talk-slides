#program base.
rMT(pb1;pb2;pf1;ob1;ob2;of1). % rule move types 
branchMT(pb1;pb2;pf2). % branching (br.) move types 
plr(p;o). % players; proponent (p.) and opponent (o.) 
rS(R,S) :- head(R,S). % rule's statements from rule heads 
rS(R,S) :- body(R,S). % rule's statements from rule bodies 
stS(0,S,P) :- g(S), not contrary(S,S), plr(P). % goal - initial statement 
remBloR(0,R,H,p) :- head(R,H), rS(R,S1), rS(R,S2), contrary(S1,S2). % incons. rules 