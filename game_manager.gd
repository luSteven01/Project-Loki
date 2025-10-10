extends Node

var API_KEY : String = ""
var URL : String = "https://api.openai.com/v1/chat/completions"

# This is defines how consistent or sporadic the
# generation is going to be 
var TEMPERATURE : float = 0.5 

# Maximum amount of tokens that we can use
var MAX_TOKENS : int = 1024 

#The model of GPT we are using
var MODEL: String = "gpt-4o-mini"

# An array of past messages that keeps track of our messages.
# This will be used to send all of our chat history 
var messages = []

# This is a node of Godot, that manages 
# sending and receiving information to the API
var request: HTTPRequest

# This function has our HTTP Request Node set up so that once we 
# receive information from any request, we are going to call 
# _on_request_completed
func _ready() -> void:
	# Load API key
	API_KEY = load_env(".env", "OPENAI_API_KEY")
	if API_KEY == "":
		push_error("API key not found")
	#print(API_KEY) # For debug

	request = HTTPRequest.new() # Create a new HTTPRequest node
	add_child(request) # Add that node we created as a child to scene
	
	#dialogue_request("Hello fuck!")
	
	# With the node, it will connect it's "request_completed" signal to our _on_request_completed
	# function. That means that once an API request has been received by the AI, the function
	# will call
	request.connect("request_completed", _on_request_completed)
	
	
# This function is going to include our dialogue request that we are 
# sending to the OpenAI API.
func dialogue_request(player_dialogue):
	# This means that the format that we are sending 
	# and being returned will be of type json.
	var headers = ["Content-type: application/json", "Authorization: Bearer " + API_KEY] 
	
	# This adds a new object to messages array, 
	# containing the role and content of the request.
	messages.append({
		"role": "user",
		"content": player_dialogue
	})

	# We are defining our body here for the API call. All objects that we add 
	# inside of this body will be turned into JSON format for the API requirement
	# Essentially the meat the of API call.
	var body = JSON.stringify({
		"messages" : messages,
		"temperature": TEMPERATURE,
		"max_tokens":  MAX_TOKENS,
		"model": MODEL
	})

	# After getting the body, we now have to send the request. We want to use the 
	# POST method because we are posting data to the API.
	var send_request = request.request(URL, headers, HTTPClient.METHOD_POST, body)
	
	# Error checking to see if send_request failed.
	if send_request != OK:
		print("There was an error!")
		

func _on_request_completed(result, response_code, headers, body):
	
	# This is going to convert the body to JSON format
	var json = JSON.new()
	var parse_result = json.parse(body.get_string_from_utf8())
	var response = json.get_data()
	
		# Check if JSON parsing was successful
	if parse_result != OK:
		print("Error parsing JSON!")
		return

	# Check if the response dictionary contains an 'error' key
	if response.has("error"):
		print("API Error: ", response["error"]["message"])
		
	# If no error, it's safe to get the message
	elif response.has("choices"):
		# When accessing the message the AI sent, we look at:
		# 1. The choices list
		# 2. We select the 1st choice
		# 3. Get the data of the message.
		# 4. Then finally get the content of the message we selected.
		var message = response["choices"][0]["message"]["content"]
		#print(message) # for debug
		
		# Get DialogueBox node
		var dialogue_box = get_node("/root/Main/CanvasLayer/DialogueBox")

		# Start NPC talking animation
		dialogue_box.start_npc_talk()
		
		# Append NPC response to DialogueText
		dialogue_box.dialogue_text.text += "\n[b][NPC]:[/b]"
		await dialogue_box.type_text_slowly(message)
		
		# Stop animation when done typing
		dialogue_box.stop_npc_talk()

		# Optional: auto-scroll to bottom
		dialogue_box.dialogue_text.scroll_to_line(dialogue_box.dialogue_text.get_line_count() - 1)
	else:
		print("Received an unknown response format.")

# Utility to load keys from .env	
func load_env(path: String, key: String) -> String:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return ""
	var content = file.get_as_text().split("\n")
	for line in content:
		line = line.strip_edges()
		if line.begins_with(key + "="):
			return line.replace(key + "=", "").strip_edges()
	return ""		
	
