import sys
from typing import Optional

import blackjack.model.blackjack
from blackjack.model.blackjack import Blackjack


class UIConsola:

    def __init__(self):
        self.blackjack: Blackjack = Blackjack()
        self.opciones = {
            "1": self.iniciar_nuevo_juego,
            "2": self.salir
        }

    @staticmethod
    def mostrar_menu():
        titulo = "BLACKJACK"
        print(f"\n{titulo:_^30}")
        print("1. Iniciar nuevo juego")
        print("2. Salir")
        print(f"{'_':_^30}")

    def registrar_usuario(self):
        print("\nHola, bienvenid@ al juego de blackjack")
        nombre: str = input("¿Cuál es tu nombre?: ")
        self.blackjack.registrar_usuario(nombre)

    def ejecutar_app(self):
        self.registrar_usuario()
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ")
            accion = self.opciones.get(opcion)
            if accion:
                accion()
            else:
                print(f"{opcion} no es una opción válida")

    def iniciar_nuevo_juego(self):
        apuesta: int = self.pedir_apuesta()
        self.blackjack.iniciar_juego(apuesta)
        self.mostrar_manos(self.blackjack.cupier.mano, self.blackjack.jugador.mano)

        if not self.blackjack.jugador.mano.es_blackjack():
            self.hacer_jugada_del_jugador()
        else:
            print(f"FELICITACIONES, LOGRASTE BLACKJACK. HAS GANADO EL JUEGO")

    def hacer_jugada_del_jugador(self):
        while not self.blackjack.jugador_perdio():
            respuesta = input("¿Quiere otra carta? s(si), n(no): ")
            if respuesta == "s":
                self.blackjack.repartir_carta_a_jugador()
                self.mostrar_manos(self.blackjack.cupier.mano, self.blackjack.jugador.mano)
            elif respuesta == "n":
                break

        if self.blackjack.jugador_perdio():
            print("\nHAS PERDIDO EL JUEGO")
        else:
            self.ejecutar_turno_de_la_casa()
    #REQUISITO #4
    def ejecutar_turno_de_la_casa(self):
        print("\nTURNO DE LA CASA")
        #Metodo para destapar la mano
        Blackjack.destapar_mano_de_la_casa()
        #Si la casa tiene blackjack, gana
        if blackjack.Mano.es_blackjack():
            print("\nLA CASA GANO")
        #Se termina el juego
            self.finalizar_juego()
        #Mientras que no sea blackjack
        while not blackjack.Mano.es_blackjack:
        #Si la casa no puede pedir acaba el juego
            if not self.blackjack.casa_puede_pedir():
                self.finalizar_juego()
            else:
        #Si la casa puede pedir
                while self.blackjack.casa_puede_pedir():
        #Se reparte carta a la casa y se calcula el valor
                    self.blackjack.repartir_carta_a_la_casa()
                    self.Mano.calcular_valor()
        #Si no puede pedir o el jugador gana se acaba el juego
                    if not Blackjack.casa_puede_pedir():
                        self.finalizar_juego()
                    elif Blackjack.jugador_gano():
                        self.finalizar_juego()
    #REQUISITO #5
    def finalizar_juego(self):
        if Blackjack.jugador_gano():
            print("\n EL JUGADOR GANO!")
        elif Blackjack.casa_gano() or Blackjack.jugador_perdio():
            print("\n EL JUGADOR PERDIO!")
            blackjack.Jugador.fichas -= Blackjack.apuesta_actual
        elif blackjack.Casa.mano == blackjack.Jugador.mano:
            Blackjack.hay_empate()
            print("\n HAY EMPATE!")

    def pedir_apuesta(self):
        apuesta: int = int(input("¿Cuál es su apuesta?: "))
        while not self.blackjack.jugador.puede_apostar(apuesta) or apuesta <= 0:
            print(f"ADVERTENCIA: No tiene suficientes fichas para apostar {apuesta} o su apuesta fue de 0")
            print("Ingrese una nueva apuesta.")
            apuesta = int(input("¿Cuál es su apuesta?: "))
        return apuesta

    @staticmethod
    def mostrar_manos(mano_casa, mano_jugador):
        print(f"\n{'MANO DE LA CASA':<15}\n{str(mano_casa):<15}")
        print(f"{'VALOR: ' + str(mano_casa.calcular_valor()):<15}")
        print(f"\n{'TU MANO':<15}\n{str(mano_jugador):<15}")
        print(f"{'VALOR: ' + str(mano_jugador.calcular_valor()):<15}")

        if blackjack.Jugador.tiene_fichas():
            print("\n¿Qué desea hacer?")
            print("1. Jugar de nuevo")
            print("2. Salir")
            opcion = input("Ingrese una opción: ")
            while opcion != "1" and opcion != "2":
                opcion = input("Ingrese una opción válida (1 o 2): ")
            if opcion == "1":
                Blackjack.iniciar_nuevo_juego()
            else:
                Blackjack.finalizar_juego()

    @staticmethod
    def salir():
        print("\nGRACIAS POR JUGAR BLACKJACK. VUELVA PRONTO")
        sys.exit(0)
