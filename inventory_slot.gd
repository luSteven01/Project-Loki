extends Control

#Scene-Tree Node references
@onready var icon = $InnerBorder/ItemIcon
@onready var quantity_label = $InnerBorder/ItemQuantity
@onready var details_panel = $DetailsPanel
@onready var item_name = $DetailsPanel/ItemName
@onready var item_type = $DetailsPanel/ItemType
@onready var item_effect = $DetailsPanel/ItemEffect
@onready var usage_panel = $UsagePanel
@onready var outer_border = $OuterBorder

# signals for dragging items
signal drag_start(slot)
signal drag_end()

# holds data for item
var item = null
	
# show item when we hover mouse over item
func _on_item_button_mouse_entered() -> void:
	if item != null:
		usage_panel.visible = false
		details_panel.visible = true

# hide item details when we are not hovering over the item
func _on_item_button_mouse_exited() -> void:
	details_panel.visible = false

# create empty slot w/ no values
func set_empty():
	icon.texture = null
	quantity_label.text = ""
	
# set slots w/ details of new item we want to add to inventory; update icon and item details and quantity based on
# new item dictionary passed to it by inventory item component
func set_item(new_item):
	item = new_item
	icon.texture = new_item["texture"]
	quantity_label.text = str(item["quantity"])
	item_name.text = str(item["name"])
	item_type.text = str(item["type"])
	if item["effect"] != "":
		item_effect.text = str("-  ", item["effect"])
	else:
		item_effect.text = ""

func _on_drop_button_pressed() -> void:
	if item != null:
		var drop_position = Global.player_node.global_position
		
		# give item a drop offset of 50x to right of player's position
		# turn offset based off player rotation so its dropped in player's direction
		
		var drop_offset = Vector2(0, 50)
		drop_offset = drop_offset.rotated(Global.player_node.rotation)
		
		# remove item from inventory
		Global.drop_item(item, drop_position + drop_offset)
		Global.remove_item(item["type"], item["effect"])
		
		usage_panel.visible = false
	
	
func _on_use_button_pressed() -> void:
	usage_panel.visible = false
	
	if item != null and item["effect"] != "": # if item exists and there is an effect, apply item effect
		if Global.player_node:
			Global.player_node.apply_item_effect(item)
			Global.remove_item(item["type"], item["effect"])
			print("item hashcode: ", item["hashcode"])
		else:
			print("Player could not be found. ")

# item button events
func _on_item_button_gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT and event.is_pressed():
			if item != null:
				usage_panel.visible = !usage_panel.visible
		if event.button_index == MOUSE_BUTTON_RIGHT:
			if event.is_pressed(): # start dragging w/ right mouse
				outer_border.modulate = Color(1, 1, 0)
				drag_start.emit(self)
			else:
				outer_border.modulate = Color(1, 1, 1)
				drag_end.emit()
		
		
