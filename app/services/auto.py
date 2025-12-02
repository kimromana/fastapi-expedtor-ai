def create_service(repository):

    class GenericService:
        def __init__(self):
            self.repo = repository

        def list(self, db, **kwargs):
            return self.repo.get_list(db, **kwargs)

        def get(self, db, obj_id):
            return self.repo.get(db, obj_id)

        def create(self, db, data: dict):
            return self.repo.create(db, data)

        def patch(self, db, obj_id, data: dict):
            return self.repo.patch(db, obj_id, data)

        def delete(self, db, obj_id):
            return self.repo.delete(db, obj_id)

    return GenericService()
