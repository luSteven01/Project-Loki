extends Panel

@onready var game_manager = get_node("/root/Main/GameManager")

@onready var dialogue_text = $DialogueText
@onready var npc_icon = $NPCIcon
@onready var talk_input = $PlayerTextInput
@onready var submit_button = $SubmitButton
@onready var leave_button = $Leavebutton

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.

func initialize_with_npc (npc):
	#NPC Icon
	dialogue_text.text = ""
	submit_button.disabled = true


func _on_submit_button_pressed() -> void:
	pass # Replace with function body.


func _on_leave_button_pressed() -> void:
	pass # Replace with function body.
