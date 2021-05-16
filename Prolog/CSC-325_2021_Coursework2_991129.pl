/*----Student: Chuks Ajeh, Student No: 991129 */
/*--------------------Parser-----------------------*/

s(s(NP,VP)) --> np(NUM,subject,Person,Animacy,NP), vp(VP,NUM,Person,Animacy).

/*---------NP RULES------------*/
np(NUM,_,_,Animacy, np(Det,N)) --> det(NUM,Det),nbar(NUM,N,Animacy).
np(NUM,_,_,_,np(Det,N,PP))--> det(NUM,Det), nbar(NUM,N,_), pp(PP).  
np(plural,_,_,_, np(N)) --> nbar(plural,N,_).
np(NUM,SubOb,Person,_,np(Pro)) --> pro(SubOb,NUM,Person,Pro).

/*--------PP RULES------------*/
pp(pp(Prep,NP)) --> prep(Prep),np(_,_,_,_,NP).

/*--------VP RULES------------*/
vp(vp(V,NP),NUM,Person,Animacy)--> tv(NUM,V,Person,Animacy), np(_,object,_,_,NP).
vp(vp(V),NUM,Person,Animacy)--> iv(NUM,V,Person,Animacy).

/*----------NBAR-------------*/
nbar(NUM,nbar(N),Animacy) --> n(NUM,Animacy,N).
nbar(_,nbar(Jp),_) --> jp(Jp).

/*-----------JP RULES---------*/
jp(jp(Adj,Jp)) --> adj(Adj),jp(Jp).
jp(jp(Adj,N)) --> adj(Adj), n(_,_,N).

/*-----General Lexicon Rules---*/
pro(SubOb,NUM,Person,pro(Word)) --> [Word], {lex(Word,pro,NUM,Person,SubOb)}.
adj(adj(Word)) --> [Word], {lex(Word,adj)}.
prep(prep(Word)) --> [Word], {lex(Word,prep)}.
det(NUM, det(Word)) --> [Word], {lex(Word,det,NUM)}.
n(NUM,Animacy, n(Word)) --> [Word], {lex(Word,n,NUM,Animacy)}. 
iv(NUM, v(Word),Person,Animacy)--> [Word], {lex(Word,iv, NUM,Person,Animacy)}. 
tv(NUM, v(Word),Person,Animacy)--> [Word], {lex(Word,tv, NUM,Person,Animacy)}.


/*--------------------Lexicon----------------------*/
/*--------------------pronoun----------------------*/
lex(i,pro,singular,1,subject  ). 
lex(you,pro,singular,2,subject).
lex(the,pro,singular,3,subject).
lex(she,pro,singular,3,subject).
lex(it,pro,singular,3,subject).
lex(we,pro,plural,1,subject).
lex(you,pro,plural,2,subject).
lex(they,pro,plural,3,subject).
lex(me,pro,singular,1,object).
lex(you,pro,singular,2,object).
lex(him,pro,singular,3,object).
lex(her,pro,singular,3,object).
lex(it,pro,singular,3,object).
lex(us,pro,plural,1,object).
lex(you,pro,plural,2,object).
lex(them,pro,plural,3,object).

/*-------------------verb-------------------------*/
lex(know,tv,singular,1,animate).
lex(know,tv,singular,2,animate).
lex(knows,tv,singular,3,animate).
lex(know,tv,plural,_,animate).
lex(see,tv,singular,1,animate).
lex(see,tv,singular,2,animate).
lex(sees,tv,singular,3,animate).
lex(see,tv,plural,_,animate).
lex(hire,tv,singular,1,animate).
lex(hire,tv,singular,2,animate).
lex(hires,tv,singular,3,animate).
lex(hire,tv,plural,_,animate).
lex(fall,iv,singular,1,_).
lex(fall,iv,singular,2,_).
lex(falls,iv,singular,3,_).
lex(fall,iv,plural,_,_).
lex(sleep,iv,singular,1,animate).
lex(sleep,iv,singular,2,animate).
lex(sleeps,iv,singular,3,animate).
lex(sleep,iv,plural,_,animate).


/*----------------determiner-----------------------*/
lex(the,det,_ ).
lex(a,det,singular).
lex(two,det,plural).

/*-------------------noun---------------------------*/
lex(man,n,singular,animate).
lex(woman,n,singular,animate).
lex(apple,n,singular,inanimate).
lex(chair,n,singular,inanimate).
lex(room,n,singular,inanimate).
lex(men,n,plural,animate).
lex(women,n,plural,animate).
lex(apples,n,plural,inanimate).
lex(chairs,n,plural,inanimate).
lex(rooms,n,plural,inanimate).

/*-----------------preposition-------------------*/
lex(on,prep).
lex(in,prep).
lex(under,prep).

/*-----------------adjective---------------------*/
lex(old,adj).
lex(young,adj).
lex(red,adj).
lex(short,adj).
lex(tall,adj).

/*Reasoning!*/
/*
we are given two sentences from which we can derive almost all the rules of the grammar. We can break down these sentences to see the 
strucutre of the lanuage as the parser is creating a parsing tree. The sentences' breakdown can be seen below:

 s(Tree,[she,knows,her],[]).
 Tree = s(np(pro(she)), vp(v(knows), np(pro(her)))).

 s(
     np(
         pro(she)
        ),
      vp(
          v(knows), 
          np(
              pro(her)
            )
        )
    ).

s(Tree, [the, woman, on, two, chairs, in, a, room, sees, two, tall, young, men], []).
Tree = s(np(det(the), nbar(n(woman)), pp(prep(on), np(det(two), nbar(n(chairs)), 
pp(prep(in), np(det(a), nbar(n(room))))))), vp(v(sees), 
(det(two), nbar(jp(adj(tall), jp(adj(young), n(men)))))))


s(
    np(
        det(the), 
        nbar(n(woman)), 
        pp(
            prep(on), 
            np(
                det(two), 
                nbar(n(chairs)), 
                pp(
                    prep(in), 
                    np(
                        det(a), 
                        nbar(n(room))
                    )
                )
            )
        )
        ), 
    vp(
        v(sees), 
        np(
            det(two), 
            nbar(
                jp(
                    adj(tall), 
                    jp(adj(young), n(men))
                )
            )
        )
    )
)
*/
/*
from these two break parse trees we can work backwards to establish the rules of this grammar:
s --> np, vp.
np --> pro
np --> det, nbar, pp.
np --> det, nbar.
np --> nbar.
vp --> tv, np %- for the transitive verb.
vp --> iv %- for the intransitive verb.
pp --> prep, np.
nbar --> n.
nbar --> jp.
jp --> adj, jp.
jp --> adj,n.

This establishes thes rules of the grammar. This rules above show the handling of the non terminals. The lexicon alone
is sufficient to show understanding of the non-terminal --> terminal relationship and would be redundant in this explanation.
but one example is det --> [the]. From this, it is now a case of deriving the parser than can create the parse tree with which 
to see the structure of the grammar.

Test and output:
?- s(Tree, [the,woman,sees,the,apples], []).
Tree = s(np(det(the), nbar(n(woman))), vp(v(sees), np(det(the), nbar(n(apples))))) .

?- s(Tree, [a,woman,knows,him], []).
Tree = s(np(det(a), nbar(n(woman))), vp(v(knows), np(pro(him)))) .

?- s(Tree, [two,woman,hires,a,man], []).
false.

?- s(Tree, [two,women,hire,a,man], []).
Tree = s(np(det(two), nbar(n(women))), vp(v(hire), np(det(a), nbar(n(man))))) .

?- s(Tree, [she,knows,her], []).
Tree = s(np(pro(she)), vp(v(knows), np(pro(her)))) .

?- s(Tree, [she,know,the,man], []).
false.

?- s(Tree, [us,see,the,apple], []).
false.

?- s(Tree, [we,see,the,apple], []).
Tree = s(np(pro(we)), vp(v(see), np(det(the), nbar(n(apple))))) .

?- s(Tree, [i,know,a,short,man], []).
Tree = s(np(pro(i)), vp(v(know), np(det(a), nbar(jp(adj(short), n(man)))))) .

?- s(Tree, [he,hires,they], []).
false.

?- s(Tree, [two,apples,fall], []).
Tree = s(np(det(two), nbar(n(apples))), vp(v(fall))) 

s(Tree, [the,apple,falls], []).
Tree = s(np(det(the), nbar(n(apple))), vp(v(falls)))

?- s(Tree, [the,apples,fall], []).
Tree = s(np(det(the), nbar(n(apples))), vp(v(fall))) 

|    s(Tree, [i,sleep], []).
Tree = s(np(pro(i)), vp(v(sleep))) 

s(Tree, [you,sleep], []).
Tree = s(np(pro(you)), vp(v(sleep)))

 s(Tree, [she,sleeps], []).
Tree = s(np(pro(she)), vp(v(sleeps))).

s(Tree, [he,sleep], []).
false.

 s(Tree, [them,sleep], []).
false.

s(Tree, [a,men,sleep], []).
false.

s(Tree, [the, tall, woman ,sees, the, red], []).
false.

s(Tree, [the, young ,tall, man ,knows ,the ,old ,short, woman], []).
Tree = s(np(det(the), nbar(jp(adj(young), jp(adj(tall), n(man))))), vp(v(knows), np(det(the), nbar(jp(adj(old), jp(adj(short), n(woman))))))) 

s(Tree, [a, man, tall, knows ,the, short, woman], []).
false.

?- s(Tree, [a, man ,on, a, chair, sees ,a ,woman, in ,a ,room], []).
Tree = s(np(det(a), nbar(n(man)), pp(prep(on), np(det(a), nbar(n(chair))))), vp(v(sees), np(det(a), nbar(n(woman)), pp(prep(in), np(det(a), nbar(n(room))))))) .

?- s(Tree, [a, man, on, a ,chair ,sees ,a, woman ,a, room ,in], []).
false.

?- s(Tree, [the ,tall, young, woman, in ,a ,room, on, the ,chair ,in ,a ,room, in, the, room ,sees, the ,red ,apples ,under ,the, chair], []).
Tree = s(np(det(the), nbar(jp(adj(tall), jp(adj(young), n(woman)))), pp(prep(in), np(det(a), nbar(n(room)), pp(prep(on), np(det(the), nbar(n(chair)), pp(prep(in), np(det(a), nbar(n(...)), pp(prep(...), np(..., ...))))))))), vp(v(sees), np(det(the), nbar(jp(adj(red), n(apples))), pp(prep(under), np(det(the), nbar(n(chair))))))) 


------ANIMACY TEST---------

s(Tree, [the, woman, sees, the, apples], []).
Tree = s(np(det(the), nbar(n(woman))), vp(v(sees), np(det(the), nbar(n(apples)))))

?- s(Tree, [a,woman,knows,him], []).
Tree = s(np(det(a), nbar(n(woman))), vp(v(knows), np(pro(him)))) .

?- s(Tree, [the,man,sleeps], []).
Tree = s(np(det(the), nbar(n(man))), vp(v(sleeps))) .

?- s(Tree, [the,room,sleeps], []).
false.

?- s(Tree, [the,apple,sees, the, chair], []).
false.

?- s(Tree, [the,rooms,know, the, man], []).
false.

?- s(Tree, [the,apple,falls], []).
Tree = s(np(det(the), nbar(n(apple))), vp(v(falls))) .

?- s(Tree, [the,man,falls], []).
Tree = s(np(det(the), nbar(n(man))), vp(v(falls))) 

*/

