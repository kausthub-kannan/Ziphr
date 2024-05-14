import ezkl
import os


class Verifier:
    def __init__(self, settings_path, vk_path, proof_path):
        self.settings_path = os.path.join(settings_path)
        self.vk_path = os.path.join(vk_path)
        self.proof_path = os.path.join(proof_path)

    async def verify(self):
        if ezkl.verify(
                self.proof_path,
                self.settings_path,
                self.vk_path,
        ):
            return {"status": 200, "message": "Model has been verified"}
        else:
            return {"status": 500, "message": "Access Denied"}
