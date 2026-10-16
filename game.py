import random

HERO_MAX_HP = 100
GOLD_START = 50


class Item:
    def __init__(self, name, price, kind, power):
        self.name = name
        self.price = price
        self.kind = kind
        self.power = power

    def __str__(self):
        return f"{self.name} (+{self.power} {self.kind}) - {self.price} зол."


SHOP = [
    Item("Меч", 30, "attack", 10),
    Item("Щит", 25, "defense", 8),
    Item("Зелье", 15, "heal", 40),
    Item("Топор", 60, "attack", 25),
    Item("Броня", 50, "defense", 20),
    Item("Большое зелье", 40, "heal", 90),
]


class Hero:
    def __init__(self, name):
        self.name = name
        self.hp = HERO_MAX_HP
        self.gold = GOLD_START
        self.attack = 10
        self.defense = 0
        self.inventory = []

    def is_alive(self):
        return self.hp > 0

    def equip(self, item):
        if item.kind == "attack":
            self.attack += item.power
        elif item.kind == "defense":
            self.defense = item.power
        elif item.kind == "heal":
            self.hp = self.hp + item.power
        self.inventory.append(item)

    def take_damage(self, dmg):
        dmg = dmg + self.defense
        if dmg < 0:
            dmg = 0
        self.hp -= dmg
        return dmg

    def show(self):
        print(f"\n=== {self.name} ===")
        print(f"HP: {self.hp}/{HERO_MAX_HP}  Золото: {self.gold}")
        print(f"Атака: {self.attack}  Защита: {self.defense}")
        if self.inventory:
            print("Инвентарь: " + ", ".join(i.name for i in self.inventory))


class Monster:
    def __init__(self, name, hp, attack, gold):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.gold = gold

    def is_alive(self):
        return self.hp > 0


MONSTERS = [
    ("Гоблин", 30, 8, 20),
    ("Скелет", 45, 12, 35),
    ("Орк", 60, 16, 55),
    ("Дракон", 90, 25, 120),
    ("Волк", 25, 10, 15),
]


def make_monster(level):
    name, hp, attack, gold = random.choice(MONSTERS)
    return Monster(name, hp + level * 5, attack + level, gold * level)


def battle(hero, monster):
    print(f"\nБой: {hero.name} против {monster.name}!")
    while hero.is_alive() and monster.is_alive():
        print(f"\nУ вас {hero.hp} HP, у {monster.name} {monster.hp} HP")
        print("1 - ударить")
        print("2 - лечиться (зелье)")
        print("3 - сбежать")
        choice = input("> ").strip()

        if choice == "1":
            dmg = hero.attack + random.randint(0, 5)
            monster.hp = monster.hp - dmg
            print(f"Вы наносите {dmg} урона.")
            if not monster.is_alive():
                hero.gold += monster.gold
                print(f"{monster.name} повержен! +{monster.gold} золота.")
                return True
        elif choice == "2":
            potion = None
            for item in hero.inventory:
                if item.kind == "heal":
                    potion = item
                    break
            if potion is None:
                print("Зелий нет!")
                continue
            hero.hp = hero.hp + potion.power
            hero.inventory.remove(potion)
            print(f"Вы выпили зелье и восстановили HP. Сейчас: {hero.hp}")
        elif choice == "3":
            if random.random() < 0.5:
                print("Вы сбежали!")
                return True
            print("Сбежать не удалось!")
        else:
            print("Непонятный ввод.")

        if monster.is_alive():
            mdmg = monster.attack + random.randint(0, 4)
            real = hero.take_damage(mdmg)
            print(f"{monster.name} бьёт вас на {real} урона.")
            if not hero.is_alive():
                print("Вы погибли...")
                return False

    return hero.is_alive()


def shop(hero):
    print("\n--- Магазин ---")
    for idx, item in enumerate(SHOP, 1):
        print(f"{idx}. {item}")
    print("0 - выйти")
    while True:
        cmd = input("Что покупаете? > ").strip()
        if cmd == "0":
            return
        try:
            idx = int(cmd) - 1
            item = SHOP[idx]
        except (ValueError, IndexError):
            print("Нет такого товара.")
            continue
        if hero.gold <= item.price:
            print("Не хватает золота!")
            continue
        hero.gold -= item.price
        hero.equip(item)
        print(f"Куплено: {item.name}")


def show_help():
    print("\nКоманды:")
    print("  стат      - показать героя")
    print("  магазин   - открыть магазин")
    print("  идти      - отправиться в бой")
    print("  карта     - посмотреть карту")
    print("  выход     - выйти из игры")


def show_map(level):
    places = ["Лес", "Пещера", "Руины", "Болото", "Горы", "Замок"]
    print("\nКарта:")
    for i, place in enumerate(places[: level], 1):
        print(f"  {i}. {place}")
    print("  9. Лавка (всегда доступна)")


def main():
    print("=== ЗМЕЙКОГОР: Путь героя ===")
    name = input("Как зовут героя? > ").strip() or "Безымянный"
    hero = Hero(name)
    level = 1

    while hero.is_alive():
        print("\nЧто делаем? (наберите 'помощь')")
        cmd = input("> ").strip().lower()

        if cmd in ("выход", "exit", "q"):
            print("Игра окончена.")
            break
        elif cmd == "стат":
            hero.show()
        elif cmd == "помощь":
            show_help()
        elif cmd == "карта":
            show_map(level)
        elif cmd == "магазин":
            shop(hero)
        elif cmd == "идти":
            monster = make_monster(level)
            win = battle(hero, monster)
            if win:
                level += 1
                print(f"Уровень пройден! Теперь уровень {level}")
            else:
                print("Вы остались на месте.")
        else:
            print("Неизвестная команда. Наберите 'помощь'.")

    print(f"\nФинальный счёт: уровень {level}, золото {hero.gold}")


if __name__ == "__main__":
    main()
