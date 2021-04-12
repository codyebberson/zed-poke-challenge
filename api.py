import sys
import flask
from flask import request, jsonify
import requests

def log(msg):
    print(msg, file=sys.stderr, flush=True)

class PokemonCollection:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.members = []

    def add(self, pokemon):
        if len(self.members) >= self.capacity:
            return False
        self.members.append(pokemon)
        return True

    def remove(self, pokeAPI_id):
        for i in range(len(self.members)):
            if str(self.members[i]["pokeAPI_id"]) == str(pokeAPI_id):
                result = self.members[i]
                del self.members[i]
                return result
        return None

def to_json(collection):
    return jsonify({"id": collection.id, "members": collection.members})

app = flask.Flask(__name__)
app.config["DEBUG"] = True

pokemon = dict()
storage = dict()
party = PokemonCollection('party', 6)
storage['party'] = party

@app.route("/api/v1/pokemon/<id>")
def get_pokemon(id):
    if id not in pokemon:
        orig = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(id)).json()

        simple = {
            "pokeAPI_id": id,
            "name": orig["name"],
            "height": orig["height"],
            "weight": orig["weight"],
            "base_happiness": 0,
            "type_1_name": "foo",
            "type_1_generation": "foo",
            "type_2_name": "foo",
            "type_2_generation": "foo",
        }

        species = requests.get(orig["species"]["url"]).json()
        simple["base_happiness"] = species["base_happiness"]

        type1 = requests.get(orig["types"][0]["type"]["url"]).json()
        simple["type_1_name"] = type1["name"]
        simple["type_1_generation"] = type1["generation"]["name"]

        if len(orig["types"]) > 1:
            type2 = requests.get(orig["types"][1]["type"]["url"]).json()
            simple["type_2_name"] = type2["name"]
            simple["type_2_generation"] = type2["generation"]["name"]

        pokemon[id] = simple
    return pokemon[id]

@app.route("/api/v1/party", methods=["GET"])
def read_party():
    return to_json(storage["party"])

@app.route("/api/v1/party/members", methods=["POST"])
def add_party_member():
    body = request.json
    if "pokeAPI_id" not in body:
        return "Missing pokeAPI_id", 400
    if not party.add(get_pokemon(body["pokeAPI_id"])):
        return "Party full", 400
    return to_json(party)

@app.route("/api/v1/party/members/<pokeAPI_id>", methods=["DELETE"])
def delete_party_member(pokeAPI_id):
    if party.remove(pokeAPI_id) is None:
        return "Party does not contain pokemon", 400
    return to_json(party)

@app.route("/api/v1/boxes", methods=["POST"])
def create_box():
    id = str(len(storage))
    storage[id] = PokemonCollection(id, 30)
    return to_json(storage[id])

@app.route("/api/v1/boxes/<id>", methods=["GET"])
def read_box(id):
    if id not in storage:
        return "Box not found", 404
    return to_json(storage[id])

@app.route("/api/v1/boxes/<id>/members", methods=["POST"])
def add_box_member(id):
    if id not in storage:
        return "Box not found", 404
    box = storage[id]
    body = request.json
    if "pokeAPI_id" not in body:
        return "Missing pokeAPI_id", 400
    if not box.add(get_pokemon(body["pokeAPI_id"])):
        return "Box full", 400
    return to_json(box)

@app.route("/api/v1/boxes/<id>/members/<pokeAPI_id>", methods=["DELETE"])
def delete_box_member(id, pokeAPI_id):
    if id not in storage:
        return "Box not found", 404
    box = storage[id]
    if box.remove(pokeAPI_id) is None:
        return "Box does not contain pokemon", 400
    return to_json(box)

@app.route("/api/v1/move", methods=["POST"])
def move_member():
    body = request.json
    if "src_id" not in body:
        return "Missing source collection ID (src_id)", 400
    if "dst_id" not in body:
        return "Missing destination collection ID (dst_id)", 400
    if "pokeAPI_id" not in body:
        return "Missing pokemon ID (pokeAPI_id)", 400
    src_id = str(body["src_id"])
    if src_id not in storage:
        return "Source collection not found", 404
    dst_id = str(body["dst_id"])
    if dst_id not in storage:
        return "Destination collection not found", 404
    source = storage[src_id]
    destination = storage[dst_id]
    pokeAPI_id = body["pokeAPI_id"]
    pokemon = source.remove(pokeAPI_id)
    if pokemon is None:
        return "From collection does not contain pokeAPI_id", 400
    if not destination.add(pokemon):
        source.add(pokemon)
        return "Destination collection is full", 400
    return "OK", 200

app.run()
