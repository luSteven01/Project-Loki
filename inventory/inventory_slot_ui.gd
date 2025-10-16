extends Panel

@onready var item_visual : Sprite2D = $CenterContainer/Panel/item_display # to display the item in the inventory
@onready var amount_text : Label = $CenterContainer/Panel/Label 

func update(slot: Inventory_Slot):
	# changing visual and texture depending on if we got the item in our inventory 
	if !slot.item: # get item in that slot
		item_visual.visible = false
		amount_text.visible = false
	else:
		item_visual.visible = true
		item_visual.texture = slot.item.texture # get item's texture inside the slot
		amount_text.visible = true
		amount_text.text = str(slot.amount)
