extends Node

@onready var dialogue_box = get_node("/root/Main/CanvasLayer/DialogueBox") # get dialogue box from main scene 
@onready var world_context = get_node("/root/Main/WorldContext")


# API Configuration
const API_BASE_URL = "http://127.0.0.1:8000"

# State management
var sessions = {}  # { character_id: session_id }
var current_character = null
var characters = []
var is_loading = false

var http_request: HTTPRequest

enum RequestType {
	HEALTH_CHECK,
	LOAD_CHARACTERS,
	SEND_MESSAGE
}
var current_request_type = RequestType.HEALTH_CHECK

func _ready():
	print("we have world context: " + str(world_context != null))
	print("Children of WorldContext:")
	for c in world_context.get_children():
		print(" - ", c.name)
	print("GameManager instance path:", get_path())


	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(_on_request_completed)

	print("GameManager ready - connecting to backend...")
	check_server_health()

# ============================================
# API Functions
# ============================================

func check_server_health():
	print("Checking server health...")
	current_request_type = RequestType.HEALTH_CHECK
	var error = http_request.request(API_BASE_URL + "/health")
	if error != OK:
		print("Failed to connect to server: ", error)

func load_characters():
	print("Loading characters...")
	current_request_type = RequestType.LOAD_CHARACTERS
	var error = http_request.request(API_BASE_URL + "/characters")
	if error != OK:
		print("Failed to load characters: ", error)

func send_message(message: String, callback: Callable):
	if not current_character or is_loading:
		print("Cannot send message: no character selected or already loading")
		return

	is_loading = true
	print("Sending message to ", current_character.name, ": ", message)

	var url = API_BASE_URL + "/chat"
	var headers = ["Content-Type: application/json"]

	var body = {
		"message": message,
		"character_id": current_character["npc_id"],
		"session_id": sessions.get(current_character["npc_id"], null)
	}

	current_request_type = RequestType.SEND_MESSAGE
	http_request.set_meta("callback", callback)

	var error = http_request.request(url, headers, HTTPClient.METHOD_POST, JSON.stringify(body))

	if error != OK:
		print("Failed to send message: ", error)
		is_loading = false
		callback.call(null, "Failed to send message")

func select_character(character):
	current_character = character
	print("Selected character: ", character.name, " (", character.id, ")")

# ============================================
# Response Handlers
# ============================================

func _on_request_completed(result, response_code, headers, body):
	if response_code != 200:
		print("Request failed with code: ", response_code)
		handle_request_error(response_code)
		return

	var json = JSON.new()
	var error = json.parse(body.get_string_from_utf8())

	if error != OK:
		print("Failed to parse JSON: ", error)
		return

	var data = json.data

	match current_request_type:
		RequestType.HEALTH_CHECK:
			handle_health_check(data)
		RequestType.LOAD_CHARACTERS:
			handle_characters_loaded(data)
		RequestType.SEND_MESSAGE:
			handle_message_response(data)


# func _on_evidence_request_completed(result, response_code, headers, body):
# 	if response_code != 200:
# 		print("Request failed with code: ", response_code)
# 		handle_request_error(response_code)
# 		return

# 	var json = JSON.new()
# 	var error = json.parse(body.get_string_from_utf8())

# 	if error != OK:
# 		print("Failed to parse JSON: ", error)
# 		return

# 	var data = json.data
	
# 	match current_request_type:
# 		RequestType.RETRIEVE_EVIDENCE:
# 			handle_evidence_retrieval(data)


func handle_health_check(data):
	if data.api == "healthy" and data.mongodb == "connected" and data.openai == "connected":
		print("✓ Server is healthy - loading characters...")
		load_characters()
	else:
		print("✗ Server has issues:", data)

func handle_characters_loaded(data):
	characters = data.characters
	print("Loaded ", characters.size(), " characters:")
	for character in characters:
		print("  - ", character.avatar, " ", character.name, " (", character.id, ")")

	if characters.size() > 0:
		select_character(characters[0])

func handle_message_response(data):
	if not sessions.has(current_character["npc_id"]):
		sessions[current_character["npc_id"]] = data.session_id
		print("New session created for ", current_character.name, ": ", data.session_id)

	print("Received response from ", current_character.name)

	if http_request.has_meta("callback"):
		var callback = http_request.get_meta("callback")
		callback.call(data.response, null)
		http_request.remove_meta("callback")

	is_loading = false

func handle_request_error(response_code):
	print("Request error: ", response_code)
	is_loading = false

	if http_request.has_meta("callback"):
		var callback = http_request.get_meta("callback")
		#callback.call(null, "Request failed with code: " + str(response_code))
		http_request.remove_meta("callback")

# ============================================
# Public API
# ============================================

func get_characters() -> Array:
	return characters

func get_current_character():
	return current_character

func is_ready() -> bool:
	return characters.size() > 0


# ============================================
# Gameplay Functionality
# ============================================

#signal on_player_talk

#signal on_npc_talk (npc_dialogue)

# append in-game NPCs to an array 
#func get_in_game_NPCs():
	#for npc in npc_scene.get_children():
		#if npc is NPC:
			#NPCs.append(npc)
			#print("npc name: " + npc.character_name)
			#print("npc id: " + npc.npc_id)

func enter_new_dialogue(npc: NPC):
	current_character = npc
	# dialogue_box.initialize_with_npc(npc) # not needed i think, i just need the dialogue box to show up
	print("currently in a conversation with: " + current_character.character_name)
	dialogue_box.visible = true;
	dialogue_box.start_dialogue_bgm()


	# HIDE / DISABLE WORLD
	if world_context:
		world_context.visible = false
		# disable_world_input()
		
	
	# Update the dialogue box UI
	dialogue_box.current_character = current_character
	dialogue_box.dialogue_text.text = "Now interviewing: " + current_character.character_name + "\n"
	dialogue_box.submit_button.disabled = false
	dialogue_box.talk_input.editable = true
	dialogue_box.talk_input.grab_focus()

	# Show NPC icon
	for icon in dialogue_box.npc_icons.get_children():
		icon.visible = false

	dialogue_box.current_icon = dialogue_box.npc_icons.get_node_or_null(npc.npc_id.capitalize())
	if dialogue_box.current_icon:
		dialogue_box.current_icon.visible = true
	
func exit_dialogue():
	current_character = null
	# select_character(null)
	dialogue_box.visible = false;
	
	# SHOW WORLD AGAIN
	if world_context:
		world_context.visible = true
	
	
func is_dialogue_active():
	return dialogue_box.visible
