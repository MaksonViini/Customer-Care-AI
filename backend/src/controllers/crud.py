from fastapi import APIRouter

from ..database import script_collection

router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)


class CrudDescription:
    @router.get("/v1/script")
    async def get_all():
        try:
            return script_collection.find_one({})
        except Exception:
            return False

    @router.post("/v1/script")
    async def create(args):
        try:
            script_collection.insert_one(args)
        except Exception:
            return False

    @router.put("/v1/script/{_id}")
    async def update():
        pass

    @router.delete("/v1/script/{_id}")
    async def delete():
        pass
