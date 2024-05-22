"""
Copyright (c) 2024
Luis Angel Gutierrez Pineda

Todos los derechos reservados
"""
import pygame
from Elementos import Pelota , Jugador , Marcador , Tiempo 

class Juego:
    __tamano : tuple[int,int]
    __ancho : int
    __alto : int
    __display : pygame.Surface
    __pelota : Pelota
    __jugador1 : Jugador
    __jugador2 : Jugador
    __corriendo : bool
    __marcador : Marcador
    __clock = pygame.time.Clock()
    __tiempoJuego : Tiempo
    __dt : float = 0.0

    def __init__(self, ancho: int, alto :int, colorJugador1: str, colorJugador2: str, colorPelota: str) -> None:
        self.__ancho = ancho
        self.__alto = alto
        self.__tamano = (self.__ancho, self.__alto)
        self.__display = pygame.display.set_mode(self.__tamano)
        pygame.display.set_caption("Pyng-Pong")
        centro : pygame.Vector2 = pygame.Vector2(self.__display.get_rect().centerx, self.__display.get_rect().centery)
        self.__pelota = Pelota(15, centro ,colorPelota)
        self.__jugador1 = Jugador(30,True,colorJugador1,self.__display.get_rect())
        self.__jugador2 = Jugador(30,False,colorJugador2,self.__display.get_rect())
        self.__marcador = Marcador()
        self.__tiempoJuego = Tiempo()

    def empezar(self):
        self.__corriendo = True
        
        while self.__corriendo:
            if not self.__tiempoJuego.actualizarTiempo():
                self.__corriendo = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__corriendo = False
    
            self.__display.fill("black")
            
            pelotita : pygame.Rect = pygame.draw.circle(self.__display,self.__pelota.getColor(),self.__pelota.getPos(),self.__pelota.getRadio())
            j1 : pygame.Rect = pygame.draw.rect(self.__display,self.__jugador1.getColor(),self.__jugador1.getRect(),self.__jugador1.getLado())
            j2 : pygame.Rect = pygame.draw.rect(self.__display,self.__jugador2.getColor(),self.__jugador2.getRect(),self.__jugador2.getLado())
            self.__pelota.setRect(pelotita)
            
            self.__pelota.mover(self.__display.get_rect(), self.__dt, j1, j2, self.__corriendo, self.__marcador)
            self.__display.blit(self.__marcador.getText(), self.__display.get_rect().center)
            self.__display.blit(self.__tiempoJuego.getText(), self.__display.get_rect().midtop)
            
            self.__jugador1.mover(self.__display.get_rect(),self.__dt, self.__pelota.getRadio() * 2)
            self.__jugador2.mover(self.__display.get_rect(),self.__dt, self.__pelota.getRadio() * 2)

            pygame.display.flip()

            self.__dt = self.__clock.tick(60) / 1000



if __name__ =="__main__":
    pygame.init()
    Juego(1280,720,"white", "white", "white").empezar()
    pygame.quit()