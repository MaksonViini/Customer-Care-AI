from typing import List

from bson import ObjectId, json_util
from fastapi import APIRouter, HTTPException

from ..database import conversations_collection, script_collection

router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)

class CrudDescription:
    @router.get("/v1/script")
    async def get_all():
        """
        Get all scripts.

        Returns:
            dict: A dictionary containing serialized scripts.
        """
        try:
            scripts = list(script_collection.find({}))
            serialized_scripts = json_util.dumps(scripts, default=json_util.default)
            return {"scripts": serialized_scripts}
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Error retrieving scripts."
            ) from e

    @router.post("/v1/script")
    async def insert(args: dict):
        """
        Insert a script.

        Args:
            args (dict): The script data.

        Returns:
            dict: A dictionary indicating the insertion status.
        """
        try:
            script_collection.insert_one(dict(args))
            return {"status": "Script inserted successfully."}
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Error inserting script."
            ) from e


    @router.post("/v1/script/insert-many")
    async def insert_many(args_list: List[dict]):
        """
        Insert many scripts.

        Args:
            args (list): List of the script data.

        Returns:
            dict: A dictionary indicating the insertion status.
        """
        try:
            script_collection.insert_many(args_list)

            return {"status": "Script inserted successfully."}
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error inserting multiple scripts. {e}"
            ) from e

    @router.put("/v1/script/{_id}")
    async def update(_id: str, args: dict):
        """
        Update a script.

        Args:
            _id (str): The ID of the script to be updated.
            args (dict): The updated script data.

        Returns:
            dict: A dictionary indicating the update status.
        """
        try:
            script_collection.update_one({"_id": _id}, {"$set": args})
            return {"message": "Script updated successfully."}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error updating script.") from e

    @router.delete("/v1/script/{_id}")
    async def delete(_id: str):
        """
        Delete a script.

        Args:
            _id (str): The ID of the script to be deleted.

        Returns:
            dict: A dictionary indicating the deletion status.
        """
        try:
            result = script_collection.delete_one({"_id": ObjectId(_id)})
            if result.deleted_count == 1:
                return {"message": "Script deleted successfully."}
            else:
                raise HTTPException(status_code=404, detail="Script not found.")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error deleting script.") from e

    @router.delete("/v1/script/delete-many")
    async def delete_many():
        """
        Delete all messages.

        Returns:
            dict: A dictionary indicating the deletion status.
        """
        try:
            script_collection.drop()
            return {"message": "All scripts deleted successfully."}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error deleting script.") from e


class CrudMessages:
    @router.get("/v1/message")
    async def get_all():
        """
        Get all messages.

        Returns:
            dict: A dictionary containing serialized messages.
        """
        try:
            messages = list(conversations_collection.find({}))
            serialized_messages = json_util.dumps(messages, default=json_util.default)
            return {"messages": serialized_messages}
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Error retrieving messages."
            ) from e

    @router.delete("/v1/message/")
    async def delete_many():
        """
        Delete all messages.

        Returns:
            dict: A dictionary indicating the deletion status.
        """
        try:
            result = conversations_collection.drop()
            if result.deleted_count == 1:
                return {"message": "All messages deleted successfully."}
            else:
                raise HTTPException(status_code=404, detail="Messages not found.")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error deleting messages.") from e
