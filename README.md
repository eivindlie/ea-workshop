# Workshop om evolusjonære algoritmer

Dette er en workshop som forhåpentligvis vil gi et innblikk i hva evolusjonære algoritmer er, hvordan de fungerer, og litt om hva slags problemer man kan løse med slike algoritmer. Workshopen er delt inn i tre deler av økende vanskelighetsgrad, og i hver del skal man løse et problem ved hjelp av en eller flere evolusjonære algoritmer.

## 1. Travelling Salesman Problem

[Travelling Salesman Problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem) er et mye brukt eksempelproblem, og egner seg godt til å løses med evolusjonære algoritmer. Problemet er [NP-hardt](https://en.wikipedia.org/wiki/NP-hardness), og det er derfor upraktisk å lage en deterministisk algoritme for å løse problemet. Derimot kan det ofte løses effektivt med en meta-heuristisk algoritme som for eksempel en genetisk algoritme.

Traveling Salesman Problem går ut på at en handelsmann skal besøke et gitt sett av byer. Han skal besøke alle byene, og må ende opp i samme by som han starter. Gitt disse forutsetningene ønsker han å planlegge en kortest mulig reisevei mellom byene:

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/GLPK_solution_of_a_travelling_salesman_problem.svg/1920px-GLPK_solution_of_a_travelling_salesman_problem.svg.png" width="400" style="background: white">
