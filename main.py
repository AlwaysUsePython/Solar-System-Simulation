import pygame
import random
import math
import time

pygame.init()

font = pygame.font.Font('freesansbold.ttf', 50)

class Asteroid:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def move(self, planetArray):
        for planet in planetArray:
            distance = math.sqrt((planet.x - self.x)**2 + (planet.y - self.y)**2)
            try:
                xForce = planet.mass*(planet.x - self.x)/distance**2
            except:
                xForce = 0

            try:
                yForce = planet.mass*(planet.y - self.y)/distance**2
            except:
                yForce = 0


            self.dx += xForce
            self.dy += yForce

        distance = math.sqrt((375 - self.x) ** 2 + (375 - self.y) ** 2)
        try:
            xForce =  8 * (375 - self.x) / distance ** 2
        except:
            xForce = 0

        try:
            yForce =  8 * (375 - self.y) / distance ** 2
        except:
            yForce = 0

        self.dx += xForce
        self.dy += yForce

        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, (200, 200, 200), (self.x, self.y), 5)



class Planet:
    def __init__(self, mass, distance, color, angle):
        self.mass = mass
        self.distance = distance
        self.x = 375 + distance
        self.y = 375
        self.angle = angle
        self.color = color

    def move(self):
        self.angle += 10 / (self.distance)
        self.x = 375 + self.distance * math.cos(self.angle)
        self.y = 375 + self.distance * math.sin(self.angle)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.mass*5)

class Simulation:
    def __init__(self):
        self.planets = []
        self.asteroids = []
        self.year = 0

    def addPlanet(self, mass, distance, color, angle):
        self.planets.append(Planet(mass, distance, color, angle))

    def addAsteroid(self, x, y):
        dx = random.random()
        dy = random.random()
        self.asteroids.append(Asteroid(x, y, dx, dy))

    def update(self):
        for planet in self.planets:
            planet.move()
        for asteroid in self.asteroids:
            asteroid.move(self.planets)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 255, 150), (375, 375), 40)
        for planet in self.planets:
            planet.draw(screen)
        for asteroid in self.asteroids:
            asteroid.draw(screen)

        text = str(self.year)
        text = font.render(text, True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (650, 700)
        screen.blit(text, textRect)

    def getAverage(self):
        totalX = 0
        totalY = 0
        numCounted = 0

        for asteroid in self.asteroids:
            if asteroid.x < 750 and asteroid.y < 750 and asteroid.x > 0 and asteroid.y > 0:
                totalX += asteroid.x
                totalY += asteroid.y
                numCounted += 1
        avgX = totalX / numCounted
        avgY = totalY / numCounted
        return [avgX, avgY]

    def drawAverage(self, screen):
        avg = self.getAverage()
        pygame.draw.circle(screen, (255, 0, 0), (avg[0], avg[1]), 20)

    def addYear(self):
        self.year += 1

def simulate():
    screen = pygame.display.set_mode((750, 750))

    simulation: Simulation = Simulation()

    # Mercury
    simulation.addPlanet(0.5, 60, (100, 100, 100), 10)

    # Venus
    simulation.addPlanet(1, 70, (100, 255, 150), 275)

    # Earth
    simulation.addPlanet(1, 90, (100, 150, 255), 190)

    # Mars
    simulation.addPlanet(0.7, 120, (255, 100, 100), 0)

    # Jupiter
    simulation.addPlanet(4, 160, (200, 150, 150), 300)

    # Saturn
    simulation.addPlanet(2, 200, (150, 150, 100), 120)

    # Uranus
    simulation.addPlanet(3, 240, (100, 100, 255), 60)

    # Neptune
    simulation.addPlanet(2, 280, (100, 255, 200), 100)

    # Planet 9?!!?!!! (version 1)
    #simulation.addPlanet(4, 300, (0, 255, 0))

    # Planet 9?!!?!!! (version 2)
    #simulation.addPlanet(6, 350, (0, 255, 0), 90)

    yearAvgs = []

    for i in range(5000):
        simulation.addAsteroid(random.randint(1, 750), random.randint(1, 750))

    running = True
    yearStart = time.time()
    while running:
        start = time.time()
        if start - yearStart >4:
            simulation.addYear()
            yearAvgs.append(simulation.getAverage())
            if len(yearAvgs) == 5:
                return yearAvgs
            yearStart = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.MOUSEBUTTONUP:
                coords = pygame.mouse.get_pos()
                simulation.addAsteroid(coords[0], coords[1])

        simulation.update()
        simulation.draw(screen)
        simulation.drawAverage(screen)

        end = time.time()

        if (0.07 - (end - start) > 0):
            time.sleep(0.07 - (end - start))

        pygame.display.update()

while True:
    print(simulate())
