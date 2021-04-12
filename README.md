# Zed Pokemon Challenge

Get the current party:

```
curl http://localhost:5000/api/v1/party
```

Add a pokemon to the party:

```
curl -X POST -H 'Content-Type: application/json' -d '{"pokeAPI_id":1}' http://localhost:5000/api/v1/party/members
```

Create a box:

```
curl -X POST -H 'Content-Type: application/json' -d '' http://localhost:5000/api/v1/boxes
```

Get a box by ID:

```
curl http://localhost:5000/api/v1/boxes/1
```

Add a pokemon to a box:

```
curl -X POST -H 'Content-Type: application/json' -d '{"pokeAPI_id":2}' http://localhost:5000/api/v1/boxes/1/members
```

Remove a pokemon from a box:

```
curl -X DELETE http://localhost:5000/api/v1/boxes/1/members/2
```

Move a pokemon from one box to another box:

```
curl -X POST -H 'Content-Type: application/json' -d '{"src_id":1,"dst_id":2,"pokeAPI_id":2}' http://localhost:5000/api/v1/move
```

Move a pokemon from one box to the party:

```
curl -X POST -H 'Content-Type: application/json' -d '{"src_id":2,"dst_id":"party","pokeAPI_id":3}' http://localhost:5000/api/v1/move
```

Move a pokemon from the party to a box:

```
curl -X POST -H 'Content-Type: application/json' -d '{"src_id":"party","dst_id":1,"pokeAPI_id":3}' http://localhost:5000/api/v1/move
```
