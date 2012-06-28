from pymclevel import TAG_Compound
from pymclevel import TAG_Int
from pymclevel import TAG_Short
from pymclevel import TAG_Byte
from pymclevel import TAG_String
from pymclevel import TAG_Float
from pymclevel import TAG_Double
from pymclevel import TAG_List
from pymclevel import alphaMaterials
am = alphaMaterials

MobID = {
	"Blaze": "Blaze",
	"Cave Spider": "CaveSpider",
	"Chicken": "Chicken",
	"Cow": "Cow",
	"Creeper": "Creeper",
	"Ender Dragon": "EnderDragon",
	"Enderman": "Enderman",
	"Ghast": "Ghast",
	"Giant Zombie": "Giant",
	"Lava Slime": "LavaSlime",
	"Mooshroom": "MushroomCow",
	"Ocelot": "Ozelot",
	"Pig": "Pig",
	"Sheep": "Sheep",
	"Silverfish": "Silverfish",
	"Skeleton": "Skeleton",
	"Slime": "Slime",
	"Snow Golem": "SnowMan",
	"Spider": "Spider",
	"Squid": "Squid",
	"Villager": "Villager",
	"Wolf": "Wolf",
	"Zombie": "Zombie",
	"Zombie Pig-Man": "PigZombie",
	}
	
PotionEffectID = {
	"Speed": 1,
	"Slowness": 2,
	"Haste": 3,
	"Mining Fatigue": 4,
	"Strength": 5,
	"Instant Health": 6,
	"Instant Damage": 7,
	"Jump Boost": 8,
	"Nausea": 9,
	"Regeneration": 10,
	"Resistance": 11,
	"Fire Resistance": 12,
	"Water Breathing": 13,
	"Invisibility": 14,
	"Blindness": 15,
	"Night Vision": 16,
	"Hunger": 17,
	"Weakness": 18,
	"Poison": 19,
	}
	
MobIDKeys = ()
for key in MobID.keys():
	MobIDKeys = MobIDKeys + (key,)
	
PotionEffectIDKeys = ()
for key in PotionEffectID.keys():
	PotionEffectIDKeys = PotionEffectIDKeys + (key,)
	

inputs = (
	("MobID", MobIDKeys),
	("Age (Animals): ", (-600, 0)),
	("Saddle (Pig): ", (0, 1)),
	("Sheared (Sheep): ", (0, 1)),
	("Color (Sheep): ", (0, 15)),
	("Powered (Creeper): ", (0, 1)),
	("Size (Slime): ", (0, 100)),
	("Angry (Wolf): ", (0, 100)),
	("Anger (Zombie Pigman): ", (0,10)),
	("Carried (EnderMan): ", (0,1000)),
	("CarriedData (EnderMan): ", (0,100)),
	("Profession (Villager): ", (0, 5)),
	("Potion Effect: ", PotionEffectIDKeys),
	("Potion Amplifier: ", (0, 100)),
	("Potion Duration: ", (0, 1000000000)),
	("Health: ", (1, 1000000)),
)

displayName = "Create Super-Spawner"


def perform(level, box, options):
	health = options["Health: "]
	age = options["Age (Animals): "]
	saddled = options["Saddle (Pig): "]
	sheared = options["Sheared (Sheep): "]
	color = options["Color (Sheep): "]
	powered = options["Powered (Creeper): "]
	size = options["Size (Slime): "]
	angry = options["Angry (Wolf): "]
	anger = options["Anger (Zombie Pigman): "]
	carried = options["Carried (EnderMan): "]
	carrieddata = options["CarriedData (EnderMan): "]
	profession = options["Profession (Villager): "]
	poteffect = options["Potion Effect: "]
	potamp = options["Potion Amplifier: "]
	potdur = options["Potion Duration: "]
	
	for x in range(box.minx, box.maxx):
		for y in range(box.miny, box.maxy):
			for z in range(box.minz, box.maxz):
				if level.blockAt(x, y, z) == 52:
					createSuperSpawner(level, x, y, z, health, MobID[options["MobID"]], age, saddled, sheared, color, powered, size, angry, anger, carried, carrieddata, profession, poteffect, potamp, potdur)

def createSuperSpawner(level, x, y, z, health, mobid, age, saddled, sheared, color, powered, size, angry, anger, carried, carrieddata, profession, poteffect, potamp, potdur):
	mobSpawner = level.tileEntityAt(x, y, z)
	if mobSpawner == None:
		return
	mobSpawner2 = TAG_Compound()
	mobSpawner2["id"] = TAG_String("MobSpawner")
	mobSpawner2["x"] = TAG_Int(x)
	mobSpawner2["y"] = TAG_Int(y)
	mobSpawner2["z"] = TAG_Int(z)
	mobSpawner2["Delay"] = TAG_Short(120)
	mobSpawner2["SpawnData"] = TAG_Compound()
	mobSpawner2["SpawnData"]["Health"] = TAG_Short(health)
	mobSpawner2["SpawnData"]["Saddle"] = TAG_Byte(saddled)
	mobSpawner2["SpawnData"]["Sheared"] = TAG_Byte(sheared)
	mobSpawner2["SpawnData"]["Color"] = TAG_Byte(color)
	mobSpawner2["SpawnData"]["powered"] = TAG_Byte(powered)
	mobSpawner2["SpawnData"]["Size"] = TAG_Int(size)
	mobSpawner2["SpawnData"]["Angry"] = TAG_Byte(angry)
	mobSpawner2["SpawnData"]["Anger"] = TAG_Byte(anger)
	mobSpawner2["SpawnData"]["carried"] = TAG_Short(carried)
	mobSpawner2["SpawnData"]["carriedData"] = TAG_Short(carrieddata)
	mobSpawner2["SpawnData"]["Profession"] = TAG_Int(profession)
	mobSpawner2["SpawnData"]["AciveEffects"] = TAG_List()
	effect1 = TAG_Compound()
	effect1["Amplifier"] = TAG_Byte(potamp)
	effect1["Id"] = TAG_Byte(poteffect)
	effect1["Duration"] = TAG_Int(potdur)
	mobSpawner2["SpawnData"]["ActiveEffects"].append(effect1)
	mobSpawner2["EntityId"] = TAG_String(mobid)

	chunk = level.getChunk(x / 16, z / 16)
	chunk.TileEntities.remove(mobSpawner)
	chunk.TileEntities.append(mobSpawner2)
	chunk.dirty = True
	
