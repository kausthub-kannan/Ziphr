import os
import ezkl
from zkml_middleware.ezkl_setup import ZZK


class Prover(ZZK):
    def __init__(self):
        ZZK.__init__(self)

    async def generate_proof(self):
        try:
            ezkl.gen_witness(self.data_path, self.compiled_model_path, self.witness_path)
            proof = ezkl.prove(
                self.witness_path,
                self.compiled_model_path,
                self.pk_path,
                self.proof_path,
            )
            return proof
        except Exception:
            return {"status": 401, "message": "Proof could not be generated."}
