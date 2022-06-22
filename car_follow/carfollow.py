import pygame as pg

RESOLUTION = WIDTH, HEIGHT = 1080, 720
FPS = 60
BG_COL = pg.Color("white")


class Car:
    def __init__(self, pos, angle):
        self.MAX_TURN_RATE = 2
        self.MAX_VEL = 2
        self.DECEL_FAC = 50  # increasing makes car slow down more before reaching mouse
        self.STOP_DISTANCE = 20

        self.pos = pg.Vector2(pos)
        self.angle = angle

        self.vel = 0

        self.image = pg.image.load("car.jpg")
        self.image = pg.transform.scale(self.image, (80, 36))
        self.image.set_colorkey((246, 246, 246))

    @property
    def rect(self):
        return pg.Rect(self.pos, self.image.get_size())

    @property
    def facing_vector(self):
        vec = pg.Vector2()
        vec.from_polar((1, self.angle))
        return vec

    def update(self, angle_to, distance_to):
        if distance_to > self.STOP_DISTANCE:
            if angle_to > 180:
                angle_to -= 360
            if angle_to < -180:
                angle_to += 360

            if angle_to < 0:
                self.angle += max(-self.MAX_TURN_RATE, angle_to)
            else:
                self.angle += min(self.MAX_TURN_RATE, angle_to)

            move_vec = pg.Vector2()
            move_vec.from_polar((min(distance_to / self.DECEL_FAC, self.MAX_VEL), self.angle))
            self.pos += move_vec

    def render(self, display):
        image = pg.transform.rotate(self.image, -self.angle)
        size = pg.Vector2(image.get_size())
        display.blit(image, self.pos - size / 2)

    def debug_render(self, display):
        facing = pg.Vector2()
        facing.from_polar((50, self.angle))
        draw_vector(display, pg.Color("green"), self.pos, facing)


def draw_vector(display, color, pos, vec):
    pg.draw.line(display, color, pos, pos + vec)


def run():
    pg.init()

    screen = pg.display.set_mode(RESOLUTION)
    clock = pg.time.Clock()
    running = True

    car = Car((WIDTH / 2, HEIGHT / 2), 50)

    while running:
        clock.tick(FPS)
        # === EVENTS ===
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        mouse_pos = pg.Vector2(pg.mouse.get_pos())

        # === UPDATE ===
        mouse_vector = mouse_pos - car.pos
        angle_between = car.facing_vector.angle_to(mouse_vector)
        distance_between = mouse_vector.magnitude()
        car.update(angle_between, distance_between)

        # === RENDER ===
        screen.fill(BG_COL)
        car.render(screen)
        # debug render
        car.debug_render(screen)
        draw_vector(screen, pg.Color("red"), car.pos, mouse_pos - car.pos)
        pg.display.flip()


if __name__ == "__main__":
    run()
