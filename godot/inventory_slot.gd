extends Control

@onready var icon = $InnerBorder/ItemIcon
@onready var quantity_label = $InnerBorder/ItemQuantity
@onready var details_panel = $DetailsPanel
@onready var item_name = $DetailsPanel/ItemName
@onready var item_desc = $DetailsPanel/ItemDesc
@onready var usage_panel = $UsagePanel
@onready var outer_border = $OuterBorder

signal drag_start(slot)
signal drag_end()

var item_id: String = ""
var item_data: Dictionary = {}

func _ready():
	details_panel.visible = false

func set_empty():
	icon.texture = null
	item_name.text = ""
	item_desc.text = ""


func set_item(id: String, data: Dictionary):
	item_id = id
	item_data = data

	item_name.text = id.capitalize()
	icon.texture = data.get("icon", null)
	item_desc.text = data.get("description", "")


func _on_item_button_mouse_entered():
	if item_data != {}:
		usage_panel.visible = false
		details_panel.visible = true


func _on_item_button_mouse_exited():
	details_panel.visible = false

func _on_item_button_gui_input(event: InputEvent):
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT and event.is_pressed():
			if item_data != {}:
				usage_panel.visible = !usage_panel.visible
#	
# this is basically broken now so we can just remove this part
# originally this was supposed to swap inventory items but this will mess with the backend + communicating with the npcs so we arent
# doing this anymore 
		#if event.button_index == MOUSE_BUTTON_RIGHT:
			#if event.is_pressed():
				#outer_border.modulate = Color(1,1,0)
				#drag_start.emit(self)
			#else:
				#outer_border.modulate = Color(1,1,1)
				#drag_end.emit()
