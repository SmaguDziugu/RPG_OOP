import unittest
from unittest.mock import patch, mock_open, MagicMock
from character import Player, Enemy
from weapon import Weapon, solrend, skullrender, skarrcleave, the_skull_oracle, warchiefs_mercy, bloodsong_edge, grimshard
from factory import CharacterFactory
from health_bar import HealthBar
from main import save_game_result, play_game
from io import StringIO
import os
import sys

class TestPlayerHealth(unittest.TestCase):

    @patch('builtins.input', return_value='TestPlayer')
    def test_player_starts_with_full_health(self, mock_input):
        player = Player(health=100)
        self.assertEqual(player.health, player.max_health, 'Player health should be equal to max health at initialization')
        self.assertEqual(player.health, 100, 'Player should start with 100 health when created with health=100')
    
    @patch('builtins.input', return_value='TestPlayer')
    def test_player_health_cannot_exceed_max_health(self, mock_input):
        player = Player(health=100)
        player.health = 150
        self.assertEqual(player.health, 100, 'Player health should not exceed max_health (100)')
    
    @patch('builtins.input', return_value='TestPlayer')
    def test_player_health_bar_initialized_correctly(self, mock_input):
        player = Player(health=100)
        self.assertEqual(player.health_bar.entity, player, 'Health bar entity should reference the player')
        self.assertEqual(player.health_bar.color, "\033[92m", 'Player health bar color should be green (\\033[92m)')
        
    @patch('builtins.input', return_value='TestPlayer')
    def test_player_health_cannot_go_below_zero(self, mock_input):
        player = Player(health=100)
        player.health -= 150
        self.assertEqual(player.health, 0, 'Player health should not go below zero')

class TestPlayerCombatMechanics(unittest.TestCase):
    
    @patch('builtins.input', return_value='TestPlayer')
    def test_player_name_input(self, mock_input):
        player = Player(health=100)
        self.assertEqual(player.name, 'TestPlayer', 'Player name should be set to the value provided by input()')

    @patch('builtins.input', return_value='TestPlayer')
    @patch('builtins.print')
    def test_player_defend_flag_set(self, mock_print, mock_input):
        player = Player(health=100)
        player.defend()
        self.assertTrue(player.is_defending, 'Player.is_defending should be True after calling defend()')

    @patch('builtins.input', return_value='TestPlayer')
    @patch('builtins.print')
    def test_player_takes_reduced_damage_when_defending(self, mock_print, mock_input):
        player = Player(health=100)
        test_weapon = Weapon(name="TestWeapon", damage=20, description="A test weapon")
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        player.defend()
        with patch('random.random', return_value=0.5):
            enemy.attack(player)
        self.assertEqual(player.health, 90, 'Player should take half damage (10) when defending')

    @patch('builtins.input', return_value='TestPlayer')
    @patch('builtins.print')
    def test_defense_resets_after_being_hit(self, mock_print, mock_input):
        player = Player(health=100)
        test_weapon = Weapon(name="TestWeapon", damage=20, description="A test weapon")
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        player.defend()
        with patch('random.random', return_value=0.5):
            enemy.attack(player)
        self.assertFalse(player.is_defending, 'Player.is_defending should be False after being attacked')

    @patch('builtins.input', return_value='TestPlayer')
    @patch('builtins.print')
    def test_defense_persists_until_hit(self, mock_print, mock_input):
        player = Player(health=100)
        player.defend()
        self.assertTrue(player.is_defending, 'Defense flag should remain True until player is hit')
        player.health -= 5
        self.assertTrue(player.is_defending, 'Defense flag should remain True when taking damage not from enemy attack')

    @patch('builtins.input', return_value='TestPlayer')
    @patch('builtins.print')
    def test_player_critical_hit_chance(self, mock_print, mock_input):
        player = Player(health=100)
        self.assertEqual(player.critical_hit_chance, 0.35, 'Player critical hit chance should be 35%')
    
    @patch('builtins.input', return_value='TestPlayer')
    @patch('builtins.print')
    def test_player_critical_hit_doubles_damage(self, mock_print, mock_input):
        player = Player(health=100)
        test_weapon = Weapon(name="TestWeapon", damage=10, description="A test weapon")
        player.equip(test_weapon)
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        with patch('random.random', return_value=0.1):
            player.attack(enemy)
            self.assertEqual(enemy._health, 80, 'Critical hit should do double damage (20)')
    
    @patch('builtins.input', return_value='TestPlayer')
    @patch('builtins.print')
    def test_player_non_critical_hit(self, mock_print, mock_input):
        player = Player(health=100)
        test_weapon = Weapon(name="TestWeapon", damage=10, description="A test weapon")
        player.equip(test_weapon)
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        with patch('random.random', return_value=0.7):
            player.attack(enemy)
            self.assertEqual(enemy._health, 90, 'Normal hit should do standard damage (10)')
    
class TestEnemyHealth(unittest.TestCase):
    
    def test_enemy_starts_with_full_health(self):
        test_weapon = Weapon(name="TestWeapon", damage=20, description="A test weapon")
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        self.assertEqual(enemy.health, enemy.max_health, 'Enemy health should be equal to max health at initialization')
        self.assertEqual(enemy.health, 100, 'Enemy should start with 100 health when created with health=100')
    
    def test_enemy_health_cannot_exceed_max_health(self):
        test_weapon = Weapon(name="TestWeapon", damage=20, description="A test weapon")
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        enemy.health = 150
        self.assertEqual(enemy.health, 100, 'Enemy health should not exceed max_health (100)')
    
    def test_enemy_health_cannot_go_below_zero(self):
        test_weapon = Weapon(name="TestWeapon", damage=20, description="A test weapon")
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        enemy.health -= 150
        self.assertEqual(enemy.health, 0, 'Enemy health should not go below zero')
        
    def test_enemy_health_bar_initialized_correctly(self):
        test_weapon = Weapon(name="TestWeapon", damage=20, description="A test weapon")
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        self.assertEqual(enemy.health_bar.entity, enemy, 'Health bar entity should reference the enemy')
        self.assertEqual(enemy.health_bar.color, "\033[91m", 'Enemy health bar color should be red (\\033[91m)')

class TestEnemyCombatMechanics(unittest.TestCase):
    
    @patch('builtins.input', return_value='TestPlayer')
    @patch('builtins.print')
    def test_enemy_critical_hit(self, mock_print, mock_input):
        player = Player(health=100)
        test_weapon = Weapon(name="TestWeapon", damage=20, description="A test weapon")
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        with patch('random.random', side_effect=[0.9, 0.1]):
            enemy.attack(player)
        self.assertEqual(player.health, 70, 'Player should take critical damage (30) from enemy critical hit')
        
    @patch('builtins.input', return_value='TestPlayer')
    @patch('builtins.print')
    def test_enemy_instant_kill(self, mock_print, mock_input):
        player = Player(health=100)
        test_weapon = Weapon(name="TestWeapon", damage=20, description="A test weapon")
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        with patch('random.random', return_value=0.01):
            enemy.attack(player)
        self.assertEqual(player.health, 0, 'Player health should be 0 after enemy instant kill')
        
    @patch('builtins.input', return_value='TestPlayer')
    @patch('builtins.print')
    def test_enemy_normal_attack(self, mock_print, mock_input):
        player = Player(health=100)
        test_weapon = Weapon(name="TestWeapon", damage=15, description="A test weapon")
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        with patch('random.random', side_effect=[0.5, 0.5]): 
            enemy.attack(player)
        self.assertEqual(player.health, 85, 'Player should take normal damage (15) from enemy attack')
        
    @patch('builtins.input', return_value='TestPlayer')
    @patch('builtins.print')
    def test_enemy_damage_reduction(self, mock_print, mock_input):
        player = Player(health=100)
        test_weapon = Weapon(name="TestWeapon", damage=20, description="A test weapon")
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        player.defend()
        with patch('random.random', side_effect=[0.9, 0.1, 0.5]):
            enemy.attack(player)
        self.assertEqual(player.health, 85, 'Player should take reduced critical damage (15) when defending')

    @patch('builtins.input', return_value='TestPlayer')
    @patch('builtins.print')
    def test_damage_deflection_when_implemented(self, mock_print, mock_input):
        player = Player(health=100)
        test_weapon = Weapon(name="TestWeapon", damage=20, description="A test weapon")
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        original_health = player.health
        player.defend()
        self.assertEqual(player.deflect_chance, 0.25, 'Player deflect_chance should be 25%')
        with patch('random.random', side_effect=[0.9, 0.5, 0.05]):
            enemy.attack(player)
            self.assertEqual(player.health, original_health, 'Player should take no damage when deflection occurs')
        
    @patch('builtins.input', return_value='TestPlayer')
    @patch('builtins.print')
    def test_enemy_attack_damage_rounding(self, mock_print, mock_input):
        player = Player(health=100)
        test_weapon = Weapon(name="TestWeapon", damage=17, description="A test weapon")
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        player.defend()
        with patch('random.random', side_effect=[0.9, 0.5, 0.5]):
            enemy.attack(player)
        self.assertEqual(player.health, 91.5, 'Damage calculation should preserve decimals (8.5)')

    @patch('builtins.print')
    def test_enemy_high_health_taunt(self, mock_print):
        test_weapon = Weapon(name="TestWeapon", damage=10, description="A test weapon")
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        with patch('random.choice', return_value="I've been kissed harder by ghosts."):
            enemy.taunt()
            mock_print.assert_called_once()
            self.assertIn("\033[93m", mock_print.call_args[0][0])
    
    @patch('builtins.print')
    def test_enemy_medium_health_taunt(self, mock_print):
        test_weapon = Weapon(name="TestWeapon", damage=10, description="A test weapon")
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        enemy.health = 50
        with patch('random.choice', return_value="You're sweating. I'm thriving."):
            enemy.taunt()
            mock_print.assert_called_once()
            self.assertIn("\033[38;5;208m", mock_print.call_args[0][0])
    
    @patch('builtins.print')
    def test_enemy_low_health_taunt(self, mock_print):
        test_weapon = Weapon(name="TestWeapon", damage=10, description="A test weapon")
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        enemy.health = 20 
        with patch('random.choice', return_value="Bleeding? No no—I'm leaking ambition."):
            enemy.taunt()
            mock_print.assert_called_once()
            self.assertIn("\033[91m", mock_print.call_args[0][0])

class TestWeaponFunctionality(unittest.TestCase):
    
    @patch('builtins.input', return_value='TestPlayer')
    def test_weapon_properties_accessible(self, mock_input):
        test_weapon = Weapon(name="TestWeapon", damage=15, description="A test weapon")
        self.assertEqual(test_weapon.name, "TestWeapon", 'Weapon name should be accessible through the name property')
        self.assertEqual(test_weapon.damage, 15, 'Weapon damage should be accessible through the damage property')
        self.assertEqual(test_weapon.description, "A test weapon", 'Weapon description should be accessible through the description property')
        
    @patch('builtins.input', return_value='TestPlayer')
    @patch('builtins.print')
    def test_player_can_equip_weapon(self, mock_print, mock_input):
        player = Player(health=100)
        test_weapon = Weapon(name="TestWeapon", damage=15, description="A test weapon")
        player.equip(test_weapon)
        self.assertEqual(player.weapon, test_weapon, 'Player should have the equipped weapon accessible via the weapon property')

    @patch('builtins.input', return_value='TestPlayer')
    @patch('builtins.print')
    def test_player_weapon_persists(self, mock_print, mock_input):
        player = Player(health=100)
        player.equip(solrend)
        self.assertEqual(player.weapon.name, "Solrend", 'Players weapon name should persist after being equipped')
        self.assertEqual(player.weapon.damage, 10, 'Players weapon damage should persist after being equipped')
        self.assertEqual(player.weapon.description, "Forged from the First Sun's last light, its embered blade burns truth into shadow. With each righteous strike, it blazes brighter—bound to oath, fire, and the fearless.", 
                         'Players weapon description should persist after being equipped')
        
    @patch('builtins.input', return_value='TestPlayer')
    @patch('builtins.print')
    def test_player_attack_uses_weapon_damage(self, mock_print, mock_input):
        player = Player(health=100)
        test_weapon = Weapon(name="TestWeapon", damage=10, description="A test weapon")
        player.equip(test_weapon)
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        initial_enemy_health = enemy.health
        with patch('random.random', return_value=0.4):
            player.attack(enemy)   
            expected_enemy_health = initial_enemy_health - test_weapon.damage
            self.assertEqual(enemy.health, expected_enemy_health, 'Enemy health should be reduced by weapon damage (10) (expected: 90)')

    @patch('builtins.input', return_value='TestPlayer')
    @patch('builtins.print')
    def test_critical_hit_doubles_weapon_damage(self, mock_print, mock_input):
        player = Player(health=100)
        test_weapon = Weapon(name="TestWeapon", damage=10, description="A test weapon")
        player.equip(test_weapon)
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        initial_enemy_health = enemy.health
        with patch('random.random', return_value=0.1):
            player.attack(enemy)
            expected_enemy_health = initial_enemy_health - (test_weapon.damage * 2)
            self.assertEqual(enemy.health, expected_enemy_health, 'Critical hit should double weapon damage (20) (expected: 80')

    @patch('builtins.input', return_value='TestPlayer')
    def test_enemy_can_hold_weapon(self, mock_input):
        test_weapon = Weapon(name="TestWeapon", damage=15, description="A test weapon")
        enemy = Enemy(name="Test Enemy", health=100, weapon=test_weapon)
        self.assertEqual(enemy.weapon, test_weapon, 'Enemy should have the assigned weapon accessible via the weapon property')
        self.assertEqual(enemy.weapon.damage, 15, 'Enemy weapon damage should be accessible and match the assigned value')

class TestCharacterFactory(unittest.TestCase):
    
    def test_create_enemy_returns_enemy_instance(self):
        enemy = CharacterFactory.create_enemy()
        self.assertIsInstance(enemy, Enemy, "Factory should return an Enemy instance")
    
    def test_create_enemy_with_default_params(self):
        enemy = CharacterFactory.create_enemy()

        self.assertIsNotNone(enemy.name, "Enemy should have a name")
        self.assertTrue(isinstance(enemy.name, str), "Enemy name should be a string")
        self.assertTrue(len(enemy.name) > 0, "Enemy name should not be empty")
        
        self.assertIsNotNone(enemy.weapon, "Enemy should have a weapon")
        self.assertIsInstance(enemy.weapon, Weapon, "Enemy weapon should be an instance of Weapon class")
        
        self.assertEqual(enemy.health, 100, "Enemy should have 100 health")
        self.assertEqual(enemy.health, enemy.max_health, "Enemy health should equal max_health")
    
    def test_create_enemy_with_specific_name(self):
        test_name = "Test Enemy Name"
        enemy = CharacterFactory.create_enemy(name=test_name)
        self.assertEqual(enemy.name, test_name, "Enemy should have the specified name")
    
    def test_create_enemy_with_specific_weapon(self):
        test_weapon = skullrender
        enemy = CharacterFactory.create_enemy(weapon=test_weapon)
        self.assertEqual(enemy.weapon, test_weapon, "Enemy should have the specified weapon")
    
    def test_create_enemy_with_specific_name_and_weapon(self):
        test_name = "Test Enemy Name"
        test_weapon = grimshard
        enemy = CharacterFactory.create_enemy(name=test_name, weapon=test_weapon)
        self.assertEqual(enemy.name, test_name, "Enemy should have the specified name")
        self.assertEqual(enemy.weapon, test_weapon, "Enemy should have the specified weapon")
    
    def test_weapon_list_contents(self):
        weapon_list = CharacterFactory.get_weapon_list()
        
        expected_weapons = [skullrender, skarrcleave, the_skull_oracle, warchiefs_mercy, bloodsong_edge, grimshard]
        for weapon in expected_weapons:
            self.assertIn(weapon, weapon_list, f"Weapon list should contain {weapon.name}")
            
        self.assertEqual(len(weapon_list), len(expected_weapons), "Weapon list should contain exactly the expected weapons")
    
    def test_enemy_name_list_contents(self):
        name_list = CharacterFactory.get_enemy_name_list()
        
        expected_names = [
            "Grothak the Chain-Breaker, the fearsome Orc Warlord",
            "Drokmaw the Gutlord, a sly Ogre Chieftain",
            "Kringlak the Red Smoke, a drunkard Goblin Saboteur"
        ]   
        for name in expected_names:
            self.assertIn(name, name_list, f"Enemy name list should contain '{name}'")
        self.assertEqual(len(name_list), len(expected_names), "Enemy name list should contain exactly the expected names")
    
    @patch('random.choice')
    def test_random_selection(self, mock_choice):
        mock_choice.side_effect = ["Grothak the Chain-Breaker, the fearsome Orc Warlord", skullrender]
        enemy = CharacterFactory.create_enemy()
        self.assertEqual(mock_choice.call_count, 2, "random.choice should be called twice")
        self.assertEqual(enemy.name, "Grothak the Chain-Breaker, the fearsome Orc Warlord")
        self.assertEqual(enemy.weapon, skullrender)
    
    def test_enemy_health_bar(self):
        enemy = CharacterFactory.create_enemy()
        self.assertIsNotNone(enemy.health_bar, "Enemy should have a health bar")
        self.assertEqual(enemy.health_bar.entity, enemy, "Health bar entity should reference the enemy")
        self.assertEqual(enemy.health_bar.color, "\033[91m", "Enemy health bar color should be red")
    
    def test_enemy_combat_properties(self):
        enemy = CharacterFactory.create_enemy()
        self.assertEqual(enemy.critical_hit_chance, 0.15, "Enemy should have 15% critical hit chance")
        self.assertEqual(enemy.instant_kill_chance, 0.03, "Enemy should have 3% instant kill chance")

class TestHealthBar(unittest.TestCase):
    
    def test_health_bar_initialization(self):
        mock_entity = MagicMock()
        mock_entity.max_health = 100
        mock_entity.health = 100
        mock_entity.name = "Test Entity"
        health_bar = HealthBar(mock_entity, length=20, is_colored=True, color="red")
        self.assertEqual(health_bar.entity, mock_entity, 'Health bar should reference the provided entity')
        self.assertEqual(health_bar.length, 20, 'Health bar length should match the provided length')
        self.assertTrue(health_bar.is_colored, 'Health bar is_colored flag should match the provided value')
        self.assertEqual(health_bar.color, "\033[91m", 'Health bar color should be set to the correct ANSI code')
    
    def test_health_bar_update(self):
        mock_entity = MagicMock()
        mock_entity.max_health = 100
        mock_entity.health = 100
        mock_entity.name = "Test Entity"
        
        health_bar = HealthBar(mock_entity)
        mock_entity.health = 50
        health_bar.update()
        self.assertEqual(health_bar._current_value, 50, 'Health bar update should reflect the current entity health')
    
    @patch('builtins.print')
    def test_health_bar_drawing_full_health(self, mock_print):
        mock_entity = MagicMock()
        mock_entity.max_health = 100
        mock_entity.health = 100
        mock_entity.name = "Test Entity"
        health_bar = HealthBar(mock_entity, length=10)
        health_bar.draw()
        self.assertEqual(mock_print.call_count, 2, 'Health bar draw should print two lines (stats and bar)')
    
    @patch('builtins.print')
    def test_health_bar_drawing_partial_health(self, mock_print):
        mock_entity = MagicMock()
        mock_entity.max_health = 100
        mock_entity.health = 50
        mock_entity.name = "Test Entity"
        health_bar = HealthBar(mock_entity, length=10)
        health_bar.draw()
        mock_print.assert_any_call("Test Entity's HEALTH: 50/100")
    
    @patch('builtins.print')
    def test_health_bar_drawing_no_health(self, mock_print):
        mock_entity = MagicMock()
        mock_entity.max_health = 100
        mock_entity.health = 0
        mock_entity.name = "Test Entity"
        health_bar = HealthBar(mock_entity, length=10)
        health_bar.draw()
        mock_print.assert_any_call("Test Entity's HEALTH: 0/100")


class TestInputValidation(unittest.TestCase):
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_invalid_then_valid_input(self, mock_print, mock_input):
        mock_input.side_effect = ['3', '1']
        def get_player_choice():
            while True:
                choice = input("Enter your choice (1 or 2): ")
                if choice in ['1', '2']:
                    return choice
                print("Invalid choice. Please enter '1' to Attack or '2' to Defend.")
        
        result = get_player_choice()
        self.assertEqual(result, '1', 'Function should return valid input after receiving invalid input')
        mock_print.assert_called_once_with("Invalid choice. Please enter '1' to Attack or '2' to Defend.")

if __name__ == '__main__':
    unittest.main()