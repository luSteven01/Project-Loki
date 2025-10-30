extends Panel

@onready var game_manager = get_node("/root/Main/GameManager")

@onready var dialogue_text : RichTextLabel = get_node("NPC_Dialogue")
@onready var npc_icon : TextureRect = get_node("NPC_Icon")
@onready var talk_input : TextEdit  = get_node("Player_Input")
@onready var submit_button : Button = get_node("SubmitButton")
@onready var leave_button : Button = get_node("LeaveButton")

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	game_manager.on_player_talk.connect(_on_player_talk)
	game_manager.on_npc_talk.connect(_on_npc_talk)	

func initialize_with_npc (npc):
	npc_icon.texture = npc.icon # add NPC icon
	dialogue_text.text = ""
	submit_button.disabled = true

#func _on_submit_button_pressed() -> void:
	#var player_message = talk_input.text.strip_edges()
	#if player_message != "":
		## Show player's message in dialogue window
		#dialogue_text.text += "\n[Player]: " + player_message
#
		## Send player's message to GameManager → ChatGPT
		#game_manager.dialogue_request(player_message)
#
		## Clear the input for the next line
		#talk_input.text = ""
#
#
#func _on_leave_button_pressed() -> void:
	#hide() # Replace with function to return to game screen
	
func _on_player_talk():
	talk_input.text = "" # clear text-input so player can type a new message
	dialogue_text.text = "Forming response..." # update NPC's dialogue text 
	submit_button.disabled = true # disable talk button so player cannot send a message while server is processing message
	
func _on_npc_talk (npc_dialogue):
	dialogue_text.text = npc_dialogue # update dialogue's text to npc's
	submit_button.disabled = false #re-enable talk button so player can respond to NPC's message
	# pass;
	
func _on_submit_button_pressed() -> void:
	game_manager.dialogue_request(talk_input.text)
	
func _on_leave_button_pressed() -> void:
	game_manager.exit_dialogue()
