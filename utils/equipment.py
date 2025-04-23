def update_equipment(level):
    """
    Zwraca nazwę miecza i zbroi w zależności od poziomu gracza.
    """
    weapon_tiers = [
        "Drewniany Miecz",
        "Żelazny Miecz",
        "Stalowy Miecz",
        "Miecz Wojownika",
        "Miecz Króla",
        "Miecz Legendarny"
    ]

    armor_tiers = [
        "Lniana Zbroja",
        "Skórzana Zbroja",
        "Żelazna Zbroja",
        "Zbroja Rycerska",
        "Zbroja Królewska",
        "Zbroja Nieśmiertelnych"
    ]

    index = min(level // 5, len(weapon_tiers) - 1)
    return weapon_tiers[index], armor_tiers[index]
