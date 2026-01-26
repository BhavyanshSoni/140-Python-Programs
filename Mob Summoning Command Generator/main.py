"""
Minecraft Summon Command Builder
--------------------------------
A simple CLI tool that asks the user which mob to spawn, which ARMOR material to use,
then asks for enchantments for each armor piece, and finally prints a single
Java Edition /summon command with NBT to paste into Minecraft (1.20+).

Notes
- Works for Java Edition. Tested NBT format is broadly valid for 1.20+.
- Armor order in ArmorItems must be: BOOTS, LEGGINGS, CHESTPLATE, HELMET.
- Enchantment format while typing: name:level, name:level ... (comma-separated)
  Example: protection:4, unbreaking:3, mending:1
- Leave empty to skip enchantments for that piece.
- By default, drop chances are set to 0 so the mob won't drop the armor.
- Add more enchantment aliases in ENCH_ALIASES if you like.
"""

from typing import Dict, List
import re

# --- Configurable dictionaries ---
ARMOR_MATERIALS = {
    "leather": {
        "helmet": "minecraft:leather_helmet",
        "chestplate": "minecraft:leather_chestplate",
        "leggings": "minecraft:leather_leggings",
        "boots": "minecraft:leather_boots",
    },
    "gold": {
        "helmet": "minecraft:golden_helmet",
        "chestplate": "minecraft:golden_chestplate",
        "leggings": "minecraft:golden_leggings",
        "boots": "minecraft:golden_boots",
    },
    "chainmail": {
        "helmet": "minecraft:chainmail_helmet",
        "chestplate": "minecraft:chainmail_chestplate",
        "leggings": "minecraft:chainmail_leggings",
        "boots": "minecraft:chainmail_boots",
    },
    "iron": {
        "helmet": "minecraft:iron_helmet",
        "chestplate": "minecraft:iron_chestplate",
        "leggings": "minecraft:iron_leggings",
        "boots": "minecraft:iron_boots",
    },
    "diamond": {
        "helmet": "minecraft:diamond_helmet",
        "chestplate": "minecraft:diamond_chestplate",
        "leggings": "minecraft:diamond_leggings",
        "boots": "minecraft:diamond_boots",
    },
    "netherite": {
        "helmet": "minecraft:netherite_helmet",
        "chestplate": "minecraft:netherite_chestplate",
        "leggings": "minecraft:netherite_leggings",
        "boots": "minecraft:netherite_boots",
    },
}

# Common armor enchantments and some handy aliases
ENCH_ALIASES: Dict[str, str] = {
    # Protection variants
    "prot": "minecraft:protection",
    "protection": "minecraft:protection",
    "blast_protection": "minecraft:blast_protection",
    "blast": "minecraft:blast_protection",
    "fire_protection": "minecraft:fire_protection",
    "fireprot": "minecraft:fire_protection",
    "projectile_protection": "minecraft:projectile_protection",
    "proj": "minecraft:projectile_protection",

    # Durability/repair
    "unbreaking": "minecraft:unbreaking",
    "mending": "minecraft:mending",

    # Helmet
    "respiration": "minecraft:respiration",
    "aqua_affinity": "minecraft:aqua_affinity",

    # Boots
    "feather_falling": "minecraft:feather_falling",
    "depth_strider": "minecraft:depth_strider",
    "frost_walker": "minecraft:frost_walker",
    "soul_speed": "minecraft:soul_speed",

    # Thorns + Swift Sneak (leggings)
    "thorns": "minecraft:thorns",
    "swift_sneak": "minecraft:swift_sneak",
}

ARMOR_ORDER = ["boots", "leggings", "chestplate", "helmet"]  # NBT order requirement


def normalize_material(inp: str) -> str:
    key = inp.strip().lower()
    # allow some short forms
    short = {
        "golden": "gold",
        "gold": "gold",
        "chain": "chainmail",
        "chainmail": "chainmail",
        "iron": "iron",
        "dia": "diamond",
        "diamond": "diamond",
        "netherite": "netherite",
        "neth": "netherite",
        "leather": "leather",
    }.get(key, key)
    return short


def parse_enchants(s: str) -> List[Dict[str, str]]:
    """Parse a comma-separated list like "protection:4, unbreaking:3" into
    [{id: 'minecraft:protection', lvl: '4s'}, ...]. Returns an empty list if none.
    """
    if not s.strip():
        return []
    out = []
    parts = [p.strip() for p in s.split(',') if p.strip()]
    for p in parts:
        # Accept formats: name:level OR name level
        m = re.match(r"^([a-zA-Z_]+)\s*[: ]\s*(\d+)$", p)
        if not m:
            print(f"  Skipping '{p}' (use 'name:level', e.g., protection:4)")
            continue
        name = m.group(1).lower()
        lvl = int(m.group(2))
        ench_id = ENCH_ALIASES.get(name, None)
        if ench_id is None:
            # If user typed full namespaced id already
            if ":" in name:
                ench_id = name  # trust user input
            else:
                print(f"  Unknown enchant '{name}', skipping. Add it to ENCH_ALIASES if needed.")
                continue
        out.append({"id": ench_id, "lvl": f"{lvl}s"})  # 's' = short in NBT
    return out


def enchants_nbt(enchs: List[Dict[str, str]]) -> str:
    if not enchs:
        return ""
    parts = [f"{{id:\"{e['id']}\",lvl:{e['lvl']} }}" for e in enchs]
    return f"tag:{{Enchantments:[{', '.join(parts)}]}}"


def item_nbt(item_id: str, enchs: List[Dict[str, str]]) -> str:
    tag_part = enchants_nbt(enchs)
    if tag_part:
        return f"{{id:\"{item_id}\",Count:1b,{tag_part}}}"
    else:
        return f"{{id:\"{item_id}\",Count:1b}}"


def build_command(mob: str, material_key: str, per_piece_enchs: Dict[str, List[Dict[str, str]]], \
                  no_drops: bool = True, persistent: bool = True) -> str:
    material = ARMOR_MATERIALS[material_key]

    armor_items_strs = []
    for piece in ARMOR_ORDER:
        item_id = material[piece]
        armor_items_strs.append(item_nbt(item_id, per_piece_enchs.get(piece, [])))

    armor_items_nbt = f"ArmorItems:[{', '.join(armor_items_strs)}]"
    drop_chances_nbt = "ArmorDropChances:[0.0f,0.0f,0.0f,0.0f]" if no_drops else ""
    persistence_nbt = "PersistenceRequired:1b" if persistent else ""

    extra_parts = ", ".join([p for p in [drop_chances_nbt, persistence_nbt] if p])
    body = ", ".join([p for p in [armor_items_nbt, extra_parts] if p])

    return f"/summon {mob} ~ ~ ~ {{{body}}}"


def ask(prompt: str) -> str:
    try:
        return input(prompt)
    except EOFError:
        return ""


def main():
    print("=== Minecraft Summon Command Builder ===")
    mob = ask("Mob ID (e.g., zombie, skeleton, husk, drowned, blaze): ").strip()
    if not mob:
        mob = "zombie"
        print("  (Empty -> defaulted to 'zombie')")

    material_in = normalize_material(ask("Armor material (leather/gold/chainmail/iron/diamond/netherite): "))
    while material_in not in ARMOR_MATERIALS:
        print("  Invalid material. Try again.")
        material_in = normalize_material(ask("Armor material (leather/gold/chainmail/iron/diamond/netherite): "))

    print("\nEnter enchantments for each piece (comma-separated 'name:level').")
    print("Examples: protection:4, unbreaking:3, mending:1  |  (Leave blank to skip)\n")

    per_piece_enchs: Dict[str, List[Dict[str, str]]] = {}
    for piece in ["helmet", "chestplate", "leggings", "boots"]:
        raw = ask(f"{piece.title()} enchants: ")
        per_piece_enchs[piece] = parse_enchants(raw)

    nodrops_ans = ask("Set armor drop chances to 0? (Y/n): ").strip().lower()
    no_drops = (nodrops_ans != "n")

    persistent_ans = ask("Make mob persistent (won't despawn)? (Y/n): ").strip().lower()
    persistent = (persistent_ans != "n")

    # Build and show command
    cmd = build_command(mob, material_in, per_piece_enchs, no_drops, persistent)

    print("\n\n>>> Copy & paste this in Minecraft chat/command block:")
    print(cmd)


if __name__ == "__main__":
    main()



# /summon zombie ~ ~ ~ {ArmorItems:[{id:"minecraft:iron_boots",Count:1b,tag:{Enchantments:[{id:"minecraft:protection",lvl:4s }, {id:"minecraft:unbreaking",lvl:3s }, {id:"minecraft:mending",lvl:1s }]}}, {id:"minecraft:iron_leggings",Count:1b,tag:{Enchantments:[{id:"minecraft:protection",lvl:4s }, {id:"minecraft:unbreaking",lvl:3s }, {id:"minecraft:mending",lvl:1s }]}}, {id:"minecraft:iron_chestplate",Count:1b,tag:{Enchantments:[{id:"minecraft:protection",lvl:4s }, {id:"minecraft:unbreaking",lvl:3s }, {id:"minecraft:mending",lvl:1s }]}}, {id:"minecraft:iron_helmet",Count:1b,tag:{Enchantments:[{id:"minecraft:protection",lvl:4s }, {id:"minecraft:unbreaking",lvl:3s }, {id:"minecraft:mending",lvl:1s }]}}], ArmorDropChances:[0.0f,0.0f,0.0f,0.0f]}