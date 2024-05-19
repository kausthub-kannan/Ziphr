import asyncio
import json
import logging

import streamlit as st
import warnings
import requests

from zkml.prover.prover import Prover
from zkml.verifier.verifier import Verifier


async def main():
    warnings.filterwarnings("ignore",
                            message="RuntimeWarning: Enable tracemalloc to get the object allocation traceback")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    st.set_page_config("Ziphr")
    st.title("Ziphr")
    st.markdown("")

    if st.button("Prove Model"):
        try:
            prover = Prover()
            proof = await prover.generate_proof()
            if 'status' not in proof.keys():

                with open(prover.proof_path, 'r') as f:
                    proof_data = json.load(f)

                data = json.dumps(proof_data)

                verification_status = requests.post("http://127.0.0.1:8000/verify", data=data).json()
                logger.info(verification_status['message'])
                st.write(verification_status['message'])

            else:
                error_msg = proof["message"]
                logger.error(f"ZK Proof Generation Failed | {error_msg}")

        except Exception as e:
            logger.error(f"ZK Proof Generation or Verification Failed | {str(e)}")
            logger.error("ERROR | SETUP FAILED | " + str(e))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
