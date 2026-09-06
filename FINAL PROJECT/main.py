import pygame
import random
import math
import sys

# initialize game

pygame.init()
pygame.mixer.init()

# first, scaling the window

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Museum")

clock = pygame.time.Clock()

# loading colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (230, 200, 100)

# loading the font i chose from google fonts

font = pygame.font.Font(
    "assets/font/syne.ttf",
    36
)

notice_font = pygame.font.Font(
    "assets/font/syne.ttf",
    18
)

button_font = pygame.font.Font(
    "assets/font/syne.ttf",
    24
)

puzzle_font = pygame.font.Font(
    "assets/font/syne.ttf",
    26
)

pool_font = pygame.font.Font(
    "assets/font/syne.ttf",
    18
)

# loading my artwork

intro_image = pygame.image.load(
    "assets/images/introduction/intro.png"
).convert()
intro_image = pygame.transform.smoothscale(intro_image, (WIDTH, HEIGHT))

gallery_image = pygame.image.load(
    "assets/images/museum/the_gallery.png"
).convert()
gallery_image = pygame.transform.smoothscale(gallery_image, (WIDTH, HEIGHT))

forest_image = pygame.image.load(
    "assets/images/forest/forest.png"
).convert()
forest_image = pygame.transform.smoothscale(forest_image, (WIDTH, HEIGHT))

lovers_image = pygame.image.load(
    "assets/images/thelovers/the_lovers.png"
).convert()
lovers_image = pygame.transform.smoothscale(lovers_image, (WIDTH, HEIGHT))

sky_image = pygame.image.load(
    "assets/images/sky/cloudy_sky.png"
).convert()
sky_image = pygame.transform.smoothscale(sky_image, (WIDTH, HEIGHT))

stars_bg_image = pygame.image.load(
    "assets/images/nightsky/infinity.png"
).convert()
stars_bg_image = pygame.transform.smoothscale(stars_bg_image, (WIDTH, HEIGHT))

exit_bg_image = pygame.image.load(
    "assets/images/exit/exit.png"
).convert()
exit_bg_image = pygame.transform.smoothscale(exit_bg_image, (WIDTH, HEIGHT))


def autocrop_surface(surface, bg_color=(255, 255, 255), tolerance=30, stride=2):

    width, height = surface.get_size()

    min_x, min_y = width, height
    max_x, max_y = 0, 0
    found = False

    for x in range(0, width, stride):
        for y in range(0, height, stride):

            r, g, b, a = surface.get_at((x, y))

            if a == 0:
                continue

            if (
                abs(r - bg_color[0]) <= tolerance
                and abs(g - bg_color[1]) <= tolerance
                and abs(b - bg_color[2]) <= tolerance
            ):
                continue

            found = True

            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

    if not found:
        return surface

    pad = stride * 2

    min_x = max(0, min_x - pad)
    min_y = max(0, min_y - pad)
    max_x = min(width - 1, max_x + pad)
    max_y = min(height - 1, max_y + pad)

    crop_rect = pygame.Rect(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)

    return surface.subsurface(crop_rect).copy()


# music
# note: the music is entirely loaded from pixabay and is license free, i will add the sources in my description in git

CURRENT_TRACK = None


def play_music(path, loop=-1):


    global CURRENT_TRACK

    if CURRENT_TRACK == path:
        return

    pygame.mixer.music.stop()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(loop)

    CURRENT_TRACK = path


play_music("assets/music/intro/intro.mp3")

MAIN_THEME_PATH = "assets/music/main theme/main.mp3"
# note: the main theme plays in the main gallery and the exit screen, so basically everywhere that's not a mini-game.

# i also chose sound effects from pixabay, however, differently from the music, they are only relevant on the exit screen

exit_lose_sound = pygame.mixer.Sound("assets/sounds/lose/lose.mp3")
exit_click_sound = pygame.mixer.Sound("assets/sounds/click/click.mp3")
exit_door_sound = pygame.mixer.Sound("assets/sounds/door/door.mp3")
exit_win_sound = pygame.mixer.Sound("assets/sounds/win/win.mp3")

exit_sound_channel = pygame.mixer.Channel(1)

# game state

game_state = "INTRO"

collected_letters = {
    "WORD_PUZZLE": False,
    "FOREST": False,
    "CLOUD": False,
    "STARS": False,
}

# okay so i decided on the exit password "tech" (pun intended), so now it's time to assign each game its own reward letter.
# note for myself: change it so the player doesn't have to unscramble the letters themselves anymore

TARGET_WORD = "TECH"

GAME_LETTER_REWARDS = {
    "WORD_PUZZLE": "C",
    "FOREST": "E",
    "CLOUD": "T",
    "STARS": "H",
}


def letters_earned():
    return sum(1 for earned in collected_letters.values() if earned)


def all_letters_collected():
    return all(collected_letters.values())


def get_unlocked_letters():

    unlocked = set()

    for game_name, done in collected_letters.items():

        if done and GAME_LETTER_REWARDS.get(game_name):
            unlocked.add(GAME_LETTER_REWARDS[game_name])

    return unlocked


def get_password_display():

    unlocked = get_unlocked_letters()

    return " ".join(ch if ch in unlocked else "_" for ch in TARGET_WORD)


# finallyyy time to become the narrator in the intro hehe
# note: button function works now!!

intro_steps = [
    {"text": "Welcome to the museum."},
    {"text": "We rarely get any visitors...", "button": "Leave"},
    {"text": "Oh no, there appears to have been a misunderstanding!"},
    {"text": "No, you cannot leave until you have earned the exit password.", "button": "How do I exit?"},
    {"text": "You must enter four paintings and play games or solve riddles."},
    {"text": "Only once you complete each game, you will receive one reward letter."},
    {"text": "Once you have gained all four letters, you will be able to unlock the door."},
    {"text": "Are you ready to play?", "button": "Play"},
]

current_step = 0

displayed_text = ""
typing_index = 0

typing_speed = 0.045
last_typing_time = 0

# note: ask test players if the typing is too fast and adjust if necessary

def current_step_data():
    return intro_steps[current_step]


def current_step_text():
    return current_step_data()["text"]


def step_finished_typing():
    return typing_index >= len(current_step_text())


def advance_intro_step():

    global current_step, displayed_text, typing_index

    current_step += 1

    if current_step >= len(intro_steps):
        current_step = len(intro_steps) - 1

    displayed_text = ""
    typing_index = 0


# okay it looks too boring, quick new addition: dust particles

dust_particles = []

for i in range(80):

    particle = {
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "size": random.randint(1, 3),
        "speed_x": random.uniform(-0.15, 0.15),
        "speed_y": random.uniform(-0.3, 0.3),
        "alpha": random.randint(40, 120)
    }

    dust_particles.append(particle)


def update_dust():

    for particle in dust_particles:

        particle["x"] += particle["speed_x"]
        particle["y"] += particle["speed_y"]

        if particle["x"] < 0:
            particle["x"] = WIDTH

        if particle["x"] > WIDTH:
            particle["x"] = 0

        if particle["y"] < 0:
            particle["y"] = HEIGHT

        if particle["y"] > HEIGHT:
            particle["y"] = 0


def draw_dust():

    dust_surface = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    for particle in dust_particles:

        pygame.draw.circle(
            dust_surface,
            (255, 255, 255, particle["alpha"]),
            (int(particle["x"]), int(particle["y"])),
            particle["size"]
        )

    screen.blit(dust_surface, (0, 0))
# update: way better

# feedback adjustment: need to fix buttons to make them more visible
def wrap_text(text, render_font, max_width):

    words = text.split(" ")
    lines = []
    current = ""

    for word in words:

        test_line = current + (" " if current else "") + word

        if render_font.size(test_line)[0] <= max_width:
            current = test_line
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def draw_intro_text(text, y):

    if not text:
        return

    max_text_width = WIDTH - 300

    lines = wrap_text(text, font, max_text_width)

    line_height = font.get_linesize()
    total_height = line_height * len(lines)
    start_y = y - total_height // 2 + line_height // 2

    max_line_width = max(font.size(line)[0] for line in lines)

    panel_padding_x = 40
    panel_padding_y = 24

    panel_rect = pygame.Rect(
        0, 0,
        max_line_width + panel_padding_x * 2,
        total_height + panel_padding_y * 2
    )
    panel_rect.center = (WIDTH // 2, y)

    panel_surface = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
    panel_surface.fill((0, 0, 0, 150))
    screen.blit(panel_surface, panel_rect)

    outline_offsets = [(-2, -2), (-2, 2), (2, -2), (2, 2), (0, -2), (0, 2), (-2, 0), (2, 0)]

    for i, line in enumerate(lines):

        line_y = start_y + i * line_height

        for ox, oy in outline_offsets:
            outline_text = font.render(line, True, BLACK)
            outline_rect = outline_text.get_rect(center=(WIDTH // 2 + ox, line_y + oy))
            screen.blit(outline_text, outline_rect)

        rendered_text = font.render(line, True, WHITE)
        text_rect = rendered_text.get_rect(center=(WIDTH // 2, line_y))
        screen.blit(rendered_text, text_rect)


def draw_continue_notice():

    text = notice_font.render(
        "Press any key to continue",
        True,
        WHITE
    )

    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 35))

    screen.blit(text, text_rect)


# same thing for text backdrop

def draw_text_with_backdrop(rendered_text, y, padding_x=20, padding_y=10, bg_alpha=200):

    text_rect = rendered_text.get_rect(center=(WIDTH // 2, y))

    panel_rect = pygame.Rect(
        0, 0,
        text_rect.width + padding_x * 2,
        text_rect.height + padding_y * 2
    )
    panel_rect.center = text_rect.center

    panel_surface = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
    panel_surface.fill((0, 0, 0, bg_alpha))
    screen.blit(panel_surface, panel_rect)

    screen.blit(rendered_text, text_rect)


# button drawing

def get_button_rect(label, y):


    rendered_text = button_font.render(label, True, WHITE)

    padding_x = 30
    padding_y = 16

    rect = pygame.Rect(
        0, 0,
        rendered_text.get_width() + padding_x * 2,
        rendered_text.get_height() + padding_y * 2
    )

    rect.center = (WIDTH // 2, y)

    return rect


def draw_button(text, rect):

    button_surface = pygame.Surface(
        (rect.width, rect.height),
        pygame.SRCALPHA
    )

    button_surface.fill((0, 0, 0, 190))
    screen.blit(button_surface, rect)

    pygame.draw.rect(screen, WHITE, rect, 1)

    rendered_text = button_font.render(text, True, WHITE)
    text_rect = rendered_text.get_rect(center=rect.center)

    screen.blit(rendered_text, text_rect)


# defining the clickable areas for the paintings
# note for transparency: had to use claude ai to figure out the exact measurements of my drawing so as not to go insane

painting1_area = pygame.Rect(76, 42, 450, 199)    # the lovers
painting2_area = pygame.Rect(667, 0, 450, 356)    # forest
painting3_area = pygame.Rect(49, 435, 309, 267)   # sky
painting4_area = pygame.Rect(960, 505, 320, 215)  # infinity

exit_area = pygame.Rect(678, 446, 109, 46)        # exit screen (too small? remember to fix if necessary!!

show_debug_overlay = False

def draw_debug_overlay():

    for rect, label in [
        (painting1_area, "WORD_PUZZLE"),
        (painting2_area, "FOREST"),
        (painting3_area, "CLOUD"),
        (painting4_area, "STARS"),
        (exit_area, "EXIT"),
    ]:

        pygame.draw.rect(screen, (255, 0, 0), rect, 3)
        label_text = notice_font.render(label, True, (255, 0, 0))
        screen.blit(label_text, (rect.x, rect.y - 20))


# starting work on forest maze

MAZE_COLS = 30
MAZE_ROWS = 16

MAZE_X = 80
MAZE_Y = 100

MAZE_WIDTH = 1120
MAZE_HEIGHT = 550

CELL_WIDTH = MAZE_WIDTH // MAZE_COLS
CELL_HEIGHT = MAZE_HEIGHT // MAZE_ROWS

EXTRA_OPENING_CHANCE = 0.15


def generate_maze():

    maze = []

    for row in range(MAZE_ROWS):
        maze.append([])
        for col in range(MAZE_COLS):
            maze[row].append({
                "visited": False,
                "top": True,
                "right": True,
                "bottom": True,
                "left": True
            })

    start_row = 0
    start_col = 0
    maze[start_row][start_col]["visited"] = True

    stack = [(start_row, start_col)]

    while stack:

        current_row, current_col = stack[-1]
        neighbours = []

        if current_row > 0 and not maze[current_row - 1][current_col]["visited"]:
            neighbours.append(("up", current_row - 1, current_col))

        if current_col < MAZE_COLS - 1 and not maze[current_row][current_col + 1]["visited"]:
            neighbours.append(("right", current_row, current_col + 1))

        if current_row < MAZE_ROWS - 1 and not maze[current_row + 1][current_col]["visited"]:
            neighbours.append(("down", current_row + 1, current_col))

        if current_col > 0 and not maze[current_row][current_col - 1]["visited"]:
            neighbours.append(("left", current_row, current_col - 1))

        if neighbours:

            direction, new_row, new_col = random.choice(neighbours)

            if direction == "up":
                maze[current_row][current_col]["top"] = False
                maze[new_row][new_col]["bottom"] = False
            elif direction == "right":
                maze[current_row][current_col]["right"] = False
                maze[new_row][new_col]["left"] = False
            elif direction == "down":
                maze[current_row][current_col]["bottom"] = False
                maze[new_row][new_col]["top"] = False
            elif direction == "left":
                maze[current_row][current_col]["left"] = False
                maze[new_row][new_col]["right"] = False

            maze[new_row][new_col]["visited"] = True
            stack.append((new_row, new_col))

        else:
            stack.pop()

    return maze


def add_maze_loops(maze, chance):


    for row in range(MAZE_ROWS):
        for col in range(MAZE_COLS):

            cell = maze[row][col]

            if col < MAZE_COLS - 1 and cell["right"]:
                if random.random() < chance:
                    cell["right"] = False
                    maze[row][col + 1]["left"] = False

            if row < MAZE_ROWS - 1 and cell["bottom"]:
                if random.random() < chance:
                    cell["bottom"] = False
                    maze[row + 1][col]["top"] = False

    return maze


forest_maze = generate_maze()
forest_maze = add_maze_loops(forest_maze, EXTRA_OPENING_CHANCE)

forest_goal_row = MAZE_ROWS - 1
forest_goal_col = MAZE_COLS - 1


def draw_forest_maze():

    maze_color = (220, 230, 210)

    for row in range(MAZE_ROWS):
        for col in range(MAZE_COLS):

            cell = forest_maze[row][col]
            x = MAZE_X + col * CELL_WIDTH
            y = MAZE_Y + row * CELL_HEIGHT

            if cell["top"]:
                pygame.draw.line(screen, maze_color, (x, y), (x + CELL_WIDTH, y), 4)

            if cell["right"]:
                pygame.draw.line(screen, maze_color, (x + CELL_WIDTH, y), (x + CELL_WIDTH, y + CELL_HEIGHT), 4)

            if cell["bottom"]:
                pygame.draw.line(screen, maze_color, (x, y + CELL_HEIGHT), (x + CELL_WIDTH, y + CELL_HEIGHT), 4)

            if cell["left"]:
                pygame.draw.line(screen, maze_color, (x, y), (x, y + CELL_HEIGHT), 4)

    goal_x = MAZE_X + forest_goal_col * CELL_WIDTH
    goal_y = MAZE_Y + forest_goal_row * CELL_HEIGHT

    pygame.draw.rect(screen, GOLD, (goal_x + 4, goal_y + 4, CELL_WIDTH - 8, CELL_HEIGHT - 8))
# feedback update: maze is good level of difficulty like this

def reset_forest_player():

    global player_x, player_y, player_row, player_col, player_angle

    player_row = 0
    player_col = 0
    player_x = MAZE_X + CELL_WIDTH // 2
    player_y = MAZE_Y + CELL_HEIGHT // 2
    player_angle = -90  # facing up


player_x = 0
player_y = 0
player_row = 0
player_col = 0
player_angle = -90

reset_forest_player()

PLAYER_SPEED = 4
PLAYER_RADIUS = 9


def draw_player():

    tip_length = PLAYER_RADIUS          # matches the collision boundary exactly
    back_length = PLAYER_RADIUS * 1.1
    back_spread = math.radians(125)     # wider stance, less needle-like

    angle_rad = math.radians(player_angle)

    tip = (
        player_x + tip_length * math.cos(angle_rad),
        player_y + tip_length * math.sin(angle_rad)
    )

    back_left = (
        player_x + back_length * math.cos(angle_rad + back_spread),
        player_y + back_length * math.sin(angle_rad + back_spread)
    )

    back_right = (
        player_x + back_length * math.cos(angle_rad - back_spread),
        player_y + back_length * math.sin(angle_rad - back_spread)
    )

    pygame.draw.polygon(screen, WHITE, [tip, back_left, back_right])


def move_forest_player(keys):

    global player_x, player_y, player_row, player_col, player_angle

    dx = 0
    dy = 0

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx -= PLAYER_SPEED

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx += PLAYER_SPEED

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy -= PLAYER_SPEED

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy += PLAYER_SPEED

    if dx != 0 or dy != 0:
        player_angle = math.degrees(math.atan2(dy, dx))

    player_col = int((player_x - MAZE_X) // CELL_WIDTH)
    player_row = int((player_y - MAZE_Y) // CELL_HEIGHT)

    player_col = max(0, min(MAZE_COLS - 1, player_col))
    player_row = max(0, min(MAZE_ROWS - 1, player_row))

    cell = forest_maze[player_row][player_col]

    cell_left = MAZE_X + player_col * CELL_WIDTH
    cell_right = cell_left + CELL_WIDTH
    cell_top = MAZE_Y + player_row * CELL_HEIGHT
    cell_bottom = cell_top + CELL_HEIGHT

    new_x = player_x + dx

    if dx > 0 and cell["right"] and new_x + PLAYER_RADIUS > cell_right:
        new_x = cell_right - PLAYER_RADIUS

    if dx < 0 and cell["left"] and new_x - PLAYER_RADIUS < cell_left:
        new_x = cell_left + PLAYER_RADIUS

    player_x = new_x

    new_y = player_y + dy

    if dy > 0 and cell["bottom"] and new_y + PLAYER_RADIUS > cell_bottom:
        new_y = cell_bottom - PLAYER_RADIUS

    if dy < 0 and cell["top"] and new_y - PLAYER_RADIUS < cell_top:
        new_y = cell_top + PLAYER_RADIUS

    player_y = new_y

    if player_row == forest_goal_row and player_col == forest_goal_col:
        collected_letters["FOREST"] = True
# movement working!! yayyy

# the word puzzle for the lovers painting i wrote in advance so just need to add it now

BLANK_WIDTH = 140
WORD_SPACE = 12
LINE_SPACING = 65
LINE_HEIGHT = puzzle_font.get_linesize()

POEM_START_Y = 160
POOL_START_Y = 480

word_puzzle_lines = [
    [("word", "A"), ("word", "band"), ("word", "that"), ("word", "ties"),
     ("word", "two"), ("blank", 0), ("word", "together,")],

    [("word", "a"), ("word", "curse"), ("word", "that"), ("word", "holds"),
     ("word", "two"), ("blank", 1), ("word", "apart,")],

    [("word", "may"), ("word", "one"), ("word", "day"), ("word", "be"),
     ("word", "forever"), ("blank", 2), ("word", ",")],

    [("word", "if"), ("word", "hope"), ("word", "only"), ("word", "remains"),
     ("word", "in"), ("blank", 3), ("word", "of"), ("blank", 4), ("word", "hearts.")],
]

word_puzzle_answers = {
    0: "souls",
    1: "lovers",
    2: "broken",
    3: "both",
    4: "their",
}

word_puzzle_distractors = ["people", "minds", "worlds"]
# feedback update: good level of difficulty now, was too many words before
word_puzzle_state = {
    "pool": [],
    "blanks": {bid: None for bid in word_puzzle_answers},
    "selected_pool_index": None,
    "checked": False,
    "all_correct": False,
}


def reset_word_puzzle():

    words = list(word_puzzle_answers.values()) + list(word_puzzle_distractors)
    random.shuffle(words)

    word_puzzle_state["pool"] = [{"word": w, "placed": False} for w in words]
    word_puzzle_state["blanks"] = {bid: None for bid in word_puzzle_answers}
    word_puzzle_state["selected_pool_index"] = None
    word_puzzle_state["checked"] = False
    word_puzzle_state["all_correct"] = False


reset_word_puzzle()


def compute_puzzle_line_layout(y_start):

    layout = []
    y = y_start

    for line in word_puzzle_lines:

        widths = []

        for ttype, tval in line:
            if ttype == "word":
                widths.append(puzzle_font.size(tval)[0])
            else:
                widths.append(BLANK_WIDTH)

        total_width = sum(widths) + WORD_SPACE * (len(widths) - 1)
        x = WIDTH // 2 - total_width // 2

        row = []

        for (ttype, tval), w in zip(line, widths):

            rect = pygame.Rect(x, y, w, LINE_HEIGHT)

            if ttype == "word":
                row.append({"type": "word", "text": tval, "rect": rect})
            else:
                row.append({"type": "blank", "blank_id": tval, "rect": rect})

            x += w + WORD_SPACE

        layout.append(row)
        y += LINE_SPACING

    return layout


def compute_pool_layout(y):

    cols = 4
    cell_w = 170
    cell_h = 40
    gap_x = 16
    gap_y = 16

    total_row_width = cols * cell_w + (cols - 1) * gap_x
    start_x = WIDTH // 2 - total_row_width // 2

    rects = []

    for idx in range(len(word_puzzle_state["pool"])):

        row = idx // cols
        col = idx % cols

        x = start_x + col * (cell_w + gap_x)
        y_pos = y + row * (cell_h + gap_y)

        rects.append(pygame.Rect(x, y_pos, cell_w, cell_h))

    return rects


def draw_word_pool(y):

    rects = compute_pool_layout(y)

    for idx, item in enumerate(word_puzzle_state["pool"]):

        if item["placed"]:
            continue

        rect = rects[idx]
        selected = (word_puzzle_state["selected_pool_index"] == idx)

        # adding dark panel for visibility
        panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 225))
        screen.blit(panel, rect)

        border_color = GOLD if selected else WHITE
        pygame.draw.rect(screen, border_color, rect, 1)

        # small drop-shadow behind the word for extra contrast.
        shadow_surf = pool_font.render(item["word"], True, BLACK)
        shadow_rect = shadow_surf.get_rect(center=(rect.centerx + 1, rect.centery + 1))
        screen.blit(shadow_surf, shadow_rect)

        text_surf = pool_font.render(item["word"], True, WHITE)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)


def draw_word_puzzle():

    screen.blit(lovers_image, (0, 0))

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 130))
    screen.blit(overlay, (0, 0))

    title = button_font.render('Complete the description of "The Lovers"', True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, 90))
    screen.blit(title, title_rect)

    layout = compute_puzzle_line_layout(POEM_START_Y)

    for row in layout:
        for token in row:

            if token["type"] == "word":

                text_surf = puzzle_font.render(token["text"], True, WHITE)
                screen.blit(text_surf, token["rect"].topleft)

            else:

                bid = token["blank_id"]
                filled_word = word_puzzle_state["blanks"][bid]

                if word_puzzle_state["checked"]:
                    if filled_word == word_puzzle_answers[bid]:
                        color = (90, 200, 120)
                    else:
                        color = (200, 90, 90)
                else:
                    color = WHITE

                pygame.draw.rect(screen, color, token["rect"], 1)

                if filled_word:
                    word_surf = puzzle_font.render(filled_word, True, WHITE)
                    word_rect = word_surf.get_rect(center=token["rect"].center)
                    screen.blit(word_surf, word_rect)

    draw_word_pool(POOL_START_Y)

    if word_puzzle_state["all_correct"]:

        letter = GAME_LETTER_REWARDS["WORD_PUZZLE"]
        msg_text = f'Correct! You collected the letter "{letter}". Press ESC to leave.'
        msg = button_font.render(msg_text, True, GOLD)
        draw_text_with_backdrop(msg, 650)

    else:

        all_filled = all(v is not None for v in word_puzzle_state["blanks"].values())

        if all_filled:
            check_rect = get_button_rect("Check Answer", 650)
            draw_button("Check Answer", check_rect)
        else:
            hint = notice_font.render("Click a word below, then click a blank to place it.", True, WHITE)
            draw_text_with_backdrop(hint, 650)

        if word_puzzle_state["checked"] and not word_puzzle_state["all_correct"]:

            msg = notice_font.render(
                "Not quite - click a red blank to remove it and try again.", True, (255, 150, 150)
            )
            draw_text_with_backdrop(msg, 685)


def handle_word_puzzle_click(pos):

    if word_puzzle_state["all_correct"]:
        return

    all_filled = all(v is not None for v in word_puzzle_state["blanks"].values())

    if all_filled:

        check_rect = get_button_rect("Check Answer", 650)

        if check_rect.collidepoint(pos):

            correct = all(
                word_puzzle_state["blanks"][bid] == answer
                for bid, answer in word_puzzle_answers.items()
            )

            word_puzzle_state["checked"] = True

            if correct:
                word_puzzle_state["all_correct"] = True
                collected_letters["WORD_PUZZLE"] = True

            return

    pool_rects = compute_pool_layout(POOL_START_Y)

    for idx, rect in enumerate(pool_rects):

        item = word_puzzle_state["pool"][idx]

        if item["placed"]:
            continue

        if rect.collidepoint(pos):

            if word_puzzle_state["selected_pool_index"] == idx:
                word_puzzle_state["selected_pool_index"] = None
            else:
                word_puzzle_state["selected_pool_index"] = idx

            return

    layout = compute_puzzle_line_layout(POEM_START_Y)

    for row in layout:
        for token in row:

            if token["type"] != "blank":
                continue

            if not token["rect"].collidepoint(pos):
                continue

            bid = token["blank_id"]
            current_word = word_puzzle_state["blanks"][bid]

            if current_word is not None:

                for item in word_puzzle_state["pool"]:
                    if item["word"] == current_word and item["placed"]:
                        item["placed"] = False
                        break

                word_puzzle_state["blanks"][bid] = None
                word_puzzle_state["checked"] = False

            elif word_puzzle_state["selected_pool_index"] is not None:

                sel_idx = word_puzzle_state["selected_pool_index"]
                sel_item = word_puzzle_state["pool"][sel_idx]

                word_puzzle_state["blanks"][bid] = sel_item["word"]
                sel_item["placed"] = True
                word_puzzle_state["selected_pool_index"] = None
                word_puzzle_state["checked"] = False

            return


# cloud mini game

CLOUD_GRAVITY = 0.7
CLOUD_JUMP_VELOCITY = -13
CLOUD_MOVE_SPEED = 5

CLOUD_PLAYER_WIDTH = 16
CLOUD_PLAYER_HEIGHT = 24

CLOUD_GROUND_Y = 560

CLOUD_TIME_LIMIT = 10.0  # seconds

# note for later: maybe try making some clouds move left right and some up down




cloud_platforms_config = [
    {"base_x": 90,   "base_y": CLOUD_GROUND_Y, "axis": "x", "range": 25, "speed": 0.032, "phase": 0.0},
    {"base_x": 215,  "base_y": CLOUD_GROUND_Y, "axis": "y", "range": 90, "speed": 0.032, "phase": 0.5},
    {"base_x": 340,  "base_y": CLOUD_GROUND_Y, "axis": "x", "range": 25, "speed": 0.036, "phase": 1.0},
    {"base_x": 465,  "base_y": CLOUD_GROUND_Y, "axis": "y", "range": 90, "speed": 0.030, "phase": 1.5},
    {"base_x": 590,  "base_y": CLOUD_GROUND_Y, "axis": "x", "range": 25, "speed": 0.038, "phase": 2.0},
    {"base_x": 715,  "base_y": CLOUD_GROUND_Y, "axis": "y", "range": 90, "speed": 0.033, "phase": 2.5},
    {"base_x": 840,  "base_y": CLOUD_GROUND_Y, "axis": "x", "range": 25, "speed": 0.035, "phase": 3.0},
    {"base_x": 965,  "base_y": CLOUD_GROUND_Y, "axis": "y", "range": 85, "speed": 0.031, "phase": 3.5},
    {"base_x": 1090, "base_y": CLOUD_GROUND_Y, "axis": "x", "range": 25, "speed": 0.037, "phase": 4.0},
    {"base_x": 1200, "base_y": CLOUD_GROUND_Y, "axis": "y", "range": 80, "speed": 0.034, "phase": 4.5},
]

CLOUD_PLATFORM_WIDTH = 65
CLOUD_PLATFORM_HEIGHT = 16
CLOUD_PLATFORM_VISUAL_WIDTH = 105
CLOUD_PLAYER_VISUAL_HEIGHT = 75

person_image_raw = pygame.image.load(
    "assets/images/person.png"
).convert_alpha()
person_image_raw = autocrop_surface(person_image_raw)

person_aspect_ratio = person_image_raw.get_width() / person_image_raw.get_height()
person_visual_width = int(CLOUD_PLAYER_VISUAL_HEIGHT * person_aspect_ratio)

person_image = pygame.transform.smoothscale(
    person_image_raw, (person_visual_width, CLOUD_PLAYER_VISUAL_HEIGHT)
)

cloud_image_raw = pygame.image.load(
    "assets/images/cloud.png"
).convert_alpha()
cloud_image_raw = autocrop_surface(cloud_image_raw, tolerance=10, stride=1)

cloud_aspect_ratio = cloud_image_raw.get_height() / cloud_image_raw.get_width()
cloud_visual_height = int(CLOUD_PLATFORM_VISUAL_WIDTH * cloud_aspect_ratio)

cloud_image = pygame.transform.smoothscale(
    cloud_image_raw, (CLOUD_PLATFORM_VISUAL_WIDTH, cloud_visual_height)
)

cloud_state = {
    "player_x": 0.0,
    "player_y": 0.0,
    "vel_x": 0.0,
    "vel_y": 0.0,
    "on_ground": True,
    "time": 0.0,
    "platform_rects": [],
    "prev_platform_x": [],
    "prev_platform_y": [],
    "standing_on": None,
    "won": False,
    "lost": False,
    "time_left": CLOUD_TIME_LIMIT,
}


def reset_cloud_game():

    cloud_state["platform_rects"] = []
    cloud_state["prev_platform_x"] = []
    cloud_state["prev_platform_y"] = []

    for cfg in cloud_platforms_config:
        rect = pygame.Rect(
            0, 0, CLOUD_PLATFORM_WIDTH, CLOUD_PLATFORM_HEIGHT
        )
        rect.center = (cfg["base_x"], cfg["base_y"])
        cloud_state["platform_rects"].append(rect)
        cloud_state["prev_platform_x"].append(rect.centerx)
        cloud_state["prev_platform_y"].append(rect.centery)

    start_rect = cloud_state["platform_rects"][0]

    cloud_state["player_x"] = float(start_rect.centerx)
    cloud_state["player_y"] = float(start_rect.top - CLOUD_PLAYER_HEIGHT)
    cloud_state["vel_x"] = 0.0
    cloud_state["vel_y"] = 0.0
    cloud_state["on_ground"] = True
    cloud_state["time"] = 0.0
    cloud_state["standing_on"] = 0
    cloud_state["won"] = False
    cloud_state["lost"] = False
    cloud_state["time_left"] = CLOUD_TIME_LIMIT


reset_cloud_game()


def get_cloud_player_rect():

    return pygame.Rect(
        int(cloud_state["player_x"] - CLOUD_PLAYER_WIDTH / 2),
        int(cloud_state["player_y"]),
        CLOUD_PLAYER_WIDTH,
        CLOUD_PLAYER_HEIGHT,
    )


def update_cloud_platforms():

    cloud_state["time"] += 1

    for idx, cfg in enumerate(cloud_platforms_config):

        rect = cloud_state["platform_rects"][idx]
        cloud_state["prev_platform_x"][idx] = rect.centerx
        cloud_state["prev_platform_y"][idx] = rect.centery

        offset = math.sin(cloud_state["time"] * cfg["speed"] + cfg["phase"]) * cfg["range"]

        if cfg["axis"] == "x":
            rect.centerx = int(cfg["base_x"] + offset)
            rect.centery = cfg["base_y"]
        else:
            rect.centery = int(cfg["base_y"] + offset)
            rect.centerx = cfg["base_x"]


def update_cloud_game(keys):

    if cloud_state["won"] or cloud_state["lost"]:
        return

    # failure if time runs out
    # note: too fast?
    cloud_state["time_left"] -= 1 / 60

    if cloud_state["time_left"] <= 0:
        cloud_state["time_left"] = 0
        cloud_state["lost"] = True
        return

   # horizontal
    cloud_state["vel_x"] = 0

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        cloud_state["vel_x"] = -CLOUD_MOVE_SPEED

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        cloud_state["vel_x"] = CLOUD_MOVE_SPEED

    # jump function
    if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and cloud_state["on_ground"]:
        cloud_state["vel_y"] = CLOUD_JUMP_VELOCITY
        cloud_state["on_ground"] = False
        cloud_state["standing_on"] = None


    if cloud_state["on_ground"] and cloud_state["standing_on"] is not None:

        idx = cloud_state["standing_on"]
        rect = cloud_state["platform_rects"][idx]

        delta_x = rect.centerx - cloud_state["prev_platform_x"][idx]
        cloud_state["player_x"] += delta_x


        cloud_state["player_y"] = rect.top - CLOUD_PLAYER_HEIGHT

    # in desparate need for a gravity function so the player stops floating lol
    cloud_state["vel_y"] += CLOUD_GRAVITY

    prev_bottom = cloud_state["player_y"] + CLOUD_PLAYER_HEIGHT

    cloud_state["player_x"] += cloud_state["vel_x"]
    cloud_state["player_y"] += cloud_state["vel_y"]

    cloud_state["player_x"] = max(
        CLOUD_PLAYER_WIDTH / 2, min(WIDTH - CLOUD_PLAYER_WIDTH / 2, cloud_state["player_x"])
    )

    player_rect = get_cloud_player_rect()

    cloud_state["on_ground"] = False
    cloud_state["standing_on"] = None

    if cloud_state["vel_y"] >= 0:

        for idx, rect in enumerate(cloud_state["platform_rects"]):

            horizontal_overlap = player_rect.right > rect.left and player_rect.left < rect.right
            was_above = prev_bottom <= rect.top + 1
            now_at_or_below = player_rect.bottom >= rect.top

            if horizontal_overlap and was_above and now_at_or_below and player_rect.bottom <= rect.bottom + 14:

                cloud_state["player_y"] = rect.top - CLOUD_PLAYER_HEIGHT
                cloud_state["vel_y"] = 0
                cloud_state["on_ground"] = True
                cloud_state["standing_on"] = idx

                if idx == len(cloud_state["platform_rects"]) - 1:
                    cloud_state["won"] = True
                    collected_letters["CLOUD"] = True

                break

    # respawning on platform/fixing disappearing issue of player
    if cloud_state["player_y"] > HEIGHT:

        start_rect = cloud_state["platform_rects"][0]
        cloud_state["player_x"] = float(start_rect.centerx)
        cloud_state["player_y"] = float(start_rect.top - CLOUD_PLAYER_HEIGHT)
        cloud_state["vel_x"] = 0.0
        cloud_state["vel_y"] = 0.0
        cloud_state["on_ground"] = True
        cloud_state["standing_on"] = 0


def draw_cloud_game():

    screen.blit(sky_image, (0, 0))

    last_index = len(cloud_state["platform_rects"]) - 1

    # cloud platforms
    for idx, rect in enumerate(cloud_state["platform_rects"]):

        cloud_rect = cloud_image.get_rect(center=rect.center)
        screen.blit(cloud_image, cloud_rect)

        if idx == last_index:
            goal_label = notice_font.render("GOAL", True, GOLD if cloud_state["won"] else WHITE)
            label_rect = goal_label.get_rect(center=(rect.centerx, cloud_rect.top - 12))
            screen.blit(goal_label, label_rect)

    # fix player size issue due to framed png
    player_rect = get_cloud_player_rect()
    visual_rect = person_image.get_rect(midbottom=player_rect.midbottom)
    screen.blit(person_image, visual_rect)

    # timer display
    timer_color = (255, 130, 130) if cloud_state["time_left"] <= 3 else WHITE
    timer_text = notice_font.render(f"Time: {cloud_state['time_left']:.1f}s", True, timer_color)
    draw_text_with_backdrop(timer_text, 40)

    if cloud_state["won"]:

        letter = GAME_LETTER_REWARDS["CLOUD"]

        if letter:
            msg_text = f'You made it across! You collected the letter "{letter}". Press ESC to return.'
        else:
            msg_text = "You made it across! Letter collected. Press ESC to return."

        msg = button_font.render(msg_text, True, GOLD)
        draw_text_with_backdrop(msg, 90)

    elif cloud_state["lost"]:

        msg = button_font.render("Out of time! Press R to try again, or ESC to leave.", True, (255, 150, 150))
        draw_text_with_backdrop(msg, 90)

    else:

        hint = notice_font.render("Arrow keys / WASD to move, Space to jump", True, WHITE)
        draw_text_with_backdrop(hint, 90)


# infinity game

STARS_TARGET_SCORE = 15
STARS_MAX_LIVES = 3

STARS_PADDLE_WIDTH = 120
STARS_PADDLE_HEIGHT = 18
STARS_PADDLE_Y = 660
STARS_PADDLE_SPEED = 13

STARS_FALL_SPEED_MIN = 7.0
STARS_FALL_SPEED_MAX = 11.5
STARS_SPAWN_INTERVAL = 20

STARS_METEOR_CHANCE = 0.28
STARS_COMET_CHANCE = 0.22
STARS_ASTEROID_CHANCE = 0.22

STARS_OBJECT_RADIUS = 24
STARS_ASTEROID_RADIUS = int(STARS_OBJECT_RADIUS * 1.4)  # bigger hitbox, harder to dodge

stars_state = {
    "paddle_x": WIDTH // 2,
    "objects": [],  # each: {"x", "y", "speed", "type", "radius"}
    "score": 0,
    "lives": STARS_MAX_LIVES,
    "spawn_timer": 0,
    "won": False,
    "lost": False,
}


def reset_stars_game():

    stars_state["paddle_x"] = WIDTH // 2
    stars_state["objects"] = []
    stars_state["score"] = 0
    stars_state["lives"] = STARS_MAX_LIVES
    stars_state["spawn_timer"] = 0
    stars_state["won"] = False
    stars_state["lost"] = False


reset_stars_game()


def get_stars_paddle_rect():

    return pygame.Rect(
        int(stars_state["paddle_x"] - STARS_PADDLE_WIDTH / 2),
        STARS_PADDLE_Y,
        STARS_PADDLE_WIDTH,
        STARS_PADDLE_HEIGHT,
    )


def spawn_star_object():

    roll = random.random()

    if roll < STARS_METEOR_CHANCE:
        obj_type = "meteor"
    elif roll < STARS_METEOR_CHANCE + STARS_COMET_CHANCE:
        obj_type = "comet"
    elif roll < STARS_METEOR_CHANCE + STARS_COMET_CHANCE + STARS_ASTEROID_CHANCE:
        obj_type = "asteroid"
    else:
        obj_type = "star"

    if obj_type == "comet":
        speed = random.uniform(STARS_FALL_SPEED_MAX, STARS_FALL_SPEED_MAX + 3.5)
    elif obj_type == "asteroid":
        speed = random.uniform(STARS_FALL_SPEED_MIN * 0.7, STARS_FALL_SPEED_MIN * 1.1)
    else:
        speed = random.uniform(STARS_FALL_SPEED_MIN, STARS_FALL_SPEED_MAX)

    radius = STARS_ASTEROID_RADIUS if obj_type == "asteroid" else STARS_OBJECT_RADIUS

    stars_state["objects"].append({
        "x": random.randint(40, WIDTH - 40),
        "y": -radius,
        "speed": speed,
        "type": obj_type,
        "radius": radius,
    })


def update_stars_game(keys):

    if stars_state["won"] or stars_state["lost"]:
        return

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        stars_state["paddle_x"] -= STARS_PADDLE_SPEED

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        stars_state["paddle_x"] += STARS_PADDLE_SPEED

    half_paddle = STARS_PADDLE_WIDTH / 2
    stars_state["paddle_x"] = max(half_paddle, min(WIDTH - half_paddle, stars_state["paddle_x"]))

    stars_state["spawn_timer"] += 1

    if stars_state["spawn_timer"] >= STARS_SPAWN_INTERVAL:
        stars_state["spawn_timer"] = 0
        spawn_star_object()

    paddle_rect = get_stars_paddle_rect()
    remaining_objects = []

    for obj in stars_state["objects"]:

        obj["y"] += obj["speed"]

        r = obj["radius"]

        obj_rect = pygame.Rect(
            obj["x"] - r,
            obj["y"] - r,
            r * 2,
            r * 2,
        )

        if obj_rect.colliderect(paddle_rect):

            if obj["type"] == "star":
                stars_state["score"] += 1
            else:
                stars_state["lives"] -= 1

            continue  # remove from game if caught

        if obj["y"] - r > HEIGHT:
            continue  # fell through the bottom = harmless

        remaining_objects.append(obj)

    stars_state["objects"] = remaining_objects

    if stars_state["score"] >= STARS_TARGET_SCORE:
        stars_state["won"] = True
        collected_letters["STARS"] = True

    elif stars_state["lives"] <= 0:
        stars_state["lost"] = True


def draw_star_shape(surface, center, radius, color):

    points = []

    for i in range(10):

        angle = math.radians(i * 36 - 90)
        r = radius if i % 2 == 0 else radius * 0.45

        points.append((
            center[0] + r * math.cos(angle),
            center[1] + r * math.sin(angle),
        ))

    pygame.draw.polygon(surface, color, points)


def draw_comet_shape(surface, center, radius, color):

    # adding a glowing for solely for aesthetic purposes lol
    tail_length = radius * 2.2

    tail_points = [
        (center[0] - radius * 0.6, center[1] - radius * 0.4),
        (center[0] + radius * 0.6, center[1] - radius * 0.4),
        (center[0], center[1] - tail_length),
    ]

    pygame.draw.polygon(surface, (120, 200, 230), tail_points)
    pygame.draw.circle(surface, (210, 240, 250), center, int(radius * 0.8))
    pygame.draw.circle(surface, color, center, int(radius * 0.8), 2)


def draw_asteroid_shape(surface, center, radius, color):

    # also adding a bigger jagged rock
    points = []
    num_points = 8

    for i in range(num_points):

        angle = math.radians(i * (360 / num_points))
        jitter = random.uniform(0.75, 1.0)
        r = radius * jitter

        points.append((
            center[0] + r * math.cos(angle),
            center[1] + r * math.sin(angle),
        ))

    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, (60, 55, 50), points, 2)


def draw_stars_game():

    screen.blit(stars_bg_image, (0, 0))

    for obj in stars_state["objects"]:

        pos = (int(obj["x"]), int(obj["y"]))
        r = obj["radius"]

        if obj["type"] == "star":
            draw_star_shape(screen, pos, r, GOLD)
        elif obj["type"] == "meteor":
            pygame.draw.circle(screen, (140, 60, 40), pos, r)
            pygame.draw.circle(screen, (90, 40, 25), pos, r, 2)
        elif obj["type"] == "comet":
            draw_comet_shape(screen, pos, r, (60, 140, 170))
        else:  # asteroid
            draw_asteroid_shape(screen, pos, r, (120, 115, 110))

    paddle_rect = get_stars_paddle_rect()
    pygame.draw.rect(screen, WHITE, paddle_rect, border_radius=8)

    score_text = notice_font.render(
        f"Stars: {stars_state['score']} / {STARS_TARGET_SCORE}    Lives: {stars_state['lives']}",
        True, WHITE
    )
    draw_text_with_backdrop(score_text, 60)

    if stars_state["won"]:

        letter = GAME_LETTER_REWARDS["STARS"]

        if letter:
            msg_text = f'Yay! You caught enough stars! You collected the letter "{letter}". Press ESC to return.'
        else:
            msg_text = "Yay! You caught enough stars! Letter collected. Press ESC to return."

        msg = button_font.render(msg_text, True, GOLD)
        draw_text_with_backdrop(msg, 120)

    elif stars_state["lost"]:

        msg = button_font.render("Ouh that was close! Press R to try again, or ESC to leave.", True, (255, 150, 150))
        draw_text_with_backdrop(msg, 120)

    else:

        hint = notice_font.render("Press left/right or up/down to move - Goal: catch the stars, avoid everything else!", True, WHITE)
        draw_text_with_backdrop(hint, 120)


# exit screen

exit_win_lines = [
    "Oh my! it seems you have managed to unlock the door!",
    "I guess you are free to go then..",
    "(We should definitely add more riddles next time..)",
    "Oh sorry you weren't meant to hear that!",
    "Goodbye!",
]

exit_state = {
    "result": None,
    "line_index": 0,
    "displayed_text": "",
    "typing_index": 0,
    "last_typing_time": 0,
    "sound_queue": [],
}


def enter_exit_screen():

    global game_state

    game_state = "EXIT"

    play_music(MAIN_THEME_PATH)

    exit_state["line_index"] = 0
    exit_state["displayed_text"] = ""
    exit_state["typing_index"] = 0
    exit_state["last_typing_time"] = 0
    exit_state["sound_queue"] = []

    if all_letters_collected():

        exit_state["result"] = "WIN"
        exit_state["sound_queue"] = [exit_click_sound, exit_door_sound, exit_win_sound]

        first_sound = exit_state["sound_queue"].pop(0)
        exit_sound_channel.play(first_sound)

    else:

        exit_state["result"] = "LOSE"
        exit_sound_channel.play(exit_lose_sound)


def exit_current_line_text():

    return exit_win_lines[exit_state["line_index"]]


def exit_step_finished_typing():

    return exit_state["typing_index"] >= len(exit_current_line_text())


def advance_exit_line():

    exit_state["line_index"] += 1

    if exit_state["line_index"] >= len(exit_win_lines):
        exit_state["line_index"] = len(exit_win_lines) - 1

    exit_state["displayed_text"] = ""
    exit_state["typing_index"] = 0


def update_exit_screen():

    if exit_state["result"] == "WIN" and exit_state["sound_queue"]:

        if not exit_sound_channel.get_busy():

            next_sound = exit_state["sound_queue"].pop(0)
            exit_sound_channel.play(next_sound)

    if exit_state["result"] != "WIN":
        return

    current_text = exit_current_line_text()
    current_time = pygame.time.get_ticks()

    if exit_state["typing_index"] < len(current_text):

        if current_time - exit_state["last_typing_time"] > typing_speed * 1000:

            exit_state["displayed_text"] += current_text[exit_state["typing_index"]]
            exit_state["typing_index"] += 1
            exit_state["last_typing_time"] = current_time


def draw_exit_screen():

    screen.blit(exit_bg_image, (0, 0))

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 110))
    screen.blit(overlay, (0, 0))

    if exit_state["result"] == "WIN":

        draw_intro_text(exit_state["displayed_text"], HEIGHT // 2)

        if exit_step_finished_typing():
            draw_continue_notice()

    else:

        text = button_font.render(
            f"You need all 4 letters ({letters_earned()}/4 so far). Press ESC.", True, WHITE
        )
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        screen.blit(text, text_rect)

        password_text = font.render(get_password_display(), True, GOLD)
        password_rect = password_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(password_text, password_rect)

    draw_letters_hud()


# small hud helper for the letters counter, and an empty dict kept around
# in case i want to add a placeholder mini-game state again later

placeholder_info = {}


def draw_letters_hud():

    text = notice_font.render(f"Letters: {letters_earned()} / 4", True, WHITE)
    screen.blit(text, (20, 20))


# alrightt, now onto the main game loop

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_b:
                show_debug_overlay = not show_debug_overlay

            if game_state == "INTRO":

                step = current_step_data()

                if not step_finished_typing():


                    displayed_text = current_step_text()
                    typing_index = len(current_step_text())

                elif "button" not in step:


                    advance_intro_step()



            elif game_state == "FOREST":

                if event.key == pygame.K_ESCAPE:
                    game_state = "MUSEUM"
                    play_music(MAIN_THEME_PATH)

            elif game_state == "WORD_PUZZLE":

                if event.key == pygame.K_ESCAPE:
                    game_state = "MUSEUM"
                    play_music(MAIN_THEME_PATH)
                elif event.key == pygame.K_r:
                    reset_word_puzzle()

            elif game_state == "CLOUD":

                if event.key == pygame.K_ESCAPE:
                    game_state = "MUSEUM"
                    play_music(MAIN_THEME_PATH)
                elif event.key == pygame.K_r:
                    reset_cloud_game()

            elif game_state == "STARS":

                if event.key == pygame.K_ESCAPE:
                    game_state = "MUSEUM"
                    play_music(MAIN_THEME_PATH)
                elif event.key == pygame.K_r:
                    reset_stars_game()

            elif game_state == "EXIT":

                if exit_state["result"] == "WIN":

                    if not exit_step_finished_typing():

                        exit_state["displayed_text"] = exit_current_line_text()
                        exit_state["typing_index"] = len(exit_current_line_text())

                    elif exit_state["line_index"] < len(exit_win_lines) - 1:

                        advance_exit_line()

                    elif event.key == pygame.K_ESCAPE:

                        game_state = "MUSEUM"

                else:

                    if event.key == pygame.K_ESCAPE:
                        game_state = "MUSEUM"

            elif game_state in placeholder_info:

                if event.key == pygame.K_RETURN:
                    collected_letters[game_state] = True
                elif event.key == pygame.K_ESCAPE:
                    game_state = "MUSEUM"
                    play_music(MAIN_THEME_PATH)

        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_state == "INTRO":

                step = current_step_data()

                if step_finished_typing() and "button" in step:

                    button_rect = get_button_rect(step["button"], 570)

                    if button_rect.collidepoint(event.pos):

                        if step["button"] == "Play":

                            game_state = "MUSEUM"
                            play_music(MAIN_THEME_PATH)

                        else:

                            advance_intro_step()

            elif game_state == "MUSEUM":

                if painting1_area.collidepoint(event.pos):
                    game_state = "WORD_PUZZLE"
                    play_music("assets/music/thelovers/lovers.mp3")
                    if not collected_letters["WORD_PUZZLE"]:
                        reset_word_puzzle()

                elif painting2_area.collidepoint(event.pos):
                    game_state = "FOREST"
                    play_music("assets/music/forest/forest.mp3")
                    forest_maze = generate_maze()
                    forest_maze = add_maze_loops(forest_maze, EXTRA_OPENING_CHANCE)
                    reset_forest_player()

                elif painting3_area.collidepoint(event.pos):
                    game_state = "CLOUD"
                    play_music("assets/music/sky/sky.mp3")
                    if not collected_letters["CLOUD"]:
                        reset_cloud_game()

                elif painting4_area.collidepoint(event.pos):
                    game_state = "STARS"
                    play_music("assets/music/nightsky/night.mp3")
                    if not collected_letters["STARS"]:
                        reset_stars_game()

                elif exit_area.collidepoint(event.pos):
                    enter_exit_screen()

            elif game_state == "WORD_PUZZLE":

                handle_word_puzzle_click(event.pos)

    # need update functions

    update_dust()

    if game_state == "INTRO":

        current_text = current_step_text()
        current_time = pygame.time.get_ticks()

        if typing_index < len(current_text):

            if current_time - last_typing_time > typing_speed * 1000:

                displayed_text += current_text[typing_index]
                typing_index += 1
                last_typing_time = current_time

    if game_state == "FOREST":

        keys = pygame.key.get_pressed()
        move_forest_player(keys)

    if game_state == "CLOUD":

        update_cloud_platforms()
        keys = pygame.key.get_pressed()
        update_cloud_game(keys)

    if game_state == "STARS":

        keys = pygame.key.get_pressed()
        update_stars_game(keys)

    if game_state == "EXIT":

        update_exit_screen()

    # drawing

    if game_state == "INTRO":

        screen.blit(intro_image, (0, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 110))
        screen.blit(overlay, (0, 0))

        draw_dust()

        draw_intro_text(displayed_text, HEIGHT // 2)

        step = current_step_data()

        if step_finished_typing():

            if "button" in step:
                button_rect = get_button_rect(step["button"], 570)
                draw_button(step["button"], button_rect)
            else:
                draw_continue_notice()

    elif game_state == "MUSEUM":

        screen.blit(gallery_image, (0, 0))
        draw_dust()
        draw_letters_hud()

        if show_debug_overlay:
            draw_debug_overlay()

    elif game_state == "FOREST":

        screen.blit(forest_image, (0, 0))
        draw_forest_maze()
        draw_player()
        draw_letters_hud()

        if collected_letters["FOREST"]:

            letter = GAME_LETTER_REWARDS["FOREST"]
            win_text = button_font.render(
                f'You collected the letter "{letter}"! Press ESC to return.', True, GOLD
            )
            win_rect = win_text.get_rect(center=(WIDTH // 2, 40))
            screen.blit(win_text, win_rect)

    elif game_state == "WORD_PUZZLE":

        draw_word_puzzle()
        draw_letters_hud()

    elif game_state == "CLOUD":

        draw_cloud_game()
        draw_letters_hud()

    elif game_state == "STARS":

        draw_stars_game()
        draw_letters_hud()

    elif game_state == "EXIT":

        draw_exit_screen()

    elif game_state in placeholder_info:

        draw_placeholder_game(game_state)
        draw_letters_hud()

    pygame.display.flip()
    clock.tick(60)

# note: main loop works now, feedback on difficulty and fun was good
# no dead-ends or mistakes noticed for now so should work properly (?)




# end of game is finalized, i thinkk it's safe to say coding is done!!




pygame.quit()
sys.exit()