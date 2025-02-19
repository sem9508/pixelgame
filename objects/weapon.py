class Weapon:
    def __init__(self, name, weapon_type, damage, attack_range, cooldown, attack_duration):
        self.name = name
        self.type = weapon_type
        self.damage = damage
        self.attack_range = attack_range
        self.cooldown = cooldown
        self.attack_duration = attack_duration