from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

print("\n\n")
print("NAME               HP                                  MP")
print("                    _________________________          __________")
print(bcolors.BOLD + "Valos:   " +
      "460/460   |" + bcolors.OKGREEN + "█████████████████████████" +
      bcolors.ENDC + bcolors.BOLD + "|  65/65 |" + bcolors.OKBLUE + "██████████" + bcolors.ENDC + "|")

print("NAME               HP                                  MP")
print("                    _________________________          __________")
print("Valos:   460/460   |                         |  65/65 |          |")

print("NAME               HP                                  MP")
print("                    _________________________          __________")
print("Valos:   460/460   |                         |  65/65 |          |")

print("\n\n")

# Create black magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
metheor = Spell("Metheor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create white magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

# Create items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item( "MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_magic = [fire, thunder, blizzard, metheor, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]
# Instanciate people
player = Person(460, 65, 60, 34, player_magic, player_items)
enemy = Person(915, 65, 45, 35, [], [])

running = True


print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("===========================")
    player.choose_action()
    choice = input("Choose action:")
    index = int(choice) - 1

# Attack
    if index == 0:
        dmg = player.generate_damage()
        enemy.take_damage(dmg)
        print("You attacked for", dmg, "points of damage. Enemy HP:", enemy.get_hp())

# Magic
    elif index == 1:
        player.choose_magic()
        print("Current MP:", bcolors.OKBLUE + str(player.get_mp()) + bcolors.ENDC)
        magic_choice = int(input("Choose a spell:")) - 1

        if magic_choice == -1:
            continue

        spell = player.magic[magic_choice]
        magic_dmg = spell.generate_damage()
        current_mp = player.get_mp()

        if spell.cost > current_mp:
            print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
            continue

        player.reduce_mp(spell.cost)

        if spell.type == "white":
            player.heal(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " heals for ", str(magic_dmg), "HP" + bcolors.ENDC)
        elif spell.type == "black":
            enemy.take_damage(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage." + bcolors.ENDC)

# Items
    elif index == 2:
        player.choose_item()
        item_choice = int(input("Choose item: ")) - 1

        if item_choice == -1:
            continue

        iitem = player.items[item_choice]["item"]

        if player.items[item_choice]["quantity"] == 0:
            print(bcolors.FAIL + "\nNone left..." + bcolors.ENDC)
            continue

        player.items[item_choice]["quantity"] -= 1

        if iitem.type == "potion":
            player.heal(iitem.prop)
            print(bcolors.OKGREEN + "\n" + iitem.name, "heals for", str(iitem.prop), "HP" + bcolors.ENDC)
        elif iitem.type == "elixer":
            player.hp = player.max_hp
            player.mp = player.max_mp
            print(bcolors.OKGREEN + "\n" + iitem.name, "fully restores HP/MP" + bcolors.ENDC)
        elif iitem.type == "attack":
            enemy.take_damage(iitem.prop)
            print(bcolors.FAIL + "\n" + iitem.name + " deals " + str(iitem.prop) + " points of damage." + bcolors.ENDC)


    enemy_choice = 1
    enemy_dmg = enemy.generate_damage()
    player.take_damage(enemy_dmg)
    print("Enemy attacks for", enemy_dmg, "points of damage. Player HP", player.get_hp(), ".")

    print("----------------------------------")
    print("Enemy HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC)
    print("Your HP:", bcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.get_max_hp()) + bcolors.ENDC)
    print("Your MP", bcolors.OKBLUE + str(player.get_mp()) + "/" + str(player.get_max_mp()) + bcolors.ENDC)


    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif player.get_hp() ==0:
        print(bcolors.FAIL + "Your enemy has defeated you!" + bcolors.ENDC)
        running = False