"""
Copyright (c) 2024
Luis Angel Gutierrez Pineda

Todos los derechos reservados.
"""
import pygame
from Elementos import Pelota as pelota, Jugador as jugador

class Juego:
    __tamano : tuple[int,int]
    __ancho : int
    __alto : int
    __display : pygame.Surface
    __pelota : pelota
    __jugador1 : jugador
    __jugador2 : jugador
    __corriendo : bool
    __clock = pygame.time.Clock()
    __dt : float = 0.0

    def __init__(self, ancho: int, alto :int, colorJugador1: str, colorJugador2: str, colorPelota: str) -> None:
        self.__ancho = ancho
        self.__alto = alto
        self.__tamano = (self.__ancho, self.__alto)
        self.__display = pygame.display.set_mode(self.__tamano)
        centro : pygame.Vector2 = pygame.Vector2(self.__display.get_rect().centerx, self.__display.get_rect().centery)
        self.__pelota = pelota(40, centro ,colorPelota)
        self.__jugador1 = jugador(90,True,colorJugador1,self.__display.get_rect())
        self.__jugador2 = jugador(90,False,colorJugador2,self.__display.get_rect())

    def empezar(self):
        self.__corriendo = True
        
        while self.__corriendo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__corriendo = False

            self.__display.fill("black")
            
            pelotita : pygame.Rect = pygame.draw.circle(self.__display,self.__pelota.getColor(),self.__pelota.getPos(),self.__pelota.getRadio())
            j1 : pygame.Rect = pygame.draw.rect(self.__display,self.__jugador1.getColor(),self.__jugador1.getRect(),self.__jugador1.getLado())
            j2 : pygame.Rect = pygame.draw.rect(self.__display,self.__jugador2.getColor(),self.__jugador2.getRect(),self.__jugador2.getLado())
            self.__pelota.setRect(pelotita)

            self.__pelota.mover(self.__display.get_rect(), self.__dt, j1, j2)

            self.__jugador1.mover(self.__display.get_rect(),self.__dt)
            self.__jugador2.mover(self.__display.get_rect(),self.__dt)

            pygame.display.flip()

            self.__dt = self.__clock.tick(60) / 1000


pygame.init()
Juego(1280,720,"red", "blue", "green").empezar()
pygame.quit()