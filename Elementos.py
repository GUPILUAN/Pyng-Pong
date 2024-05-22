"""
Copyright (c) 2024
Luis Angel Gutierrez Pineda

Todos los derechos reservados.
"""
import pygame
import random

class Marcador:
    __puntosVisita : int = 0
    __puntosLocal : int = 0
    __font : pygame.font.Font 
    __text : pygame.Surface
    def __init__(self) -> None:
        self.__font = pygame.font.Font(None, 72)
        self.renderMarcador()

    def updateMarcador(self, anotoLocal : bool) -> None:
        if anotoLocal:
            self.__puntosLocal += 1
        else:
            self.__puntosVisita += 1
        self.renderMarcador()

    def renderMarcador(self)-> None:
        self.__text = self.__font.render(f"{self.__puntosLocal} - {self.__puntosVisita}", True, (255,255,255))

    def getText(self) -> pygame.Surface:
        return self.__text
    
    def getTextRect(self) -> pygame.Rect:
        return self.__text.get_rect()
    

class Tiempo:
    __tiempoLimite: float
    __tiempoInicio: float
    __font: pygame.font.Font
    __text: pygame.Surface
    __tiempoTranscurrido: float

    def __init__(self, tiempoLimite: float = 180) -> None:

        self.__font = pygame.font.Font(None, 36)
        self.__tiempoLimite = tiempoLimite if tiempoLimite < 3600 and tiempoLimite > 0 else 180
        self.__tiempoInicio = pygame.time.get_ticks()
        self.__tiempoTranscurrido = 0.0
        self.__text = self.__font.render(f"{self.__tiempoTranscurrido:.2f}", True, (255, 255, 255))

    def actualizarTiempo(self) -> bool:
        minutos : str = f"0{int((self.__tiempoLimite-self.__tiempoTranscurrido)/ 60)}"  if int(self.__tiempoLimite-self.__tiempoTranscurrido) / 60 < 10 else f"{int((self.__tiempoLimite-self.__tiempoTranscurrido) / 60)}"
        segundos : str = f"0{int(self.__tiempoLimite-self.__tiempoTranscurrido) % 60}" if int(self.__tiempoLimite-self.__tiempoTranscurrido) % 60 < 10 else f"{int(self.__tiempoLimite-self.__tiempoTranscurrido) % 60}"
        self.__tiempoTranscurrido = (pygame.time.get_ticks() - self.__tiempoInicio) / 1000
        self.__text = self.__font.render(f"{minutos}:{segundos}", True, (255, 255, 255))
        if self.__tiempoTranscurrido >= self.__tiempoLimite:
            return False
        return True

    def getText(self) -> pygame.Surface:
        return self.__text

    def getTextRect(self) -> pygame.Rect:
        return self.__text.get_rect()

class Pelota:
    __color : pygame.Color
    __radio : int
    __pos : pygame.Vector2
    __velocidad : pygame.Vector2
    __posInicial : pygame.Vector2
    __empezado : bool = False
    __rect : pygame.Rect
    __direccion : pygame.Vector2 

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

    def mover(self, displayRect: pygame.Rect, dt: float, player1Rect: pygame.Rect, 
              player2Rect: pygame.Rect, empezado : bool, marcador: Marcador) -> None:
        
        if not self.__empezado:
            self.__direccion = self.getPosInicial() - self.__pos
   
        self.__direccion.normalize_ip()
        self.__empezado = empezado

        if (self.__pos.y - self.__radio) < displayRect.top :
            self.setPos(pygame.Vector2(self.__pos.x, displayRect.top + self.__radio))
            self.__direccion.y *= -1
            self.setVelocidad(10)
        elif(self.__pos.y + self.__radio) > displayRect.bottom:
            self.setPos(pygame.Vector2(self.__pos.x, displayRect.bottom - self.__radio))
            self.__direccion.y *= -1
            self.setVelocidad(10)

        if self.__pos.x < displayRect.left or self.__pos.x > displayRect.right:
            marcador.updateMarcador(self.__pos.x > displayRect.right)
            numeroRandom = random.randint(displayRect.top, displayRect.bottom)
            self.modificarYPosInicial(numeroRandom)
            self.setPos(self.getPosInicial())
            self.resetVelocidad()
            self.__empezado = False
    
        #Detecta colision con el jugador de la izquierda
        if self.__rect.colliderect(player1Rect):
            metido = player1Rect.right - self.__rect.left
            self.setPos(pygame.Vector2(self.__pos.x + metido, self.__pos.y))
            self.__direccion.x *= -1
            self.setVelocidad(20)
        #Detecta colision con el jugador de la derecha
        elif self.__rect.colliderect(player2Rect):
            metido =  self.__rect.right - player2Rect.left
            self.setPos(pygame.Vector2(self.__pos.x - metido, self.__pos.y))
            self.__direccion.x *= -1
            self.setVelocidad(20)


        velocidad = self.__direccion * self.getVelocidad().x * dt
        self.setPos(self.__pos + velocidad)

    
class Jugador:
    __color : pygame.Color
    __ancho : int
    __alto : int
    __pos : pygame.Vector2
    __velocidad : float
    __local : bool
    __rect : pygame.Rect

    def __init__(self, lado: int, local : bool , color : str, displayRect : pygame.Rect ) -> None:
        self.__ancho = lado 
        self.__alto = lado * 9
        self.image = pygame.Surface((self.__ancho,self.__alto))
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
        self.__ancho = nuevoLado

    def getLado(self) -> int:
        return self.__ancho
    
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
    

    def mover(self, displayRect : pygame.Rect, dt : float, pelotaSize : int) -> None:
        tecla : pygame.key.ScancodeWrapper = pygame.key.get_pressed()

        if self.__local:
            if tecla[pygame.K_w] and not tecla[pygame.K_s] and (self.__pos.y - self.__alto/2 - pelotaSize) > displayRect.top:
                self.__pos.y -= self.__velocidad * dt
                self.__rect = self.image.get_rect(center=(self.__pos.x, self.__pos.y))
            elif tecla[pygame.K_s] and not tecla[pygame.K_w] and (self.__pos.y + self.__alto/2 + pelotaSize) < displayRect.bottom:
                self.__pos.y += self.__velocidad * dt
                self.__rect = self.image.get_rect(center=(self.__pos.x, self.__pos.y))
        else:
            if tecla[pygame.K_UP] and not tecla[pygame.K_DOWN]   and (self.__pos.y - self.__alto/2 - pelotaSize) > displayRect.top:
                self.__pos.y -= self.__velocidad * dt
                self.__rect = self.image.get_rect(center=(self.__pos.x, self.__pos.y))
            elif tecla[pygame.K_DOWN] and not tecla[pygame.K_UP]  and (self.__pos.y + self.__alto/2 + pelotaSize) < displayRect.bottom:
                self.__pos.y += self.__velocidad * dt
                self.__rect = self.image.get_rect(center=(self.__pos.x, self.__pos.y))
