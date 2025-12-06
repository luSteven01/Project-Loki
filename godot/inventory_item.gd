# want texture of sprite2D node = texture assigned in edtior. use @tool annotation to be able to see changes to texture
# in editor and in-game. when we change it, can see icon image change in real-time 
#@tool 
extends Node2D

# type: categorize item; executes logic for item
# name: identifier; displayed when player hovers over it
# effect: describes what it does when used/equipped
# texture: visual representation of item in the game
@export var evidence_id = ""
#var evidence_name = ""
#var evidence_owner = ""
#var evidence_description = ""
#var evidence_location = ""
#@export var evidence_texture = Texture
#@export var evidence_hashcode = ""

# static; used to spawn items from scene onto main scene on load
var scene_path = "res://inventory_item.tscn"

# enable item to spawn w/ different sprite texture
@onready var icon_sprite = $Sprite2D


# if player is in range, set to true bc they are overlapping w/ collision. otherwise, false 
var player_in_range = false

func _ready():
	#assign texture property to sprite2D node if we are still not in editor; texture reflects in game itself
	#if not Engine.is_editor_hint():

		if evidence_id != "" and GameManager.evidence_list.has(evidence_id):
			var evidence = GameManager.evidence_list[evidence_id]
			
			evidence_id = evidence["id"]
			#evidence_name = evidence["name"]
			#evidence_owner = evidence["belongs_to"]
			#evidence_description = evidence["description"]
			#evidence_location = evidence["location"]
			#
			#print(evidence_id + ", " + evidence_name + ", " + evidence_owner + ", " + evidence_description + ", " + evidence_location)
		#
		#icon_sprite.texture = evidence_texture
	
	
	

# in process func, assign texture property to sprite2D node if we are still in the editor
# icon updates and shows correct icon while we are still in the edtior
# when we assign diff texture properties in main scene, updates in edtior & when we run the scene
func _process(delta):
	#if Engine.is_editor_hint():
		#icon_sprite.texture = evidence_texture
		
	# add item to inventory when E is pressed
	if player_in_range and Input.is_action_just_pressed("ui_add"):
		pickup_item()

# creates dictionary that represents item w/ all of its properties; called when we ui_add input	& add item to inventory
func pickup_item():
	var item = {
		"quantity": 1,
		"id": evidence_id,
		#"name": evidence_name,
		#"texture": evidence_texture,
		#"owner": evidence_owner,
		#"description": evidence_description,
		#"location": evidence_location,
		"scene_path": scene_path,
	}
	# Call add_item func from global script; pass item dictionary as parameter
	# after adding, remove item from scene using queue_free()
	if Global.player_node:
		Global.add_item(item)
		self.queue_free()


func _on_area_2d_body_entered(body: Node2D) -> void:
	if body.is_in_group("Player"):
		player_in_range = true
		body.interact_ui.visible = true


func _on_area_2d_body_exited(body: Node2D) -> void:
	if body.is_in_group("Player"):
		player_in_range = false
		body.interact_ui.visible = false

# item data
func set_item_data(data):
	evidence_id = data["id"]
	#evidence_name = data["name"]
	#evidence_owner = data["owner"]
	#evidence_texture = data["texture"]
	 #scene_path = data["scene_path"]
	#evidence_description = data["description"]
	#evidence_location = data["location"]

func initiate_items(id, itemName, itemOwner, texture, description, location):
	evidence_id = id
	#evidence_name = itemName
	#evidence_owner = itemOwner
	#evidence_texture = texture
	#evidence_description = description
	#evidence_location = location
	#
	
