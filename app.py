import pygame
import sys
import random
import requests

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AstroidEscape")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game settings
clock = pygame.time.Clock()
running = True

# Spaceship settings
ship_width, ship_height = 80, 67
ship_x, ship_y = WIDTH // 2, HEIGHT - 200
ship_speed = 5
ship_angle = 0

# Load spaceship image
spaceship_img = pygame.image.load("./sprites/spaceship.png")
spaceship_img = pygame.transform.scale(spaceship_img, (ship_width, ship_height))

# Reset game function
def reset_game():
    global ship_x, ship_y, score, asteroids, scoreVar, asteroids_data
    ship_x, ship_y = WIDTH // 2, HEIGHT - 200
    score = 0
    scoreVar = 0
    asteroids = []
    asteroids_data = fetch_asteroid_data()

# Asteroid settings
asteroids = []
asteroid_spawn_chance = 20

# Load asteroid images
asteroid_images = [
    pygame.image.load(f"./sprites/astro1-{i}.png") for i in range(6)
]
scaled_asteroids = [pygame.transform.scale(img, (50, 50)) for img in asteroid_images]

# Score settings
scoreVar = 0
score = 0

# NASA API settings
API_KEY = "Vf0izKb95ljh8S5oFmtkcw42kAhcpPkfutKHoguC"
API_URL = "https://api.nasa.gov/neo/rest/v1/feed"
asteroids_data = []

def fetch_asteroid_data():
    """Fetch asteroid data from NASA API and scale for game."""
    try:
        response = requests.get(API_URL, params={
            "start_date": "2025-01-01",
            "end_date": "2025-01-07",
            "api_key": API_KEY
        })
        data = response.json()

        # Extract asteroid size, velocity, and approach date
        asteroid_list = []
        for date in data["near_earth_objects"]:
            for asteroid in data["near_earth_objects"][date]:
                diameter = asteroid["estimated_diameter"]["meters"]["estimated_diameter_max"]
                velocity = float(asteroid["close_approach_data"][0]["relative_velocity"]["kilometers_per_second"])
                approach_date = asteroid["close_approach_data"][0]["close_approach_date"]
                name = asteroid["name"]

                # Scale size and speed
                size = int((diameter / 50) * 20)  # Adjust scale for game
                size = max(10, min(size, 60))  # Clamp size between 10-60 px
                speed = int(velocity / 10) + 1  # Adjust scale for game
                speed = max(1, min(speed, 10))  # Clamp speed between 1-10 units/frame

                asteroid_list.append({
                    "name": name,
                    "size": size,
                    "speed": speed,
                    "approach_date": approach_date
                })
        return asteroid_list
    except Exception as e:
        print(f"Error fetching asteroid data: {e}")
        return []

asteroids_data = fetch_asteroid_data()

# Load sounds
pygame.mixer.init()
background_music = pygame.mixer.Sound("./sounds/spacebgm.wav")
death_sound = pygame.mixer.Sound("./sounds/ded.wav")
background_music.set_volume(0.5)
death_sound.set_volume(0.7)

# Play background music
pygame.mixer.Sound.play(background_music, loops=-1)

def display_game_over(asteroid_details, final_score):
    """Display Game Over screen with relevant information."""
    font_title = pygame.font.Font("./fonts/PressStart2P-Regular.ttf", 40)
    font_details = pygame.font.Font("./fonts/Pixelate-Regular.ttf", 30)

    # Messages
    game_over_text = "GAME OVER"
    asteroid_info = [
        f"You got Crushed by: {asteroid_details['name']}",
        f"Score: {final_score}",
    ]

    screen.fill(BLACK)
    title_surface = font_title.render(game_over_text, True, WHITE)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 100))

    y_offset = 200
    for line in asteroid_info:
        detail_surface = font_details.render(line, True, RED)
        screen.blit(detail_surface, (WIDTH // 2 - detail_surface.get_width() // 2, y_offset))
        y_offset += 50

    pygame.display.flip()
    pygame.mixer.Sound.play(death_sound)
    pygame.time.wait(3000)
    reset_game()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ship_x > 0:
        ship_x -= ship_speed
        ship_angle = 10
    elif keys[pygame.K_RIGHT] and ship_x < WIDTH - ship_width:
        ship_x += ship_speed
        ship_angle = -10
    else:
        ship_angle = 0

    scoreVar += 1
    if scoreVar % 60 == 0:
        score += 1

    rotated_spaceship_img = pygame.transform.rotate(spaceship_img, ship_angle)
    rotated_rect = rotated_spaceship_img.get_rect(center=(ship_x + ship_width // 2, ship_y + ship_height // 2))

    if random.randint(1, asteroid_spawn_chance) == 1:
        if asteroids_data:
            asteroid_data = asteroids_data.pop(0)
            asteroid_x = random.randint(0, WIDTH - 50)
            asteroid_y = -50
            asteroid_image = random.choice(scaled_asteroids)
            size = asteroid_data["size"]
            speed = asteroid_data["speed"]
            name = asteroid_data["name"]
            asteroid_image = pygame.transform.scale(asteroid_image, (size, size))
            angle = random.randint(0, 360)
            rotated_asteroid_image = pygame.transform.rotate(asteroid_image, angle)
            rotated_rect = rotated_asteroid_image.get_rect()
            rotated_rect.center = (asteroid_x + size // 2, asteroid_y + size // 2)
            asteroids.append([asteroid_x, asteroid_y, size, speed, rotated_asteroid_image, rotated_rect, angle, asteroid_data])
        else:
            asteroid_x = random.randint(0, WIDTH - 50)
            asteroid_y = -50
            size = random.randint(10, 50)
            speed = random.randint(1, 5)
            asteroid_image = random.choice(scaled_asteroids)
            angle = random.randint(0, 360)
            rotated_asteroid_image = pygame.transform.rotate(asteroid_image, angle)
            rotated_rect = rotated_asteroid_image.get_rect()
            rotated_rect.center = (asteroid_x + size // 2, asteroid_y + size // 2)
            asteroids.append([asteroid_x, asteroid_y, size, speed, rotated_asteroid_image, rotated_rect, angle, None])

    screen.fill(BLACK)
    for asteroid in asteroids[:]:
        asteroid[1] += asteroid[3]
        asteroid[5].center = (asteroid[0] + asteroid[2] // 2, asteroid[1] + asteroid[2] // 2)
        screen.blit(asteroid[4], asteroid[5])
        if asteroid[1] > HEIGHT:
            asteroids.remove(asteroid)

    ship_rect = pygame.Rect(ship_x, ship_y, ship_width, ship_height)
    for asteroid in asteroids:
        if ship_rect.colliderect(asteroid[5]):
            display_game_over(asteroid[7], score)
            break

    font = pygame.font.Font("./fonts/Pixelate-Regular.ttf", 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(rotated_spaceship_img, rotated_rect.topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
