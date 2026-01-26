# solar_sandbox.py
import math, random, sys
import pygame

pygame.init()
WIDTH, HEIGHT = 1100, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar Sandbox - Create / Destroy")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 16)
BIG = pygame.font.SysFont("consolas", 28)

# Colors
BG = (6, 10, 25)
SUN_COLOR = (255, 200, 0)
WHITE = (230, 230, 230)
GRAY = (120, 120, 130)
RED = (230, 80, 60)
GREEN = (60, 200, 120)
YELLOW = (240, 220, 100)
TRAIL_ALPHA = 70

CENTER = (WIDTH // 2, HEIGHT // 2)

# physics-ish constants (not realistic units)
G = 6.674e-1  # tune for orbit speeds visually


def draw_text(surface, text, pos, color=WHITE, font=FONT):
    surface.blit(font.render(text, True, color), pos)


class Button:
    def __init__(self, rect, text, color=(50, 50, 60)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.hover = False

    def draw(self, surf):
        c = tuple(min(255, x + 30) for x in self.color) if self.hover else self.color
        pygame.draw.rect(surf, c, self.rect, border_radius=6)
        pygame.draw.rect(surf, (40, 40, 50), self.rect, 2, border_radius=6)
        txt = FONT.render(self.text, True, WHITE)
        # Center text horizontally and vertically within the button
        txt_x = self.rect.x + (self.rect.width - txt.get_width()) // 2
        txt_y = self.rect.y + (self.rect.height - txt.get_height()) // 2
        # Ensure text doesn't go outside button bounds
        txt_x = max(self.rect.x + 4, min(txt_x, self.rect.x + self.rect.width - txt.get_width() - 4))
        surf.blit(txt, (txt_x, txt_y))

    def handle_event(self, ev):
        if ev.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(ev.pos)
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.rect.collidepoint(ev.pos):
                return True
        return False


class Slider:
    def __init__(self, x, y, w, label, min_v, max_v, val):
        self.rect = pygame.Rect(x, y, w, 18)
        self.label = label
        self.min_v = min_v
        self.max_v = max_v
        self.value = val
        self.handle_x = self.x_from_val(val)
        self.dragging = False

    def x_from_val(self, v):
        return int(self.rect.x + (v - self.min_v) / (self.max_v - self.min_v) * self.rect.width)

    def val_from_x(self, x):
        frac = min(1, max(0, (x - self.rect.x) / self.rect.width))
        return self.min_v + frac * (self.max_v - self.min_v)

    def draw(self, surf):
        # label - ensure it fits in the allocated space
        label_text = f"{self.label}: {self.value:.2f}"
        label_surface = FONT.render(label_text, True, WHITE)
        # If text is too wide, truncate it
        max_width = 130  # Leave some margin
        if label_surface.get_width() > max_width:
            # Try with fewer decimal places
            label_text = f"{self.label}: {self.value:.1f}"
            label_surface = FONT.render(label_text, True, WHITE)
            if label_surface.get_width() > max_width:
                # If still too wide, truncate the label
                label_text = f"{self.label[:8]}: {self.value:.1f}"
                label_surface = FONT.render(label_text, True, WHITE)
        
        draw_text(surf, label_text, (self.rect.x - 140, self.rect.y - 2))
        # bar
        pygame.draw.rect(surf, (70, 70, 80), self.rect, border_radius=6)
        pos = (self.x_from_val(self.value), self.rect.y + self.rect.height // 2)
        pygame.draw.circle(surf, (200, 200, 200), pos, 8)

    def handle_event(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.rect.collidepoint(ev.pos) or pygame.Rect(self.x_from_val(self.value) - 10, self.rect.y, 20, self.rect.height).collidepoint(ev.pos):
                self.dragging = True
        elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
            self.dragging = False
        elif ev.type == pygame.MOUSEMOTION and self.dragging:
            x = ev.pos[0]
            self.value = self.val_from_x(x)


class Planet:
    def __init__(self, distance, size, color, angular_speed, initial_angle=None):
        self.distance = distance
        self.size = size
        self.color = color
        self.angular_speed = angular_speed  # radians per second
        self.angle = initial_angle if initial_angle is not None else random.random() * 2 * math.pi
        self.trail = []
        self.max_trail = 160

    def update(self, dt):
        self.angle = (self.angle + self.angular_speed * dt) % (2 * math.pi)
        x = CENTER[0] + math.cos(self.angle) * self.distance
        y = CENTER[1] + math.sin(self.angle) * self.distance
        self.trail.append((x, y))
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)

    def pos(self):
        return (CENTER[0] + math.cos(self.angle) * self.distance,
                CENTER[1] + math.sin(self.angle) * self.distance)

    def draw(self, surf):
        # draw trail
        if len(self.trail) > 1:
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            alpha_step = int(TRAIL_ALPHA / max(1, len(self.trail)))
            for i in range(1, len(self.trail)):
                p1 = self.trail[i - 1]
                p2 = self.trail[i]
                pygame.draw.line(s, (self.color[0], self.color[1], self.color[2], alpha_step), p1, p2, max(1, int(self.size // 3)))
            surf.blit(s, (0, 0))
        x, y = map(int, self.pos())
        pygame.draw.circle(surf, self.color, (x, y), int(self.size))
        # outline
        pygame.draw.circle(surf, (30, 30, 30), (x, y), int(self.size), 1)

    def is_clicked(self, mpos):
        x, y = self.pos()
        dx = mpos[0] - x
        dy = mpos[1] - y
        return dx * dx + dy * dy <= (self.size ** 2)


class ExplosionParticle:
    def __init__(self, pos):
        self.x, self.y = pos
        angle = random.random() * math.tau
        speed = random.uniform(20, 200)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.uniform(0.6, 1.4)
        self.age = 0
        self.size = random.uniform(2, 6)
        self.color = (255, random.randint(100, 220), random.randint(50, 120))

    def update(self, dt):
        self.age += dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        # simple damping
        self.vx *= (1 - 2 * dt)
        self.vy *= (1 - 2 * dt)

    def draw(self, surf):
        if self.age < self.life:
            alpha = max(0, 255 * (1 - self.age / self.life))
            s = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(s, (self.color[0], self.color[1], self.color[2], int(alpha)), (int(self.size), int(self.size)), int(self.size))
            surf.blit(s, (self.x - self.size, self.y - self.size))


# UI elements
btn_create = Button((20, 20, 150, 38), "Create Planet")
btn_destroy = Button((190, 20, 150, 38), "Destroy Mode: OFF")
btn_pause = Button((360, 20, 120, 38), "Pause: OFF")
info_rect = pygame.Rect(20, 70, 360, 160)

# sliders for create modal
slider_size = Slider(240, 220, 260, "Size", 3, 30, 10)
slider_dist = Slider(240, 260, 260, "Distance", 60, min(WIDTH // 2 - 40, 420), 150)
slider_speed = Slider(240, 300, 260, "Speed", -2.5, 2.5, 0.9)

show_create_modal = False
destroy_mode = False
paused = False

planets = []
explosion_particles = []

# prepopulate some planets
def add_planet(distance, size, speed, color=None):
    if color is None:
        color = (random.randint(40, 240), random.randint(40, 240), random.randint(40, 240))
    # convert 'speed' slider into angular speed: speed influences angular velocity visually
    angular_speed = speed * 0.8  # tuning factor
    p = Planet(distance, size, color, angular_speed)
    planets.append(p)

# add some default planets
add_planet(80, 12, 1.7, (120, 180, 255))
add_planet(140, 9, 1.15, (200, 120, 80))
add_planet(210, 14, 0.85, (160, 240, 160))


def explode_at(pos, intensity=18):
    for _ in range(intensity * 4):
        explosion_particles.append(ExplosionParticle(pos))


def draw_ui(surf):
    # left info panel
    pygame.draw.rect(surf, (18, 22, 30), info_rect, border_radius=8)
    pygame.draw.rect(surf, (40, 40, 50), info_rect, 2, border_radius=8)
    draw_text(surf, "Solar Sandbox", (info_rect.x + 8, info_rect.y + 8), YELLOW, BIG)
    draw_text(surf, f"Planets: {len(planets)}", (info_rect.x + 8, info_rect.y + 50))
    
    # Split long text into multiple lines to fit in the box
    shortcuts_text = "Shortcuts: C = quick create, D = toggle destroy, P = pause"
    shortcuts_surface = FONT.render(shortcuts_text, True, WHITE)
    if shortcuts_surface.get_width() > info_rect.width - 16:  # Leave margin
        # Split into two lines
        draw_text(surf, "Shortcuts: C = quick create, D = toggle", (info_rect.x + 8, info_rect.y + 80))
        draw_text(surf, "destroy, P = pause", (info_rect.x + 8, info_rect.y + 100))
    else:
        draw_text(surf, shortcuts_text, (info_rect.x + 8, info_rect.y + 80))
    
    create_text = "Click Create -> adjust sliders -> Add Planet"
    create_surface = FONT.render(create_text, True, WHITE)
    if create_surface.get_width() > info_rect.width - 16:
        # Split into two lines
        draw_text(surf, "Click Create -> adjust sliders ->", (info_rect.x + 8, info_rect.y + 110))
        draw_text(surf, "Add Planet", (info_rect.x + 8, info_rect.y + 130))
    else:
        draw_text(surf, create_text, (info_rect.x + 8, info_rect.y + 110))


def create_modal(surf):
    # modal background
    modal = pygame.Rect(200, 180, 520, 180)
    pygame.draw.rect(surf, (18, 18, 26), modal, border_radius=10)
    pygame.draw.rect(surf, (40, 40, 50), modal, 2, border_radius=10)
    draw_text(surf, "Create Planet", (modal.x + 12, modal.y + 8), YELLOW, BIG)
    # sliders
    slider_size.draw(surf)
    slider_dist.draw(surf)
    slider_speed.draw(surf)
    # Buttons - ensure they have enough space for text
    add_btn = Button((modal.x + 360, modal.y + 120, 130, 34), "Add Planet", color=(30, 140, 80))
    cancel_btn = Button((modal.x + 200, modal.y + 120, 130, 34), "Cancel", color=(120, 40, 50))
    add_btn.draw(surf)
    cancel_btn.draw(surf)
    return add_btn, cancel_btn


def update(dt):
    if not paused:
        for p in planets:
            p.update(dt)
    # update explosion particles
    for ep in explosion_particles[:]:
        ep.update(dt)
        if ep.age >= ep.life:
            explosion_particles.remove(ep)


def draw(surf):
    surf.fill(BG)
    # sun
    pygame.draw.circle(surf, SUN_COLOR, CENTER, 36)
    pygame.draw.circle(surf, (255, 240, 200), CENTER, 14)
    # planets
    for p in planets:
        p.draw(surf)
    # explosion particles
    for ep in explosion_particles:
        ep.draw(surf)
    # UI
    btn_create.draw(surf)
    btn_destroy.draw(surf)
    btn_pause.draw(surf)
    draw_ui(surf)
    if show_create_modal:
        add_btn, cancel_btn = create_modal(surf)
        return add_btn, cancel_btn
    return None, None


def quick_random_planet():
    dist = random.randint(70, min(WIDTH // 2 - 60, 420))
    size = random.randint(6, 20)
    speed = random.uniform(-2.0, 2.0)
    add_planet(dist, size, speed)


# Main loop
running = True
while running:
    dt = CLOCK.tick(60) / 1000.0
    add_btn = cancel_btn = None

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_c:
                quick_random_planet()
            if ev.key == pygame.K_d:
                destroy_mode = not destroy_mode
                btn_destroy.text = f"Destroy Mode: {'ON' if destroy_mode else 'OFF'}"
            if ev.key == pygame.K_p:
                paused = not paused
                btn_pause.text = f"Pause: {'ON' if paused else 'OFF'}"

        # UI events
        if btn_create.handle_event(ev):
            show_create_modal = True
        if btn_destroy.handle_event(ev):
            destroy_mode = not destroy_mode
            btn_destroy.text = f"Destroy Mode: {'ON' if destroy_mode else 'OFF'}"
        if btn_pause.handle_event(ev):
            paused = not paused
            btn_pause.text = f"Pause: {'ON' if paused else 'OFF'}"

        # modal events
        if show_create_modal:
            slider_size.handle_event(ev)
            slider_dist.handle_event(ev)
            slider_speed.handle_event(ev)
            # we need to capture clicks for the modal buttons returned in draw
            # We'll detect by manual rect check after drawing step.

        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and not show_create_modal:
            mpos = ev.pos
            if destroy_mode:
                # check planets for hit (reverse order so topmost is removed)
                for p in reversed(planets):
                    if p.is_clicked(mpos):
                        explode_at(p.pos(), intensity=int(max(8, p.size // 1.5)))
                        try:
                            planets.remove(p)
                        except ValueError:
                            pass
                        break

    # draw once to get modal button rects
    add_btn, cancel_btn = draw(SCREEN)
    pygame.display.flip()

    # handle add/cancel button clicks if modal visible
    if show_create_modal and add_btn and cancel_btn:
        for ev in pygame.event.get([pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]):
            # pass these to slider handlers as well
            slider_size.handle_event(ev)
            slider_dist.handle_event(ev)
            slider_speed.handle_event(ev)
            if add_btn.handle_event(ev):
                # create planet with slider values
                sz = max(2, slider_size.value)
                dist = max(40, slider_dist.value)
                sp = slider_speed.value
                # Add the planet and close modal
                add_planet(dist, sz, sp)
                show_create_modal = False
            if cancel_btn.handle_event(ev):
                show_create_modal = False

    # update logic
    update(dt)

    # redraw
    draw(SCREEN)
    # draw current mode indicator
    mode_text = f"Mode: {'DESTROY' if destroy_mode else 'CREATE/EDIT' if show_create_modal else 'NORMAL'}"
    draw_text(SCREEN, mode_text, (20, HEIGHT - 28), WHITE)
    pygame.display.flip()

pygame.quit()
sys.exit()
