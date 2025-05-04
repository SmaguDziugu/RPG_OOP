class Weapon:
    def __init__(self, name: str, damage: int, description: str) -> None:
        self._name = name
        self._damage = damage
        self._description = description

    @property
    def name(self):
        return self._name
        
    @property
    def damage(self):
        return self._damage
        
    @property
    def description(self):
        return self._description

skullrender = Weapon(name="Skullrender",
                    damage=13,
                    description="a brutal axe that crushes helmets and heads alike")

warchiefs_mercy = Weapon(name="Warchief's Mercy",
                    damage=9,
                    description="a brutal greatsword that delivers only one kindness: a quick death to those who kneel")

bloodsong_edge = Weapon(name="Bloodsong Edge",
                        damage=7,
                        description="a cursed sword that sings louder with each soul it takes")

skarrcleave = Weapon(name="Skarrcleave",
                     damage=11,
                     description="a brutal war axe that split a titan in two")

the_skull_oracle = Weapon(name="The Skull Oracle",
                          damage=15,
                          description="a mace inscribed with death runes, said to speak prophecy in blood")

grimshard = Weapon(name="Grimshard",
                   damage=14,
                   description="notched with obsidian, each strike leaves splinters in the soul")

solrend = Weapon(name="Solrend",
                 damage=10,
                 description="Forged from the First Sun's last light, its embered blade burns truth into shadow. With each righteous strike, it blazes brighter—bound to oath, fire, and the fearless.")