extends Node

# reference to player node
var player_node : Node = null
# manages inventory

# path reference to inventory slots 
@onready var inventory_slot_scene = preload("res://inventory_slot.tscn")
@onready var dialogue_box = preload("res://dialogue_box.tscn")

# holds inventory items
var inventory = []

var dialogue = null

# items we spawn on load
var spawnable_items = [
	{"type": "Consumable", 
	"name": "Berry", 
	"effect": "Health", 
	"texture": preload("res://Assets/Icons/icon31.png"),
	"hashcode": "f13e7"}
	
	#{"type": "Consumable", 
	#"name": "Mushroom", 
	#"effect": "Mana", 
	#"texture": preload("res://Assets/Icons/icon32.png"),
	#"hashcode": "275a0"},
	
	#{"type": "Consumable", 
	#"name": "Coin", 
	#"effect": "Money", 
	#"texture": preload("res://Assets/Icons/icon20.png"),
	#"hashcode": "ba572"},
	#
	#{"type": "Consumable", 
	#"name": "Shell", 
	#"effect": "SlotIncrease", 
	#"texture": preload("res://Assets/Icons/icon30.png"),
	#"hashcode": "3b48d"}
]

# signal for updating inventory
signal inventory_updated

func _ready():
	# initialize inventory with 10 slots initially
	# when we remove/add items, notify game that inventory is updated to update inventory UI
	dialogue = dialogue_box.instantiate()
	add_child(dialogue)
	dialogue.visible = false
	inventory.resize(5)

func add_item(item):
	for i in range(inventory.size()):
		# check if item w/ type and effect already exist to stack quantity
		if inventory[i] != null and inventory[i]["type"] == item["type"] and inventory[i]["effect"] == item["effect"]:
			inventory[i]["quantity"] += item["quantity"]
			inventory_updated.emit()
			print("added item: ", inventory)
			return true
		elif inventory[i] == null: # place new item in slot if there is an empty slot
			inventory[i] = item
			inventory_updated.emit()
			print("added item: ", inventory)
			return true
	return false

# go through inventory array & remove item w/ certain type and effect
func remove_item(item_type, item_effect):
	for i in range(inventory.size()):
		if inventory[i] != null and inventory[i]["type"] == item_type and inventory[i]["effect"] == item_effect:
			inventory[i]["quantity"] -= 1
			if inventory[i]["quantity"] <= 0:
				inventory[i] = null
			inventory_updated.emit()
			return true
	return false
	
func increase_inventory_size(extra_slots):
	inventory.resize(inventory.size() + extra_slots)
	inventory_updated.emit()

func init_player_reference(player):
	player_node = player
	
# position game checks when it tries to drop an item in a valid location
func adjust_drop_position(position):
	var drop_radius = 100
	var nearby_items = get_tree().get_nodes_in_group("Items")
	
	# check if item is within spawn area
	for item in nearby_items:
		if item.global_position.distance_to(position) < drop_radius:
			# within radius: too close to drop position; overlaps w/ another item. create offset within radius value to place item nearby
			var random_offset = Vector2(randf_range(-drop_radius, drop_radius), randf_range(-drop_radius, drop_radius))
			position += random_offset
			break # valid drop position found
	return position	

func drop_item(item_data, drop_position):
	var item_scene = load(item_data["scene_path"])
	var item_instance = item_scene.instantiate()
	item_instance.set_item_data(item_data)
	
	# set valid drop position
	drop_position = adjust_drop_position(drop_position)
	item_instance.global_position = drop_position
	get_tree().current_scene.add_child(item_instance)
	
func swap_inventory_items(index1, index2):
	if index1 < 0 or index1 > inventory.size() or index2 < 0 or index2 > inventory.size():
		return false
	
	var tempSlot = inventory[index1]
	inventory[index1] = inventory[index2]
	inventory[index2] = tempSlot
	
	inventory_updated.emit()
	return true
	
func _on_inventory_updated():
	for i in range(inventory.size()):
		
		if inventory[i] == null:
			continue
			
		match(inventory[i]["name"]):
			"Berry":
				print("Berry exists: ", item_exists("Berry"))
			"Coin":
				print("Coin exists: ", item_exists("Coin"))
			"Shell":
				print("Shell exists: ", item_exists("Shell"))
			"Mushroom":
				print("Mushroom exists: ", item_exists("Mushroom"))	
			
func item_exists(item_name):
	for item in inventory:
		if item != null and item["name"] == item_name:
			return true
	return false
	
# show item to the NPC
func show_item(item):
	match item["name"]:
		"Berry":
			print("Berry was shown")
			dialogue.evidence_button.visible = true
			dialogue.evidence_button.text = "berry's hash code just for testing" + item["hashcode"]
		"Shell":
			print("Shell was shown")
			dialogue.evidence_button.visible = true
			dialogue.evidence_button.text = "shell's hash code just for testing" + item["hashcode"]
		"Mushroom":
			print("Mushrom was shown")
			dialogue.evidence_button.visible = true
			dialogue.evidence_button.text = "mushroom's hash code just for testing" + item["hashcode"]
		"Coin":
			print("Coin was shown")
			dialogue.evidence_button.visible = true
			dialogue.evidence_button.text = "coin's hash code just for testing" + item["hashcode"]
		_: # if we have an item like a quest item, add the effect here; can also call a function
			print("No item") 


	
