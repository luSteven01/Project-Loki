extends Control

@onready var grid_container = $GridContainer

# what we are drag/droping
var dragged_slot = null

func _ready():
	Global.inventory_updated.connect(_on_inventory_update) #inventory loads w/ correct # of columns and rows when inventory UI is added to scene
	_on_inventory_update()

# update inventory UI
func _on_inventory_update():
	clear_grid_container()
	
	# iterate through each item in global inventory array
	# for each item, add a slot
	for item in Global.inventory:
		# for each item, create new slot from inventory slot scene & add to grid container
		var slot = Global.inventory_slot_scene.instantiate()
		
		slot.drag_start.connect(_on_drag_start)
		slot.drag_end.connect(_on_drag_end)
		grid_container.add_child(slot)
		
		# check if slot position we are creating contains an item. no item = empty slot
		if item != null:
			slot.set_item(item)
		else:
			slot.set_empty()
	
		
# when adding existing item to inventory, quantity might not update
# func clears all children from grid container to reset inventory before adding new items
func clear_grid_container():
	while grid_container.get_child_count() > 0:
		var child = grid_container.get_child(0)
		grid_container.remove_child(child)
		child.queue_free()

# store dragged slot reference
func _on_drag_start(slot_control : Control):
	dragged_slot = slot_control
	print("Drag started from: ", dragged_slot)
	
# drop item in new slot after done dragging; get new slot 
func _on_drag_end():
	var target_slot = get_slot_at_mouse()
	if target_slot and dragged_slot != target_slot:
		drop_slot(dragged_slot, target_slot)	
	dragged_slot = null

func get_slot_at_mouse() -> Control:
	var mouse_position = get_global_mouse_position()
	for slot in grid_container.get_children():
		var slot_rect = Rect2(slot.global_position, slot.size)
		if slot_rect.has_point(mouse_position):
			return slot
	return null

func get_slot_index(slot: Control):
	for i in range(grid_container.get_child_count()):
		if grid_container.get_child(i) == slot:
			# valid slot
			return i
	# invalid slot 
	return -1

func drop_slot(slot1 : Control, slot2: Control):
	var slot1_index = get_slot_index(slot1)
	var slot2_index = get_slot_index(slot2)
	
	if slot1_index == -1 or slot2_index == -1:
		print("invalid slot")
		return
	else:
		if Global.swap_inventory_items(slot1_index, slot2_index):
			print("Swapping slot items: ", slot1, slot2_index)
			_on_inventory_update()
