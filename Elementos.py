"""
Copyright (c) 2024
Luis Angel Gutierrez Pineda

Todos los derechos reservados.
"""
import pygame
import random

class Pelota:
    __color : pygame.Color
    __radio : int
    __pos : pygame.Vector2
    __velocidad : pygame.Vector2
    __posInicial : pygame.Vector2
    __empezado : bool = False
    __rect : pygame.Rect

    def __init__(self, radio: int, pos : pygame.Vector2, color : str) -> None:
        self.__radio = radio 
        self.__color = pygame.Color(color)
        self.__posInicial = pos
        self.__velocidad = pygame.Vector2(300,300)
        self.setPos(pygame.Vector2(self.__posInicial.x -2, self.__posInicial.y-2))



    def setColor(self, nuevoColor : str) -> None:
        self.__color = pygame.Color(nuevoColor)

    def getColor(self) -> pygame.Color:
        return self.__color

    def setRadio(self, nuevoRadio :int) -> None:
        self.__radio = nuevoRadio

    def getRadio(self) -> int:
        return self.__radio
    
    def setPos(self, vector : pygame.Vector2) -> None:
        self.__pos = vector

    def getPos(self) -> pygame.Vector2:
        return self.__pos
    
    def setVelocidad(self, nuevaVel : float) -> None:
        self.__velocidad.x += nuevaVel
        self.__velocidad.y += nuevaVel

    def resetVelocidad(self) -> None:
        self.__velocidad = pygame.Vector2(300,300)

    def getVelocidad(self) -> pygame.Vector2:
        return self.__velocidad
    
    def getPosInicial(self) -> pygame.Vector2:
        return self.__posInicial
    
    def setRect(self, pelotaRect : pygame.Rect) -> None:
        self.__rect = pelotaRect

    def modificarYPosInicial(self, random : int) -> None:
        self.__posInicial.y = random


    direccion : pygame.Vector2 
    def mover(self, displayRect: pygame.Rect, dt: float, player1Rect: pygame.Rect, player2Rect: pygame.Rect) -> None:
        
        if not self.__empezado:
            self.direccion = self.getPosInicial() - self.getPos()
   
        self.direccion.normalize_ip()
        self.__empezado = True
        if self.getPos().y < displayRect.top or self.getPos().y > displayRect.bottom:
            self.direccion.y *= -1
            self.setVelocidad(10)

        if self.getPos().x < displayRect.left or self.getPos().x > displayRect.right:
            numeroRandom = random.randint(displayRect.top, displayRect.bottom)
            self.modificarYPosInicial(numeroRandom)
            self.setPos(self.getPosInicial())
            self.resetVelocidad()
            self.__empezado = False

        if self.__rect.colliderect(player1Rect) or self.__rect.colliderect(player2Rect):
            self.direccion.x *= -1
            self.setVelocidad(20)


        velocidad = self.direccion * self.getVelocidad().x * dt
        self.setPos(self.getPos() + velocidad)

    
class Jugador():
    __color : pygame.Color
    __lado : int
    __pos : pygame.Vector2
    __velocidad : float
    __local : bool
    __rect : pygame.Rect

    def __init__(self, lado: int, local : bool , color : str, displayRect : pygame.Rect ) -> None:
        self.image = pygame.Surface((lado, lado * 3))
        self.__lado = lado 
        self.__color = pygame.Color(color)
        self.image.fill(self.getColor())
        self.__local = local
        if self.__local:
            self.__pos = pygame.Vector2(displayRect.width/8, displayRect.centery)
            
        else:
            self.__pos = pygame.Vector2(displayRect.width * (7/8), displayRect.centery)
        self.__rect = self.image.get_rect(center=(self.__pos.x, self.__pos.y))
        self.__velocidad = 500

        
    def setColor(self, nuevoColor : str) -> None:
        self.__color = pygame.Color(nuevoColor)

    def getColor(self) -> pygame.Color:
        return self.__color

    def setLado(self, nuevoLado :int) -> None:
        self.__lado = nuevoLado

    def getLado(self) -> int:
        return self.__lado
    
    def setPos(self, vector : pygame.Vector2) -> None:
        self.__pos = vector

    def getPos(self) -> pygame.Vector2:
        return self.__pos
    
    def setVelocidad(self, nuevaVel : float) -> None:
        self.__velocidad = nuevaVel

    def getVelocidad(self) -> float:
        return self.__velocidad
    
    def getRect(self) -> pygame.Rect:
        return self.__rect
    

    def mover(self, displayRect : pygame.Rect, dt : float) -> None:
        tecla : pygame.key.ScancodeWrapper = pygame.key.get_pressed()

        if self.__local:
            if tecla[pygame.K_w] and (self.getPos().y - (self.getLado() * 1.5)) > displayRect.top:
                self.__pos.y -= self.__velocidad * dt
                self.__rect = self.image.get_rect(center=(self.__pos.x, self.__pos.y))
            elif (self.getPos().y - (self.getLado() * 1.5)) <= displayRect.top:
                self.setPos(pygame.Vector2(self.getPos().x, displayRect.top + 0.1 + (self.getLado() * 1.5)))
                self.__rect = self.image.get_rect(center=(self.__pos.x, self.__pos.y))

            if tecla[pygame.K_s]and (self.getPos().y + (self.getLado() * 1.5)) < displayRect.bottom:
                self.__pos.y += self.__velocidad * dt
                self.__rect = self.image.get_rect(center=(self.__pos.x, self.__pos.y))
            elif (self.getPos().y + (self.getLado() * 1.5)) >= displayRect.bottom:
                self.setPos(pygame.Vector2(self.getPos().x, displayRect.bottom - 0.1 - (self.getLado() * 1.5)))
                self.__rect = self.image.get_rect(center=(self.__pos.x, self.__pos.y))

        else:
            if tecla[pygame.K_UP] and (self.getPos().y - (self.getLado() * 1.5)) > displayRect.top:
                self.__pos.y -= self.__velocidad * dt
                self.__rect = self.image.get_rect(center=(self.__pos.x, self.__pos.y))
            elif (self.getPos().y - (self.getLado() * 1.5)) <= displayRect.top:
                self.setPos(pygame.Vector2(self.getPos().x, displayRect.top + 0.1 + (self.getLado() * 1.5)))
                self.__rect = self.image.get_rect(center=(self.__pos.x, self.__pos.y))

            if tecla[pygame.K_DOWN] and (self.getPos().y + (self.getLado() * 1.5)) < displayRect.bottom:
                self.__pos.y += self.__velocidad * dt
                self.__rect = self.image.get_rect(center=(self.__pos.x, self.__pos.y))
            elif (self.getPos().y + (self.getLado() * 1.5)) >= displayRect.bottom:
                self.setPos(pygame.Vector2(self.getPos().x, displayRect.bottom - 0.1 - (self.getLado() * 1.5)))
                self.__rect = self.image.get_rect(center=(self.__pos.x, self.__pos.y))