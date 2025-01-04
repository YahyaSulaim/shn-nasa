![AstroidEscape](https://github.com/user-attachments/assets/f5e65cb8-48c0-4dc0-b757-bf3569f32d2f)

# AstroidEscape
AstroidEscape is an exciting arcade-style game built using Pygame where players control a spaceship, dodging asteroids of varying speeds and sizes. The game dynamically generates asteroids using data from NASA's NEO (Near-Earth Object) API to create a more realistic and ever-changing environment.

## Team Members
1. [Yahya Sulaim]([https://github.com/TH-Activities/saturday-hack-night-template](https://github.com/YahyaSulaim))

## Download and Play the Game

1. **Download the Game**  
   [Download AstroidEscape](https://github.com/YahyaSulaim/shn-nasa/releases/download/v1.0/game.zip)

2. **Extract and Run**  
   - Extract the `game.zip` file.
   - Open the extracted folder and double-click **`app.exe`** to play.


## How It Works?
1. The player controls a spaceship and must dodge oncoming asteroids.
2. The game pulls asteroid data from NASA's NEO API, which provides real-time data about asteroids' speeds and sizes.
3. Each asteroid is generated based on this data, creating a diverse range of challenges for the player.
4. The player’s goal is to survive as long as possible while avoiding asteroids.

### Gameplay Demo
<video width="640" height="360" controls>
  <source src="https://github.com/YahyaSulaim/shn-nasa/raw/refs/heads/main/demo/demo0.mp4">
  Your browser does not support the video tag.
</video>

## Libraries Used
- **Pygame** (for the game engine)
- **Requests** (for connecting to the NASA API)

## How to Configure
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/AstroidEscape.git
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1. Run the game:
    In the repo directory
    ```bash
    python app.py
    ```
2. The game window will open, and you can start playing!
