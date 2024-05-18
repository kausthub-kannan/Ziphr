import ezkl
import os
from fastapi import FastAPI, Request
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Verifier:
    def __init__(self, settings_path, vk_path, proof_path):
        self.settings_path = os.path.join(settings_path)
        self.vk_path = os.path.join(vk_path)
        self.proof_path = os.path.join(proof_path)

    def verify(self):
        logger.info("ZK Verification started...")
        if ezkl.verify(
                self.proof_path,
                self.settings_path,
                self.vk_path,
        ):
            logger.info("Model has been verified")
            return {"status": 200, "message": "Model has been verified"}
        else:
            logger.info("Access Denied")
            return {"status": 500, "message": "Access Denied"}


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/verify")
async def verify(proof: Request):
    proof_js = await proof.json()
    with open("client_proof.json", "w") as json_proof:
        json.dump(proof_js, json_proof, ensure_ascii=False)

    verifier = Verifier("settings.json", "test.vk", "client_proof.json")
    vk_status = verifier.verify()

    return vk_status
