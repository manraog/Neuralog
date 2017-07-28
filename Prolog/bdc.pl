%%%%%%%%%%%%%%%%%%%% BASE DE CONOCIMIENTO %%%%%%%%%%%%%%%%%%%%%%%%%

:- dynamic(objeto/2), dynamic(tipo/2), dynamic(ubicacion/2), dynamic(estado/2), dynamic(persona/1).

%%%% UBICACION DE LA PERSONA %%%%
persona(sala).


%%%% OBJETOS Y SU SALIDA  %%%%
objeto(focoSala,1). %Pin 15 74HC595
objeto(ventanaSala, 2). %Pin 1
objeto(puertaEntrada, 3). %Pin2

objeto(focoCocina,4). %Pin 3
objeto(puertaCocina, 5). %Pin 4

objeto(focoCuarto,6). %Pin 5
objeto(puertaCuarto, 7). %Pin 6


%%%% OBJETOS Y SU TIPO  %%%%
tipo(focoCuarto,foco).
tipo(focoCocina,foco).
tipo(focoSala,foco).
tipo(puertaCuarto, puerta).
tipo(puertaCocina, puerta).
tipo(puertaEntrada, puerta).
tipo(ventanaSala, ventana).


%%%% OBJETOS Y SU UBICACION  %%%%
ubicacion(focoSala, sala).
ubicacion(ventanaSala, sala).
ubicacion(puertaEntrada, sala).

ubicacion(focoCocina, cocina).
ubicacion(puertaCocina, cocina).

ubicacion(focoCuarto, cuarto).
ubicacion(puertaCuarto, cuarto).



%%%% OBJETOS Y SU ESTADO  %%%%
estado(focoCuarto,apagado).
estado(focoCocina,apagado).
estado(focoSala,encendido).
estado(puertaCuarto,apagado).
estado(puertaCocina,apagado).
estado(puertaEntrada,encendido).
estado(ventanaSala,apagado).
