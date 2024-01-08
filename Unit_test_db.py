import db

db = db.DB()


def test_register():
    accounts_no = db.db.accounts.count_documents({})
    db.register("testAccount", 123)
    new_accounts_no = db.db.accounts.count_documents({})
    db.db.accounts.delete_one({"username": "testAccount"}) # Cleaning the db after testing
    assert (new_accounts_no - accounts_no )==1, "Test Register"

def test_create_chatroom():
    rooms_no = db.db.rooms.count_documents({})
    db.create_chatroom("testRoom")
    new_rooms_no = db.db.rooms.count_documents({})
    db.db.rooms.delete_one({"name": "testRoom"}) # Cleaning the db after testing
    assert (new_rooms_no - rooms_no )==1, "Test Create Chatroom"

def test_is_room_exist():
    db.create_chatroom("testRoom")
    assert db.is_room_exist("testRoom")
    db.db.rooms.delete_one({"name": "testRoom"})


def test_is_user_in_room_exist():
    rooms_no = db.db.rooms.count_documents({})
    db.create_chatroom("testRoom")
    new_rooms_no = db.db.rooms.count_documents({})
    assert (new_rooms_no - rooms_no )==1, "Test Create Chatroom"

    accounts_no = db.db.accounts.count_documents({})
    db.register("testAccount", 123)
    new_accounts_no = db.db.accounts.count_documents({})
    assert (new_accounts_no - accounts_no )==1, "Test Register"
    
    db.join_room("testRoom", "testAccount")
    
    room = db.db.rooms.find_one({"name" : "testRoom"})
    users_in_room: [str] = room["users"]
    
    assert ("testAccount" in users_in_room) == db.is_user_in_room_exist("testRoom", "testAccount")
    db.db.accounts.delete_one({"username": "testAccount"}) # Cleaning the db after testing
    db.db.rooms.delete_one({"name": "testRoom"}) # Cleaning the db after testing

    


def test_join_room():
    rooms_no = db.db.rooms.count_documents({})
    db.create_chatroom("testRoom")
    new_rooms_no = db.db.rooms.count_documents({})
    assert (new_rooms_no - rooms_no )==1, "Test Create Chatroom"

    accounts_no = db.db.accounts.count_documents({})
    db.register("testAccount", 123)
    new_accounts_no = db.db.accounts.count_documents({})
    assert (new_accounts_no - accounts_no )==1, "Test Register"
    
    db.join_room("testRoom", "testAccount")
    
    room = db.db.rooms.find_one({"name" : "testRoom"})
    users_in_room: [str] = room["users"]
    
    assert ("testAccount" in users_in_room)
    db.db.accounts.delete_one({"username": "testAccount"}) # Cleaning the db after testing
    db.db.rooms.delete_one({"name": "testRoom"}) # Cleaning the db after testing



def test_logout():
    online_no = db.db.accounts.count_documents({})
    db.register("testAccount", 123)
    new_online_no = db.db.accounts.count_documents({})
    assert (new_online_no - online_no )==1, "Test Register"

    db.user_login("testAccount", "0.0.0.0", 3000)

    online_no = db.db.online_peers.count_documents({})
    db.user_logout("testAccount")
    new_online_no = db.db.online_peers.count_documents({})
    assert (new_online_no - online_no )==-1, "Test Register"
    
    