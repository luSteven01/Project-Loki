extends Panel

@onready var game_manager = get_node("/root/Main/GameManager")

@onready var dialogue_text = $NPC_Dialogue
@onready var npc_icon = $NPC_Icon
@onready var talk_input = $Player_Input
@onready var submit_button = $SubmitButton
@onready var leave_button = $LeaveButton

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.

func initialize_with_npc (npc):
	#NPC Icon
	dialogue_text.text = ""
	submit_button.disabled = true


func _on_submit_button_pressed() -> void:
	var player_message = talk_input.text.strip_edges()
	if player_message != "":
		# Show player's message in dialogue window
		dialogue_text.text += "\n[Player]: " + player_message

		# Send player's message to GameManager → ChatGPT
		game_manager.dialogue_request(player_message)

		# Clear the input for the next line
		talk_input.text = ""


func _on_leave_button_pressed() -> void:
	hide() # Replace with function to return to game screen
