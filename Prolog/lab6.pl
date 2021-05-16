/*
s --> foo,bar,wiggle.
foo --> [choo].
foo --> foo,foo.
bar --> mar,zar.
mar --> me,my. 
me --> [i].
my --> [am].
zar --> blar,car.
blar --> [a].
car --> [train].
wiggle --> [toot].
wiggle --> wiggle,wiggle. 
*/

/*
s(A, D) :- foo(A, B),bar(B, C),wiggle(C, D).

foo([choo | A], A).

foo(A, C) :- foo(A, B), foo(B, C).

bar(A, C) :- mar(A, B), zar(B, C).

mar(A, C) :- me(A, B), my(B, C).

me([i | A], A).

my([am | A], A).

zar(A, C) :- blar(A, B),car(B, C).

blar([a | A], A).

car([train | A], A).

wiggle([toot | A], A).

wiggle(A, C) :- wiggle(A, B), wiggle(B, C).
*/

/*
s(X,[]).
X = [choo, i, am, a, train, toot] ;
X = [choo, i, am, a, train, toot, toot] ;
X = [choo, i, am, a, train, toot, toot, toot] ;
*/

/*Task 2: ------------------------------------------------------------------------- */

/*
s --> np,vp.
np --> det,n.
vp --> v,np.
det --> [the].
det --> [a].
n --> [woman].
n--> [man].
v --> [hires].


s(s(NP,VP)) --> np(NP),vp(VP).
np(np(Det,N)) --> det(Det),n(N).
vp(vp(V, NP )) --> v(V), np(NP).
det(det(the)) --> [the].
det(det(a)) --> [a].
n(n(woman)) --> [woman].
n(n(man)) --> [man].
v(v(hires)) --> [hires].
*/


/*
?- s(Tree,[a,man,hires,a, woman],[]).
Tree = s(np(det(a), n(man)), vp(v(hires), np(det(a), n(woman)))).
*/

/*
?- s(Tree,[a,woman,hires,the, woman],[]).
Tree = s(np(det(a), n(woman)), vp(v(hires), np(det(the), n(woman)))).
*/

/*Task 3 ---------------------------------------------------------------------------*/


s(s(NP,VP)) --> np(NUM, NP), vp(NUM,VP).
np( NUM, np(Det,N))--> det(NUM,Det), n(NUM, N).  
np(plural,np(N))--> n(plural,N).
vp(NUM,vp(V,NP))--> v(NUM,V), np(_, NP).
det(single, det(a)) --> [a].
det(plural, det(two)) --> [two].
det(_,det(the)) --> [the].
n(single,n(woman)) --> [woman].
n(single,n(man)) --> [man].
n(plural,n(women)) --> [women].
n(plural,n(men)) --> [men].
v(single,v(hires))--> [hires].
v(plural,v(hire)) --> [hire].



/*Task 4 ------------------------------------------------------------------------------*/



/*
s(s(NP,VP)) --> np(NUM, NP), vp(NUM,VP).

np(NUM, np(Det,N))--> det(NUM,Det), n(NUM, N).  
np(plural,np(N))--> n(plural,N). 

vp(NUM,vp(V))--> iv(NUM,V).
vp(NUM,vp(V,NP))--> tv(NUM,V), np(_, NP).


det(NUM, det(Word)) --> [Word], {lex(Word,det, NUM)}.

n(NUM, n(Word)) --> [Word], {lex(Word,n, NUM)}.

iv(NUM, v(Word))--> [Word], {lex(Word,iv, NUM)}.
tv(NUM, v(Word))--> [Word], {lex(Word,tv, NUM)}.

lex(a, det, single).
lex(two, det, plural).
lex(the, det, _).

lex(man, n, single). 
lex(woman, n, single). 
lex(men, n, plural). 
lex(women, n, plural). 

lex(falls, iv, single).
lex(fall, iv, _).

lex(hires, tv, single).
lex(hire, tv, plural).
*/

