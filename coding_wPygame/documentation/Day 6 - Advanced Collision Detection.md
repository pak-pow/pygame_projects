Tags: [[Python]], [[PyGame]], [[Game]], [[Programming]]

---
Today is **Day 6: Advanced Collision Detection**.

We are done writing `for` loops to check every single enemy manually (like we did in the "Dodger" game). Today, we let Pygame do the heavy lifting with **Sprite Groups** and **Masks**.

#### 1) Learning Goal

You will learn how to check for collisions between a **Sprite and a Group** (e.g., Player vs. All Enemies) and between **Group and Group** (e.g., All Bullets vs. All Asteroids) using a single line of code.

#### 2) Clear Overview

In the "Dodger" game (Chapter 21), we wrote a function `playerHasHitBaddie` that looped through every baddie to check `colliderect`1.

- **Old Way:** Slow, lots of code.
- **New Way:** `pygame.sprite.spritecollide()`. It’s faster (written in C) and handles the list logic for you.

#### 3) Deep Explanation

**A. spritecollide(sprite, group, dokill)**

This function takes a single sprite (the player) and a Group (the enemies). It returns a list of all the enemies the player is currently touching.

- **`dokill` (The Boolean):** This is the magic switch.
    
    - If `True`: Every enemy touched is **instantly removed** from all groups (deleted). Perfect for collecting coins!
    
    - If `False`: The enemies stay. Perfect for hitting a spike or wall.  

**B. groupcollide(group1, group2, dokill1, dokill2)**

This checks if any sprite in Group 1 touched any sprite in Group 2.

- Example: `bullets` vs `aliens`.
- If you set both `dokill` to `True`, the bullet _and_ the alien disappear on impact.

**C. Masks (Pixel Perfect)**

Rect collision assumes everything is a box. If you have a triangular spaceship, colliderect might say you got hit even if the bullet missed the wing but hit the empty corner of the box.

- **Masks** check the actual _pixels_. We use `pygame.sprite.collide_mask` for this (it is slower, so use it only when necessary).

---

#### 4) Runnable Pygame Code Example

This code spawns 50 Coins (Green). You are the Player (Red).


``` python
import pygame, sys, random

# 1. Setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
FPS = 60

# --- CLASSES ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0)) # Red Player
        self.rect = self.image.get_rect(center=(400, 300))
        
    def update(self):
        # Move player to mouse position
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0)) # Green Coin
        self.rect = self.image.get_rect()
        # Random spawn location
        self.rect.x = random.randrange(0, 800)
        self.rect.y = random.randrange(0, 600)

# --- GROUPS ---
all_sprites = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

# Create Player
player = Player()
all_sprites.add(player)

# Create 50 Coins
for i in range(50):
    coin = Coin()
    all_sprites.add(coin)
    coin_group.add(coin)

# --- GAME LOOP ---
score = 0
font = pygame.font.SysFont(None, 30)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 1. Update
    all_sprites.update()

    # 2. COLLISION LOGIC (The Magic Line)
    # spritecollide(sprite, group, dokill)
    # dokill=True means "Remove the coin from the group if hit"
    hit_list = pygame.sprite.spritecollide(player, coin_group, True)
    
    # hit_list is a list of all coins hit this frame.
    # We add the length of that list to the score.
    score += len(hit_list)

    # 3. Draw
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    
    # Draw Score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(FPS)
```

---
#### 5) 20-Minute Drill

**Your Task:** Modify the code above to add **Enemies**.

1. Create an `Enemy` class (make them **Blue**).
2. Create an `enemy_group`.
3. Spawn **10 Enemies** at random locations.
4. Add a collision check:
    
    - Use `spritecollide` with the player and `enemy_group`.

    - Set `dokill` to **False** (we don't want to eat the enemies!).
    
    - If the return list is not empty (meaning you hit something), print "GAME OVER" to the console (or close the game).        

*Go! This teaches you the difference between "Collecting" (`dokill=True`) and "Crashing" (`dokill=False`).*

---

#### 6) Quick Quiz

1. **What does the `True` argument do in `spritecollide(player, coins, True)`?**
    
2. **If `spritecollide` returns a list of 3 items, what happened?**
    
3. **Why is `spritecollide` better than writing a `for` loop with `colliderect`?**
    

**Answers:**

1. It kills (removes) the sprites from the group that were hit.
    
2. The player collided with 3 coins simultaneously in that single frame.
    
3. It is optimized (faster) and cleaner to write.
    

---

#### 7) Homework for Tomorrow

Take your **Pong Game**.

- Replace the manual `BALL_OBJ.colliderect(PLAYER_OBJ)` check with `spritecollide`.

- (Note: Since you probably aren't using Groups in Pong yet, you might stick to `sprite.collide_rect(ball, paddle)`, which is the Sprite version of `rect.colliderect`).    

---
#### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜ **20%**

---
#### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### Sprite vs. Group Collision:
Instead of manually looping through lists, we use `pygame.sprite.spritecollide()`.
> [!note] Syntax
> `hits = pygame.sprite.spritecollide(player, enemy_group, dokill)`
> Returns a **list** of all sprites from the group that the player hit.

#### The `dokill` Argument:
The 3rd argument in `spritecollide` determines if the hit object should be deleted.
* **`True`**: The object is removed (e.g., collecting a coin).
* **`False`**: The object stays (e.g., hitting a wall or an enemy).

#### Group vs. Group:
`pygame.sprite.groupcollide(groupA, groupB, killA, killB)` detects collisions between two entire groups (like bullets hitting asteroids). You can choose to kill neither, one, or both sides.

---

## 🛠️ WHAT I DID TODAY

* **Created Multiple Groups:** Managed a `coin_group` separately from `all_sprites`.
* **Implemented Auto-Collection:** Used `spritecollide` with `dokill=True` to instantly pick up coins and remove them from the screen.
* **Scoring:** Used the length of the collision list (`len(hits)`) to increase the score.
* **Mouse Movement:** Used `pygame.mouse.get_pos()` to make the player follow the cursor for testing.

---

## 💻 SOURCE CODE

> [!example]- SOURCE CODE
> ```python
> # Collision Logic inside Game Loop
> 
> # 1. Update positions
> all_sprites.update()
> 
> # 2. Check for Coin Collection (dokill=True)
> coins_hit = pygame.sprite.spritecollide(player, coin_group, True)
> 
> # 3. Update Score
> for coin in coins_hit:
>     score += 10
>     print("Coin collected!")
>     
> # 4. Check for Enemy Crash (dokill=False)
> enemies_hit = pygame.sprite.spritecollide(player, enemy_group, False)
> if enemies_hit:
>     print("Game Over!")
>     running = False
> ```

---

## 🧠 LEARNED TODAY

* **Optimization:** `spritecollide` is much faster than writing a manual Python `for` loop to check collisions.
* **Lists as Return Values:** Collision functions return a list, allowing us to handle multiple collisions in a single frame (e.g., a huge explosion hitting multiple enemies).

---

## 🧪 PRACTICE / EXERCISES

**Exercise: Enemy Hazards**
Goal: Add blue squares that kill the player but don't disappear.

```python
# In setup
enemy_group = pygame.sprite.Group()
# ... create enemies ...

# In Loop
if pygame.sprite.spritecollide(player, enemy_group, False):
    print("You died!")
    pygame.quit()
    sys.exit()
````

---

## 🎯 GOALS FOR TOMORROW

> [!todo] 📝 **Day 7: UI & Text Rendering**
> 
> - Create a reusable `Text` class so we don't have to write `font.render` and `blit` every time.
>     
> - Build a "Game Over" screen.
>     
> - Learn how to center text on buttons or screens properly.

