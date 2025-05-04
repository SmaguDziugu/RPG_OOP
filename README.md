# Coursework Report 

## Introduction

The goal of this coursework was to apply the theoretical knowledge gained throughout the lectures and lab sessions in a practical, creative way. I decided to create a text-based RPG battle arena game, as it provides a clear opportunity to demonstrate object-oriented programming (OOP) principles while allowing room for narrative and gameplay design.

The resulting game, titled **"Shrine of the Lost Pathways"**, follows a lone hero navigating a series of dangerous encounters within a mysterious dungeon. At this stage, the project represents a minimum viable product (MVP), focusing on core combat mechanics and game structure, with clear potential for future development and expansion. 

The program is designed to run in the terminal environment. To get started, users should ensure they have Python 3.10 or higher installed on their system. The game can be launched by either cloning the GitHub repository or downloading the project files, then navigating to the project directory in the terminal and executing the main.py script.

Once running, the player is prompted to enter their name to begin the game. Each turn, the player can choose between two actions:

Attack – Deal damage to the enemy using your equipped weapon.

Defend – Reduce incoming damage and potentially deflect it.

The game continues until either the player or the enemy is defeated (i.e., health reaches zero). At the end of each match, the player can choose to play again or exit. Match outcomes are saved to a text file (game_results.txt) for record-keeping.

## Analysis 

To begin with, the program demonstrates all four core pillars of object-oriented programming: encapsulation, inheritance, abstraction, and polymorphism. 

**Encapsulation** is achieved by declaring class attributes as protected (e.g., _health, _weapon, _is_defending) and exposing them through controlled access using Python’s @property decorators. This prevents direct access to an object's internal data and protects internal state of an object preventing accidental or unauthorized modification. For example, in the Character class, the _health attribute is protected, and access to it is controlled via a property:
~~~
@property
def health(self):
    return self._health

@health.setter
def health(self, value):
    self._health = max(0, min(value, self._max_health))
~~~
**Inheritance** is used to create a hierarchy of game characters. The abstract class Character defines common attributes and methods (such as name, health, and attack()), and both the Player and Enemy classes inherit from it. This structure avoids code duplication and allows each subclass to define unique behavior while reusing shared functionality. The Character class also uses the ABC module to enforce **abstraction** via an abstract attack() method, requiring each subclass to implement its own version:
~~~
class Character(ABC):
    ...

    @abstractmethod
    def attack(self, target):
        pass
~~~
**Polymorphism** is realized through the overriding of shared methods like attack() in each subclass. For example, the Player class has a chance to deal double damage using a critical hit mechanic, while the Enemy may trigger a rare instant-kill move. Despite calling the same method name (attack()), the behavior differs depending on the object type:
~~~
# Player attack
if is_critical:
    damage_dealt = self.weapon.damage * 2

# Enemy attack
if random.random() < self._instant_kill_chance:
    target.health = 0
~~~
Beyond the core OOP features, the project also implements the **Factory Method** design pattern. It is used to generate new Enemy instances with randomized or specified attributes. Instead of manually creating each Enemy object with Enemy(...) inside the main game logic, a centralized factory class handles all construction logic. 
~~~
class CharacterFactory:
    ...
    @classmethod
    def create_enemy(cls, name=None, weapon=None) -> Enemy:
        if name is None:
            name = random.choice(cls._enemy_name_list)
        if weapon is None:
            weapon = random.choice(cls._weapon_list)
        return Enemy(name=name, health=100, weapon=weapon)
~~~
This approach offers greater flexibility, as it eliminates the need to duplicate code when creating enemy instances. Additionally, it supports randomized generation, which enhances the gameplay experience by providing the player with varied and unpredictable encounters.

The program also demonstrates **composition**, where complex objects are built from simpler ones. A Player or Enemy object is composed of both a Weapon and a HealthBar, rather than inheriting from them. This keeps responsibilities separate and code reusable. Weapon is responsible only for damage and description. HealthBar handles visual representation of health. Player and Enemy use those classes, but don’t manage their internal logic. Also, since Weapon and HealthBar are standalone, they can be reused in other parts of the game without rewriting anything.

For example, the same HealthBar class is used by both Player and Enemy:
~~~
# Player
self._health_bar = HealthBar(self, color="green")

# Enemy
self._health_bar = HealthBar(self, color="red")
~~~
To allow the program to record and preserve player progress beyond a single game session, **file input/output (file I/O) functionality** is implemented. This ensures that key outcomes—specifically, the winner of each match, their remaining health, and the time of victory—are written to a file called game_results.txt.
~~~
def save_game_result(winner_name, winner_health):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("game_results.txt", "a") as file:
        file.write(f"{now} | Winner: {winner_name} | Health: {winner_health}\n")
~~~
The method uses the datetime module to capture the current timestamp, and appends a line to the file using the "a" mode, which ensures previous results are not overwritten.

The program’s core functionality is thoroughly tested using Python’s built-in **unittest framework**.
Mocking is used to simulate input and control randomness in tests:
~~~
@patch('builtins.input', return_value='TestPlayer')
@patch('random.random', return_value=0.05)
def test_player_critical_hit(...):
    ...
~~~
## Results
* Implemented all four pillars of object-oriented programming and demonstrated them through modular, interactive game mechanics.

* Successfully integrated the Factory Method design pattern to simplify enemy creation and enhance gameplay variability.

* Developed a complete unit test suite using Python’s unittest framework to ensure reliability and correctness of core functionality.

* Encountered challenges with applying encapsulation correctly, particularly in determining which class attributes should be protected and managed through properties. 

## Conclusion 

This coursework successfully demonstrates the practical application of object-oriented programming principles through the development of a functional text-based RPG. The project implements key concepts such as encapsulation, inheritance, abstraction, and polymorphism. Additional features like file I/O, structured unit testing, and the use of the Factory Method design pattern further strengthen the program’s quality and flexibility. 

The current version of **"Shrine of the Lost Pathways"** represents a minimal, functional prototype focused on core combat mechanics and structure. However, there is significant room for future development, both in terms of gameplay and technical depth.

Potential expansions include:

* Story progression: Introducing a narrative where the player must escape a cursed, multi-floor dungeon, eventually facing an ancient dragon guarding the "Key of True Paths."

* Class system: Adding player classes such as Warrior, Rogue, and Mage, each with unique stats and special abilities to support varied playstyles.

* Battlefield variety: Creating different “rooms” for encounters, with unique enemies and mechanics tied to each floor (e.g., Goblin Warrens, Orc Stronghold, Dragon’s Domain).

* Special abilities and cooldowns: Implementing stamina-based skills or magic that require strategic timing rather than constant spamming.

* Leveling and loot: Allowing players to gain experience, level up, and collect “Shrine Relics” from mini-bosses that boost stats or unlock new gameplay mechanics.

These additions would transform the game from a linear battle system into a full dungeon-crawling experience with RPG depth, strategic variation, and narrative progression.