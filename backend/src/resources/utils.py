from ..database import conversations_collection, script_collection


def get_dialog_by_index(index: int):
    return script_collection.find_one({"problem.id": index})


def get_last_step(existing_dialog):
    if existing_dialog and "conversation" in existing_dialog:
        return existing_dialog["conversation"][-1]["step"]
    return False


def create_conversation(data, most_similar_index, user_id):
    bot_response = get_dialog_by_index(most_similar_index)["script"][0]["message"]
    new_document = {
        "step": 1,
        "user_message": data.get("message"),
        "bot_response": bot_response,
    }
    user_dialog = {
        "dialog_id": most_similar_index,
        "user_id": user_id,
        "conversation": [new_document],
    }
    conversations_collection.insert_one(user_dialog)
    return new_document
