:- consult('bdc.pl').

%%%%%%%%%%%%%%%%%%%%%% PREDICADOS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%% Lista pines de objetos encendidos %%%%
lista_pines_encendidos(Pin):-
			estado(Objeto, encendido),
			objeto(Objeto, Pin).


%%%% Objetos segun estado Y ubicacion %%%%
lista_objetos(Objeto, Ubicacion, Estado):-
			ubicacion(ObjetoEnUbicacion, Ubicacion),
			estado(ObjetoConEstado,Estado),
			(ObjetoEnUbicacion = ObjetoConEstado -> Objeto = ObjetoConEstado).
			
%%%% Cambia objeto %%%%
cambiar(Objeto, Tipo, NuevoArgumento):- 
			functor(Hecho, Tipo, 2),
			arg(1, Hecho, Objeto),
			retract(Hecho),
			functor(NuevoHecho, Tipo, 2),
			arg(1, NuevoHecho, Objeto),
			arg(2, NuevoHecho, NuevoArgumento),
			assertz(NuevoHecho).
			
%%%% Cambia de estado al objeto %%%%
switch(Objeto):-
			estado(Objeto, Estado),
			(Estado = apagado -> cambiar(Objeto, estado, encendido); cambiar(Objeto, estado, apagado)).

%%%% Mueve de lugar objeto %%%%
mover(Objeto, Destino, Pin):- 
			cambiar(Objeto, ubicacion, Destino),
			cambiar(Objeto, objeto, Pin).
			
%%%% Elimina objeto %%%%
eliminar(_, []).

eliminar(Objeto, [H|T]):-
			functor(Hecho, H, 2),
			arg(1, Hecho, Objeto),
			retract(Hecho),
			eliminar(Objeto, T).
			
eliminar(Objeto):- 
			eliminar(Objeto, [objeto, tipo, ubicacion, estado]).

%%%% Crea nuevo Objeto %%%%
nuevo(_, [], []).

nuevo(Objeto, [Hfact | Tfacts], [Harg | Targs]):-
			functor(Hecho, Hfact, 2),
			arg(1, Hecho, Objeto),
			arg(2, Hecho, Harg),
			assertz(Hecho),
			nuevo(Objeto, Tfacts, Targs).
			
nuevo(Objeto, ListaArgumentos):-
			nuevo(Objeto, [objeto, tipo, ubicacion, estado], ListaArgumentos).

%%%% Muve persona de lugar %%%%
mueve_persona( Lugar ):-
			retract(persona(_)),
			assertz(persona(Lugar)).

%%%% Guardar %%%%
guardar:- 
			tell('bdc.pl'),
			listing(objeto),
			listing(tipo),
			listing(ubicacion),
			listing(estado),
			told.
