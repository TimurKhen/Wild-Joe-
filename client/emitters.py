import random

import arcade
from arcade.particles import Emitter, EmitBurst, FadeParticle

SMOKE_TEX = arcade.make_soft_circle_texture(20, arcade.color.LIGHT_GRAY, 255, 80)
SPARK_TEX = [
    arcade.make_soft_circle_texture(7, arcade.color.BROWN),
    arcade.make_soft_square_texture(10, arcade.color.DIRT),
    arcade.make_soft_circle_texture(7, arcade.color.ORANGE),
]
BLOOD_TEX = [
    arcade.make_soft_circle_texture(15, arcade.color.RED),
    arcade.make_soft_circle_texture(15, arcade.color.RED_DEVIL),
    arcade.make_soft_circle_texture(15, arcade.color.RADICAL_RED),
]


def smoke_mutator(p):
    p.scale_x *= 1.01
    p.scale_y *= 1.01
    p.alpha = max(0, p.alpha - 5)


def gravity_drag(p):
    p.change_y -= 0.03
    p.change_x *= 0.92
    p.change_y *= 0.92


def make_smoke_puff(x, y):
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(30),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=SMOKE_TEX,
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 0.6),
            lifetime=random.uniform(1, 2),
            start_alpha=150, end_alpha=0,
            scale=random.uniform(0.3, 0.8),
            mutation_callback=smoke_mutator,
        ),
    )


def make_explosion(x, y, count=80, radius=5.0):
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(count),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=random.choice(SPARK_TEX),
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), radius),
            lifetime=random.uniform(0.5, 1.2),
            start_alpha=255, end_alpha=0,
            scale=random.uniform(0.5, 0.7),
            mutation_callback=gravity_drag,
        ),
    )


def make_blood_explosion(x, y, count=80, radius=3.0):
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(count),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=random.choice(BLOOD_TEX),
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), radius),
            lifetime=random.uniform(0.5, 1.2),
            start_alpha=255, end_alpha=0,
            scale=random.uniform(0.5, 0.7),
            mutation_callback=gravity_drag,
        ),
    )


def make_through_blood_explosion(x, y, angle_deg, count=100, spread_angle=90, speed=4.0):
    import math

    angle_rad = math.radians(angle_deg)

    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(count),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=random.choice(BLOOD_TEX),
            change_xy=_get_through_blood_velocity(angle_rad, speed),
            lifetime=random.uniform(0.4, 1.0),
            start_alpha=255, end_alpha=0,
            scale=random.uniform(0.4, 0.8),
            mutation_callback=gravity_drag,
        ),
    )


def _get_through_blood_velocity(angle_rad, speed):
    import math
    import random

    angle_offset = random.uniform(-math.pi / 4, math.pi / 4)
    particle_angle = angle_rad + angle_offset

    particle_speed = random.uniform(speed * 0.5, speed * 2.0)

    vx = math.cos(particle_angle) * particle_speed
    vy = math.sin(particle_angle) * particle_speed

    return (vx, vy)


def make_blood_stain(x, y, scale_min=2, scale_max=5, lifetime=8.0):
    """
    Создает одно кровяное пятно, которое долго выцветает

    Args:
        x, y: позиция пятна
        scale_min, scale_max: диапазон размера пятна
        lifetime: время жизни в секундах (до полного исчезновения)
    """
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(1),  # Только одно пятно
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=random.choice(BLOOD_TEX),
            change_xy=(0.0, 0.0),  # Не двигается
            lifetime=lifetime,
            start_alpha=220,  # Начальная прозрачность
            end_alpha=0,  # Полностью исчезает
            scale=random.uniform(scale_min, scale_max),
            # Без mutation_callback, так как пятно статичное
        ),
    )


def make_blood_puddle(x, y, count=3, radius=5, lifetime=20.0):
    """
    Создает небольшую лужу крови из нескольких пятен
    """
    stains = []
    for _ in range(count):
        offset_x = random.uniform(-radius * 5, radius * 5)
        offset_y = random.uniform(-radius * 5, radius * 5)  # Эллиптическая форма

        stain = Emitter(
            center_xy=(x + offset_x, y + offset_y),
            emit_controller=EmitBurst(1),
            particle_factory=lambda e: FadeParticle(
                filename_or_texture=random.choice(BLOOD_TEX),
                change_xy=(0.0, 0.0),
                lifetime=random.uniform(lifetime * 3, lifetime * 7),
                start_alpha=random.randint(200, 220),
                end_alpha=0,
                scale=random.uniform(1.7, 3),
            ),
        )
        stains.append(stain)
    return stains