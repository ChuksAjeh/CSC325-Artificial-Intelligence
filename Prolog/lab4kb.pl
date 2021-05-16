byCar(auckland,hamilton).
byCar(hamilton,raglan).
byCar(valmont,saarbruecken).
byCar(valmont,metz).
byTrain(metz,frankfurt).
byTrain(saarbruecken,frankfurt).
byTrain(metz,paris).
byTrain(saarbruecken,paris).
byPlane(frankfurt,bangkok).
byPlane(frankfurt,singapore).
byPlane(paris,losAngeles).
byPlane(bangkok,auckland).
byPlane(losAngeles,auckland).

%- Part 1
travel(X,Y):- byCar(X,Y);byPlane(X,Y);byTrain(X,Y).

travel(X,Y):- byCar(X,Z), travel(Z,Y).
travel(X,Y):- byTrain(X,Z), travel(Z,Y).
travel(X,Y):- byPlane(X,Z), travel(Z,Y).

/*
?- travel(valmont,Y).
Y = saarbruecken ;
Y = metz ;
Y = frankfurt ;
Y = paris ;
Y = bangkok ;
Y = singapore ;
Y = auckland ;
Y = hamilton ;
Y = raglan ;
Y = losAngeles ;
Y = auckland ;
Y = hamilton ;
Y = raglan ;
Y = frankfurt ;
Y = paris ;
Y = bangkok ;
Y = singapore ;
Y = auckland ;
Y = hamilton ;
Y = raglan ;
Y = losAngeles ;
*/

/*
It repeats cities
*/

%- Part 2 

travel(X,Y, route(X,Y)):- byCar(X,Y).
travel(X,Y, route(X,Y)):- byPlane(X,Y).
travel(X,Y, route(X,Y)):- byTrain(X,Y).

travel(X,Y, route(X,Z,G)) :-
  byCar(X,Z),
  travel(Z,Y,G);
  byPlane(X,Z),
  travel(Z,Y,G);
  byTrain(X,Z),
  travel(Z,Y,G).

%- travel(valmont,paris,route(valmont,metz,route(metz,paris))). returns true 

/*
X = route(valmont, saarbruecken, route(saarbruecken, paris, route(paris, losAngeles))) ;
X = route(valmont, metz, route(metz, paris, route(paris, losAngeles))) ;
*/

/*
-------------------------------------------------------------------------------------------
Part 3
*/  

directTrain(saarbruecken,dudweiler).
directTrain(forbach,saarbruecken).
directTrain(freyming,forbach).
directTrain(stAvold,freyming).
directTrain(fahlquemont,stAvold).
directTrain(metz,fahlquemont).
directTrain(nancy,metz).

directTrain(A,B):- directTrain(B,A),!.

route(B,B, Rl, L):- reverse(Rl,L).

route(A,B, Rl,L):- directTrain(A,C), not(member(C,Rl)),route(C,B,[C|Rl],L).

route(A,B,L):- route(A,B,[A],L).



/*
L = [forbach, freyming, stAvold, fahlquemont, metz] 
*/

%- Part 4:

/*
  Step 1): Hypothesis C; that is does C follow from the KB?
  Step 2): Check memory - C is not in MO.
  Step 3): Find a rule (top down) with C as head rule - rule 1.
  Step 3): Find the conditions of rule 1 and set them as the new hypotheses - A and B
  Step 4): Check in Memory, A is not in MO. Conditions for rule 1 not yet met.
  Step 6): Find a rule for A as head - rule 2.
  Step 7): Find the conditions of rule 2 and set them as the new hypothesis. - \+X.
  Step 8): Check in memory - X not in MO.
  Step 9): Find a rule with X as head - rule 3.
  Step 10): Check in memory for D and F. They are both in memory which means conditions for rule 3 are met.
  Step 12): Got to rule 2. Although X succeeds \+X fails so we do not add X to memory.
  Step 13): \+X does not hold. X is not in Memory but there is a rule with X as head. So rule 2 conditions are not met.
  Step 14): Ergo rule 1 conditions are not met. So C cannot be added to memory.
  Step 15): Conclusion: C cannot follow from the KB.
*/