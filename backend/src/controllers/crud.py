from fastapi import APIRouter

from ..database import description_colletion, script_collection

router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)


class CrudDescription:
    @router.get("/v1/description")
    async def get_all():
        try:
            return description_colletion.find_one({})
        except Exception:
            return False

    @router.post("/v1/description")
    async def create(args):
        try:
            description_colletion.insert_one(args)
        except Exception:
            return False

    @router.put("/v1/description/{_id}")
    async def update():
        pass

    @router.delete("/v1/description/{_id}")
    async def delete():
        pass


class CrudScript:
    @router.get("/v1/script")
    async def get_all():
        try:
            return script_collection.find_one({})
        except Exception:
            return False

    @router.get("/v1/script/{_id}")
    async def get_by_id(_id):
        pass

    @router.post("/v1/script")
    async def create():
        pass

    @router.put("/v1/script/{_id}")
    async def update():
        pass

    @router.delete("/v1/script/{_id}")
    async def delete():
        pass
