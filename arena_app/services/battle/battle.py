from models.fighterEntity import FighterEntity


class BattleManager:
    def __init__(self, fighter1: FighterEntity, fighter2: FighterEntity):
        self.f1 = fighter1
        self.f2 = fighter2
        self.turn_attacker = self.f1
        self.turn_defender = self.f2
        self.finished = False
        self.winner = None

    def next_turn(self):
        # Если битва уже закончилась — просто возвращаем текущее состояние
        if self.finished:
            return {
                "message": "Битва уже завершена",
                "attacker": None,
                "defender": None,
                "f1_hp": self.f1.hp,
                "f2_hp": self.f2.hp,
                "finished": True,
                "winner": self.winner.name if self.winner else None
            }

        # Текущий атакующий наносит удар
        self.turn_attacker.attack(self.turn_defender)

        # Проверяем, жив ли защитник
        if not self.turn_defender.is_alive():
            self.finished = True
            self.winner = self.turn_attacker
            return {
                "message": "Битва окончена",
                "attacker": self.turn_attacker.name,
                "defender": self.turn_defender.name,
                "f1_hp": self.f1.hp,
                "f2_hp": self.f2.hp,
                "finished": True,
                "winner": self.winner.name
            }

        # Если оба живы — меняем местами роли на следующий ход
        self.turn_attacker, self.turn_defender = self.turn_defender, self.turn_attacker

        return {
            "message": "Ход сделан",
            "attacker": self.turn_attacker.name,  # кто будет атаковать на следующем вызове next_turn
            "defender": self.turn_defender.name,  # кто будет защищаться
            "f1_hp": self.f1.hp,
            "f2_hp": self.f2.hp,
            "finished": False,
            "winner": None
        }