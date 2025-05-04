from character import Enemy
from weapon import skullrender, skarrcleave, the_skull_oracle, warchiefs_mercy, bloodsong_edge, grimshard
import random

class CharacterFactory:
    _weapon_list = [skullrender, skarrcleave, the_skull_oracle, warchiefs_mercy, bloodsong_edge, grimshard]
    _enemy_name_list = ["Grothak the Chain-Breaker, the fearsome Orc Warlord", "Drokmaw the Gutlord, a sly Ogre Chieftain", "Kringlak the Red Smoke, a drunkard Goblin Saboteur"]
    
    @classmethod
    def get_weapon_list(cls):
        return cls._weapon_list.copy()
        
    @classmethod
    def get_enemy_name_list(cls):
        return cls._enemy_name_list.copy()
    
    @classmethod
    def create_enemy(cls, name=None, weapon=None) -> Enemy:
        if name is None:
            name = random.choice(cls._enemy_name_list)
        if weapon is None:
            weapon = random.choice(cls._weapon_list)
        
        return Enemy(name=name, health=100, weapon=weapon)