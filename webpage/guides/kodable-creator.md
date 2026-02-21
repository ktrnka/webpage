---
title: "Kodable Creator tips for family"
layout: default
show_logo: false
---

# Kodable Creator tips for family (2025)

## 🚀 Moving a Character
**Make a character that can move around the screen:**
1. Pick the character you want and place it on the screen.
2. Click the character to open its settings.
3. Add a function for each arrow key (Up, Down, Left, Right):
Example: When "Up" is pressed → do "Move Up".

## 🧱 Placing Things on the Ground
**Make your character drop or place things:**
1. Click your character.
2. Add a function: When you press the **space bar (shoot)** → do "Create" → pick what you want to place (like a block).
3. Want that block to move or do something? Click it and add functions
4. Want it to block movement? Click the item, go to **properties**, and turn on **Obstacle**.

## 🔫 Shooting Projectiles
**Make your character shoot things like lasers or fireballs:**
1. First, follow the steps above to create something when you press space.
2. Now click your projectile (laser, etc.) and:
    - Add a **loop** that moves in "My Direction".
    - Add an **on create** function: set direction = direction of the parent (the shooter).
    - Optional: **add a sound** in either the shooter or in the "on create" for the projectile.

## 💥 Making Projectiles Destroy Things
Let's say you have:
- A **ship** (that shoots),
- A **laser**,
- And **asteroids** (that should explode when hit).

**Steps:**
1. Click the **asteroid**.
2. Add an **"on hit" by laser** → then "Destroy".
3. Optional: Add a **sound** and an **animation** to make it feel like a real explosion!

**Want the laser to disappear too?**
- Click the **laser**.
- Add an **"on hit" by asteroid** → then "Destroy".

_📝 Only the object being destroyed can have the "Destroy" action._

## 💪 Things That Take Multiple Hits
Let's make a **giant asteroid** that takes 3 hits to explode.

**Steps:**
1. Click the asteroid → change health from 1 to 3.
2. In its functions:
    - Change **"on hit by laser"** → use "Subtract health".
    - Add **"on health zero"** → "Destroy" and play a big explosion sound/animation.

**Extra cool idea:**
- Add **"Set Color" to red** when health is low.
- Click the color action → add "If health == 1".

Now it glows red when it's almost destroyed!

## 🤖 Making a Boss Move by Itself
To make something (like a boss enemy) move side to side on its own:

**Steps:**
1. Put the boss at the top of the screen, facing left or right.
2. Add a **loop** to move "My Direction".
3. Add **two invisible triggers**, one on the left and one on the right of the screen.
4. On the boss:
    - Add **"on hit by left trigger"** → face right.
    - Add **"on hit by right trigger**" → face left.

_📝 If your boss looks different on each side, don't use "Flip direction". It might get stuck flipping forever!_

## 🔐 Lock and Key Game
Let's build a level where the player needs a key to open a door.

**Steps:**
1. Add your player (like a ship) and make it move.
2. Place a key and a locked door.
3. On the key:
    - When hit by the player → Set has-key = True, Destroy the key, and play a pickup sound.
4. On the lock:
    - When hit by the player → If has-key == True, then Destroy the lock and play a sound.

🧪 Test it! Make sure the door doesn't open without the key!


## 🚪 Portal to Another Level
Want to go to a new level or a win screen?

**Steps:**
1. Add a second level using the dropdown above the level area.
2. Back in Level 1, place your **portal**.
3. On the portal:
    - When hit by the player → "Load Level 2".

That's also how you can make **win** or **lose** screens!

## 🧮 Keeping Score
Want to earn points for beating enemies?

**Steps:**
1. On the bad guy: when hit → "Add: Score".
2. Add **Score Text** from the text menu.
3. Add a **loop function**: "Set Text: Score" so the number updates.

Otherwise, your score might stay stuck at 0!


## ❤️ More Than 5 Health
Characters start with max health = 5. But you can add more!

**Example:**
- Add an item (like a heart).
- On hit by the player → "Add: Health".

Use this to make **healing items!**

## 🧠 Important Concepts
- **Characters** can move with arrow keys.
- **Properties** are facts about something in your game. You can think of them like the character's settings or stats. For example: How much health it has (like hearts), how fast it moves, or what color it is.
- A **function** is a list of actions your character can follow. “When something happens (an event), run this function.” Functions can do things like move, shoot, or play a sound.
- An **event** is something that happens in the game. When something happens, you can tell your character what to do. In Kodable, events are things like "on hit by something" or "on press up". You can connect those events to functions. This is called an event handler — it's like saying: “When this happens, do that.”
- **Space bar** (called "Shoot") can place or create things—not just shoot!
- A **Spawner** is invisible and can make new things appear.
- **Obstacle/Collision** means you can't move through it.

## 🧪 Pro Tips
- Test your game often!
- Test things like:
    - Does the key unlock the door?
    - Does the laser stop when it hits something?
    - Use **animations and sounds** to show when things happen (like hits, pickups, or destruction).

## ⚠️ Limitations to Know
- If you place two of the same character (like two ships), they will share the same settings.
- Some actions only work on certain types of items.
- The **background** and **sound** are the same across all levels.