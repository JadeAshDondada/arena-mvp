class FighterEntity:
    def __init__(self, name: str, hp: int, attack: int):
        self.name = name
        self.hp = hp
        self.attack_power = attack

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, dmg: int):
        self.hp -= dmg
       # print(f"{self.name} получает {dmg} урона. Осталось HP: {self.hp}")  !!закомментировал вывод статуса персонажей

    def attack(self, other: 'Fighter'):
       # print(f"{self.name} атакует {other.name} на {self.attack_power} урона!")
        other.take_damage(self.attack_power)