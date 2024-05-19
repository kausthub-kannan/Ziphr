import asyncio
import json
import logging

import streamlit as st
import warnings
import requests

from zkml.prover.prover import Prover
from zkml.verifier.verifier import Verifier


def data_display(data):
    st.success(data["message"])


def access_denied_display():
    display_text = """
     Access Denied
     
     The verifier has denied access to the model. This can be either due the below possibilities:
        1. The proof has been tampered .i.e the proving key is not authentic to the model weights . \n
        2. The model has been tampered .i.e the model is not authentic to the proving key. Hence verifier has denied 
         access to the data.
     """
    st.error(display_text)


async def main():
    warnings.filterwarnings("ignore",
                            message="RuntimeWarning: Enable tracemalloc to get the object allocation traceback")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    st.set_page_config("Ziphr")
    st.title("Ziphr")
    st.write("ZKML based database and model authenticator")
    st.markdown("")
    st.info("""Ziphr is based on ZKML tool. Currently due to lack of availability of deployment of the verifier as edge
            function, the verifier has to be run locally.
            The future of the project is to deploy it on Azure functions""", icon="ℹ️")

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
                access_denied_display()
                logger.error(f"ZK Proof Generation Failed | {error_msg}")

        except Exception as e:
            logger.error(f"ZK Proof Generation or Verification Failed | {str(e)}")
            logger.error("ERROR | SETUP FAILED | " + str(e))


    data ={
    "message": "Model has been verified"
    }
    data_display(data)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
