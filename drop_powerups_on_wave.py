def drop_powerups_on_wave(enemy_group, powerups, all_sprites, Powerup):
    import random
    if len(enemy_group) == 0:
        return
    chosen = random.sample(list(enemy_group), min(2, len(enemy_group)))
    for enemy in chosen:
        px = enemy.rect.centerx
        py = enemy.rect.bottom + 10
        p = Powerup(px, py)
        powerups.add(p)
        all_sprites.add(p)
