import init_django_orm  # noqa: F401
import json

from db.models import Race, Skill, Player, Guild


def main() -> None:
    data = json.load(open("players.json"))

    for player_name, info in data.items():
        race_data = info["race"]
        race, _ = Race.objects.get_or_create(
            name=race_data["name"],
            defaults={"description": race_data["description"]}
        )

        if not race.skill_set.exists():
            for skill in race_data["skills"]:
                Skill.objects.create(
                    race=race,
                    name=skill["name"],
                    bonus=skill["bonus"]
                )

        guild_obj = None
        guild_data = info["guild"]
        if guild_data:
            guild_obj, _ = Guild.objects.get_or_create(
                name=guild_data["name"],
                defaults={"description": guild_data["description"]}
            )

        Player.objects.update_or_create(
            nickname=player_name,
            defaults={
                "email": info["email"],
                "bio": info["bio"],
                "race": race,
                "guild": guild_obj
            }
        )


if __name__ == "__main__":
    main()
