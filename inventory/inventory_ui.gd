extends Control

@onready var inventory : Inventory = preload("res://inventory/player_inventory.tres") # preload player inventory

@onready var slots : Array = $NinePatchRect/GridContainer.get_children()

var is_open = false

# makes sure inventory is closed at the start
func _ready():
	inventory.update.connect(update_slots) # whenever update signal is called, we connect it to update slots 
	update_slots()
	close()

func update_slots():
	for i in range (min(inventory.slots.size(), slots.size())):
		slots[i].update(inventory.slots[i]) # call our slot & update function; update to whatever the inventory item is for that specific slot
	
func _process(delta):
	if Input.is_action_just_pressed("interact_with_inventory"):
		if is_open:
			close()
		else:
			open()

func close():
	visible = false
	is_open = false

func open():
	visible = true
	is_open = true
