# making it extend a resource because we're connecting this script to any inventory (NPC, player, chest)
extends Resource

class_name Inventory

signal update # called when we update slots

@export var slots : Array[Inventory_Slot] # what we are storing in our inventory

# insert item into inventory 
func insert(item : InventoryItem):
	# first slot is open? --> add new item to that slot, amount = 0
	# if it is not, figure out what slot we are going to be in. if not full, picks slot thats empty
	var itemSlots = slots.filter(func(slot) : return slot.item == item) 
	if !itemSlots.is_empty(): # for existing slots
		itemSlots[0].amount += 1
	else:
		var emptySlots = slots.filter(func(slot) : return slot.item == null)
		if !emptySlots.is_empty():
			emptySlots[0].item = item
			emptySlots[0].item = 1 # if slot is empty, insert into inventory slot and keep new tally for it 
	update.emit() # updates slot UI
