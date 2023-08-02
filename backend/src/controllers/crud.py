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
        try:
            script_collection.insert_one(dict(args))
            return {"status": "Script inserted successfully."}
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Error inserting script."
            ) from e

    @router.post("/v1/script/insert-many")
    async def insert_many(args_list: List[dict]):
        try:
            script_collection.insert_many(args_list)

            return {"status": "Script inserted successfully."}
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error inserting multiple scripts. {e}"
            ) from e

    @router.put("/v1/script/{_id}")
    async def update(_id: str, args: dict):
        try:
            script_collection.update_one({"_id": _id}, {"$set": args})
            return {"message": "Script updated successfully."}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error updating script.") from e

    @router.delete("/v1/script/{_id}")
    async def delete(_id: str):
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
        try:
            script_collection.drop()
            return {"message": "All scripts deleted successfully."}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error deleting script.") from e


class CrudMessages:
    @router.get("/v1/message")
    async def get_all():
        try:
            scripts = list(conversations_collection.find({}))
            serialized_scripts = json_util.dumps(scripts, default=json_util.default)
            return {"scripts": serialized_scripts}
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Error retrieving scripts."
            ) from e

    @router.delete("/v1/message/")
    async def delete_many():
        try:
            result = conversations_collection.drop()
            if result.deleted_count == 1:
                return {"message": "All scripts deleted successfully."}
            else:
                raise HTTPException(status_code=404, detail="Script not found.")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error deleting script.") from e
