/*% See Bratko pages 353-356.
% 
% The code below is for the expert system shell. This is the shell that you need to use
% to write your own expert system; that is, your task will be to write the rules
% which use the shell. Get the shell running in Prolog and test using Bratko’s
% examples.
%
% Interaction with user and why and how 
% Operators for easy to read rules. */

:-op(800, fx, if).
:-op(700, xfx, then).
:-op(300, xfy, or).
:-op(200, xfy, and).
:-op(800, xfx, <=).


/*%%%%
% Adam Wyner
% Added the dynamic fact predicate as there were otherwise errors.
% p. 351 in Bratko book.*/

:-dynamic( fact/1).

% is_true( P, Proof): Proof is a proof that P is true

is_true( P, Proof)  :-
    explore( P, Proof, []).


/* explore( P, Proof, Trace): */
/*Proof is an explanation for P, Trace is a chain of rules between P's ancestor goals*/

explore( P, P, _)  :-
    fact(P).                      
    
/* P is a fact*/ 

explore(P1 and P2, Proof1 and Proof2, Trace)  :-!,
explore(P1, Proof1, Trace),
explore(P2, Proof2, Trace).

explore( P1 or P2, Proof, Trace)  :-!,
(
    explore(P1, Proof, Trace);
    explore(P2, Proof, Trace)
).

explore(P, P <= CondProof, Trace)  :-
if Cond then P, explore( Cond, CondProof, [ if Cond then P | Trace]).
/*  A rule relevant to P */ 


explore(P, Proof, Trace)  :-
askable(P),    
\+ fact(P),    
\+ already_asked(P),        
ask_user(P, Proof, Trace).


ask_user( P, Proof, Trace)  :-
nl, write( 'Is it true:'), write( P), write(?), nl, write( 'Please answer yes, no, or why'), nl,
read( Answer),
process_answer( Answer, P, Proof, Trace).   

% P may be asked of user
/* P not already known fact*/
/* P not yetasked of user*/
/* Process user's answer */

process_answer( yes, P, P  <= was_told, _)  :-  
asserta(fact(P)),
asserta(already_asked( P)).

% User told P is true


process_answer(no, P, _, _)  :-
asserta(already_asked( P)),  
fail.  
/*  % Make sure not to ask again about P*/ 
/* % User told P is not true */

process_answer(why, P, Proof, Trace)  :-  
display_rule_chain( Trace, 0), nl,
ask_user(P, Proof, Trace).     

% Ask about P again
% User requested why-explanation


display_rule_chain([], _).

display_rule_chain( [if C then P | Rules], Indent)  :-
nl, write( 'To explore whether '), write( P), write(' is true, using rule:'),
nl, write( if C then P),
NextIndent is Indent + 2,
display_rule_chain(  Rules, NextIndent).

:-dynamic already_asked/1.

/*leak_in_bathroom :- hall_wet, kitchen_dry.
problem_in_kitchen :- hall_wet,  bathroom_dry.
no_water_from_outside :- window_closed; no_rain.
leak_in_kitchen :- problem_in_kitchen, no_water_from_outside.*/

/*if hall_wet and kitchen_dry then leak_in_bathroom.
if hall_wet and bathroom_dry then problem_in_kitchen.
if window_closed or no_rain then no_water_from_outside.
if problem_in_kitchen and no_water_from_outside then leak_in_kitchen.*/
/*
askable(hall_wet).
askable(bathroom_dry).
askable(window_closed).
askable(no_rain).
*/

/*------------------------------------Lab Test---------------------------------------*/
askable(have_no_sypmtoms).
askable(self_isolated_for_two_weeks).
askable(went_to_a_large_party).
askable(person_at_party_tested_positive).
askable(not_vaccinated).
askable(previously_had_covid).
askable(infected).
askable(have_sypmtoms).

if have_no_sypmtoms and self_isolated_for_two_weeks then healthy.
if went_to_a_large_party and person_at_party_tested_positive then may_be_infected.
if not_vaccinated or not_previously_had_covid then may_not_be_immune.
if may_not_be_immune and may_be_infected and have_sypmtoms then get_tested.

/*we cannot use negation because the facts 
we are asking the user are not in the KB and if you use negation it will return true alsways*/

/*

?- is_true(healthy,HOW).

Is it true:have_no_sypmtoms?
Please answer yes, no, or why
|: yes.

Is it true:self_isolated_for_two_weeks?
Please answer yes, no, or why
|: no.

false.

is_true(healthy,HOW). 
HOW =  (healthy<=have_no_sypmtoms and self_isolated_for_two_weeks) .



is_true(healthy,WHY).

Is it true:have_no_sypmtoms?
Please answer yes, no, or why
|: yes.

Is it true:self_isolated_for_two_weeks?
Please answer yes, no, or why
|: yes.

WHY =  (healthy<=(have_no_sypmtoms<=was_told)and(self_isolated_for_two_weeks<=was_told)) .


*/

/*





?- is_true(get_tested,HOW).

Is it true:not_vaccinated?
Please answer yes, no, or why
|: yes.

Is it true:went_to_a_large_party?
Please answer yes, no, or why
|: yes.

Is it true:person_at_party_tested_positive?
Please answer yes, no, or why
|: yes.

Is it true:have_sypmtoms?
Please answer yes, no, or why
|: yes.

HOW =  (get_tested<=(may_not_be_immune<=(not_vaccinated<=was_told))
and(may_be_infected<=(went_to_a_large_party<=was_told)and(person_at_party_tested_positive<=was_told))and(have_sypmtoms<=was_told)) .


?- is_true(get_tested,WHY).

Is it true:not_vaccinated?
Please answer yes, no, or why
|: yes.

Is it true:went_to_a_large_party?
Please answer yes, no, or why
|: no.

false.
*/