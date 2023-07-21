def message_serializer(data) -> dict:
    return {"message": str(data["message"])}


def data_serializer(data_all) -> list:
    return [message_serializer(data) for data in data_all]
