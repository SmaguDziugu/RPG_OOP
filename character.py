from health_bar import HealthBar
from abc import ABC, abstractmethod
import random

class Character(ABC):
    def __init__(self, name: str, health: int) -> None:
        self._name = name
        self._health = health
        self._max_health = health

    @property
    def name(self):
        return self._name

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = max(0, min(value, self._max_health))
        
    @property
    def max_health(self):
        return self._max_health
        
    @abstractmethod
    def attack(self, target):
        pass

class Player(Character):
    def __init__(self, health: int) -> None:
        name = input("Enter your character's name: ")
        super().__init__(name=name, health=health)  
        self._health_bar = HealthBar(self, color="green")
        self._critical_hit_chance = 0.35
        self._damage_reduction = 0.5
        self._deflect_chance = 0.25
        self._is_defending = False
        
    @property
    def health_bar(self):
        return self._health_bar
    
    @property
    def critical_hit_chance(self):
        return self._critical_hit_chance
    
    @property
    def damage_reduction(self):
        return self._damage_reduction
    
    @property
    def deflect_chance(self):
        return self._deflect_chance
    
    @property
    def is_defending(self):
        return self._is_defending
    
    @is_defending.setter
    def is_defending(self, value):
        self._is_defending = value
        
    def equip(self, weapon) -> None:
        self._weapon = weapon
        print(f"\n{self.name} unsheathed {self._weapon.name} - {self._weapon.description}!\n")

    @property
    def weapon(self):
        return self._weapon

    def attack(self, target):
        is_critical = random.random() < self._critical_hit_chance
        if is_critical:
            damage_dealt = self.weapon.damage * 2
            message = f"\n{self.name} dealt {damage_dealt} damage to {target.name} with {self.weapon.name} (CRITICAL HIT!)\n"
        else:
            damage_dealt = self.weapon.damage
            message = f"\n{self.name} dealt {damage_dealt} damage to {target.name} with {self.weapon.name}\n"
        target.health -= damage_dealt
        target.health_bar.update()
        print(message)

        if isinstance(target, Enemy) and target.health > 0:
            target.taunt()

    def defend(self):
        self._is_defending = True
        print(f"\n{self.name} takes a defensive stance, reducing incoming damage by 50%\n")

class Enemy(Character):
    def __init__(self, name: str, health: int, weapon) -> None:
        super().__init__(name=name, health=health) 
        self._weapon = weapon
        self._health_bar = HealthBar(self, color="red")
        self._critical_hit_chance = 0.15
        self._instant_kill_chance = 0.03

        self._high_health_taunts = [
            "Mmm. Spicy. Do it again.",
            "I've been kissed harder by ghosts.",
            "If that was your opening move, I might live forever.",
            "You sure you're not just here to tickle me to death?",
            "Was that an attack, or are we playing tag?"
        ]
        
        self._medium_health_taunts = [
            "Oh, you're trying now? How adorable.",
            "You're sweating. I'm thriving.",
            "This is your best? I was hoping for a challenge, not a dance partner.",
            "Keep going, champ—maybe in another hour I'll notice.",
            "You're hitting harder, sure… but so does rain."
        ]
        
        self._low_health_taunts = [
            "You've almost won! Better hope I stay dead this time.",
            "Bleeding? No no—I'm leaking ambition.",
            "If I die, I'm haunting your dreams... and your love life.",
            "Go on then, hero. Finish it. Make your legend slightly less boring.",
            "Strike me down and I shall become... a dramatic footnote in your tragic little story."
        ]
        
    @property
    def health_bar(self):
        return self._health_bar
    
    @property
    def critical_hit_chance(self):
        return self._critical_hit_chance
    
    @property
    def instant_kill_chance(self):
        return self._instant_kill_chance
    
    @property
    def weapon(self):
        return self._weapon
    
    @weapon.setter
    def weapon(self, weapon):
        self._weapon = weapon

    def taunt(self):
        health_percentage = (self.health / self.max_health) * 100
        
        if health_percentage > 70:
            taunt = random.choice(self._high_health_taunts)
            print(f"\033[93m{self.name}: {taunt}\033[0m")
        elif health_percentage > 30:
            taunt = random.choice(self._medium_health_taunts)
            print(f"\033[38;5;208m{self.name}: \033[1m{taunt}\033[0m")
        else:
            taunt = random.choice(self._low_health_taunts)
            print(f"\033[91m{self.name}: \033[1m{taunt}\033[0m")

    def attack(self, target):
        if random.random() < self._instant_kill_chance:
            target.health = 0
            target.health_bar.update()
            print(f"\n\033[91m{self.name} performs a FATAL BLOW! {target.name} is instantly defeated!\033[0m\n")
            return

        is_critical = random.random() < self._critical_hit_chance
        if is_critical:
            damage_dealt = self.weapon.damage * 1.5
            message = f"\n{self.name} dealt {damage_dealt} damage to {target.name} with {self.weapon.name} (CRITICAL HIT!)\n"
        else:
            damage_dealt = self.weapon.damage
            message = f"\n{self.name} dealt {damage_dealt} damage to {target.name} with {self.weapon.name}\n"

        if isinstance(target, Player) and target.is_defending:
            if random.random() < target.deflect_chance:
                message = f"\n{target.name} perfectly deflected {self.name}'s attack!\n"
                print(message)
                target.is_defending = False
                return
            original_damage = damage_dealt
            damage_dealt *= (1 - target.damage_reduction)
            original_damage_rounded = round(original_damage, 1)
            damage_dealt_rounded = round(damage_dealt, 1)
            message += f" (Damage reduced by 50% from {original_damage_rounded} to {damage_dealt_rounded}.)\n"
            target.is_defending = False

        target.health -= damage_dealt
        target.health_bar.update()
        print(message)