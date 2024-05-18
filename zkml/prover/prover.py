import ezkl
import os
from zkml.setup.ezkl_setup import ZZK


class Prover(ZZK):
    def __init__(self):
        ZZK.__init__(self)
        self.witness_path = os.path.join('zkml/prover/witness.json')
        self.proof_path = os.path.join('zkml/prover/proof.json')

    async def generate_proof(self):
        try:
            ezkl.gen_witness("zkml/setup/" + self.data_path, "zkml/setup/" + self.compiled_model_path, self.witness_path)
            proof = ezkl.prove(
                self.witness_path,
                "zkml/setup/" + self.compiled_model_path,
                "zkml/setup/" + self.pk_path,
                self.proof_path,
            )
            return proof
        except Exception as e:
            return {"status": 401, "message": f"Proof could not be generated. {e}"}
