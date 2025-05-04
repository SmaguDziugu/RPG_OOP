from character import Player
from weapon import solrend
from factory import CharacterFactory
import sys
from datetime import datetime

def play_game():
    print("\n")
    print(r"""
                ______________
            ,===:'.,            `-._
                `:.`---.__         `-._
                    `:.     `--.         `.
                    \.        `.         `.
            (,,(,    \.         `.   ____,-`.,
        (,'     `/   \.   ,--.___`.'
    ,  ,'  ,--.  `,   \.;'         `
        `{D, {    \  :    \;
        V,,'    /  /    //
        j;;    /  ,' ,-//.    ,---.      ,
        \;'   /  ,' /  _  \  /  _  \   ,'/  
                \   `'  / \  `'  / \  `.' /   
                `.___,'   `.__,'   `.__,'    VZ

    +------------------------------------------------+
                --Shrine Of The Lost Pathways--
    +------------------------------------------------+
                    --Game Start--
    +------------------------------------------------+""")
    print("\n")
    player = Player(health=100)
    print(f"\n{player.name} begins their journey...\n")
    player.equip(solrend)
    enemy = CharacterFactory.create_enemy()
    print(f"\n{enemy.name} blocks {player.name}'s path!")

    while player.health>0 and enemy.health>0:
        print("\n")
        print("+------------------------------------------------+")
        print("Choose your action:")
        print("1. Attack")
        print("2. Defend")
        print("+------------------------------------------------+")
        print("\n")

        while True:
            choice = input("Enter your choice (1 or 2): ")
            if choice in ['1', '2']:
                break
            print("Invalid choice. Please enter '1' to Attack or '2' to Defend.")
        
        if choice == '1':
            player.attack(enemy)
        else:
            player.defend()

        if enemy.health>0:
            enemy.attack(player)

        player.health_bar.draw()
        enemy.health_bar.draw()

        input("\nPress Enter to continue...\n")

    if player.health > 0:
        save_game_result(player.name, player.health)
        print(f"\nCongratulations! {player.name} has defeated the {enemy.name}!\n")
        print(r"""
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣶⣿⣿⣿⣶⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⢟⣭⣴⣶⡦⠍⠛⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀
    ⠈⠳⣶⣤⣤⣶⣿⠿⢫⣾⣿⣿⠋⠀⠀⠀⠀⢸⣿⡟⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠈⠉⠉⠉⠁⣰⣿⣿⣿⠇⠀⢀⣀⣤⣴⣾⣧⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⡟⢠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⣠⣿⣿⣿⡟⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀
    ⠀⠀⢀⣠⣶⣿⣿⡿⠋⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⠀⠀⠀⠀
    ⠉⠛⠛⠛⠛⠛⠉⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣛⣥⣶⣆⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⠏⣥⣤⡙⢟⣫⡴⠿⠿⠿⠷⠿⣷⡀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡜⢿⡿⢃⣌⢻⣟⠛⠻⠶⠶⢶⣾⣿⡄
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⡄⣾⣿⣿⣷⡝⢿⣷⣶⣶⣦⡾⠟⠁
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣟⣛⣻⠿⠿⢧⢹⣿⣿⣿⣿⣦⡙⢷⡶⠋⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣝⠻⣿⣿⣛⠷⠌⢿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣮⣝⠻⣿⣶⣦⣤⣉⠛⠿⢿⠁⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣛⠿⢿⣧⢷⣤⡀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠛⠿⣿⣿⣿⣿⣷⡦⠉⢿⣿⡷⠦⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⡿⠋⠀⠀⠈⠀⠀⠀⠀⠀⠀
    """)
    else:
        save_game_result(enemy.name, enemy.health)
        print(f"\nGame Over! {player.name} has been defeated!")
        print(r"""
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀
    ⠀⠀⢀⡀⠀⢠⣿⡟⠿⣿⣧⣌⣉⣙⣛⣛⣋⣉⣡⣼⣿⠿⢻⣿⡄⠀⢀⡀⠀⠀
    ⠀⠀⢸⡿⢀⣾⣿⣿⣶⣌⠙⠿⣿⣿⣿⣿⣿⣿⠿⠋⣡⣶⣿⣿⣷⡀⢿⡇⠀⠀
    ⠀⠀⢸⠇⣾⣿⣿⣿⣿⣿⡆⢠⣄⠉⠛⠛⠉⣠⡄⢰⣿⣿⣿⣿⣿⣷⠸⡇⠀⠀
    ⠀⠀⠈⢠⣿⠟⢁⣤⣤⣄⣽⣄⠉⢠⣿⣿⡄⠉⣠⣯⣠⣤⣤⡈⠻⣿⡄⠁⠀⠀
    ⠀⠀⠀⣼⡏⢀⣿⣿⡿⣿⣿⡟⠀⠾⣿⣿⠷⠀⢻⣿⣿⢿⣿⣿⡀⢹⣧⠀⠀⠀
    ⠀⠀⠀⣿⣧⣀⣿⣿⣧⠈⠙⠻⢷⣦⣤⣤⣴⡶⠟⠋⠁⣼⣿⣿⣀⣼⣿⠀⠀⠀
    ⠀⠀⢸⣿⣿⣿⣿⣿⣿⣧⠈⠒⢀⣀⣤⣤⣀⡀⠒⠁⣼⣿⣿⣿⣿⣿⣿⡇⠀⠀
    ⠀⠀⠘⢿⣿⣿⣿⣿⣿⡟⢁⣴⣿⣿⣿⣿⣿⣿⣦⡈⢻⣿⣿⣿⣿⣿⡿⠃⠀⠀
    ⠀⠀⠀⠀⠈⠉⠛⠻⠿⢷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡾⠿⠟⠛⠉⠁⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """)
    return play_again()

def play_again():
    print("\n")
    print("+------------------------------------------------+")
    print("What would you like to do?")
    print("1. Play Again")
    print("2. Exit Game")
    print("+------------------------------------------------+")
    print("\n")

    while True:
        choice = input("Enter your choice (1 or 2): ")
        if choice == '1':
            return True
        elif choice == '2':
            print("\nThank you for playing Shrine Of The Lost Pathways!\n")
            print("\nFarewell, brave adventurer...\n")
            sys.exit()
        else:
            print("Invalid choice. Please enter '1' to Play Again or '2' to Exit.")

def save_game_result(winner_name, winner_health):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("game_results.txt", "a") as file:
        file.write(f"{now} | Winner: {winner_name} | Health: {winner_health}\n")

if __name__ == "__main__":
    while True:
        if not play_game():
            sys.exit()