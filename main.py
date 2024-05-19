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
    content = f"""Name: {data["name"]} \n
    Age: {data["age"]} \n
    Sex:  {data["sex"]} \n
    Address: {data["address"]} \n
    Crime: {data["crime"]} \n
    Arrest Date: {data["arrest_date"]} \n
    """
    st.markdown(content)


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
    st.warning("Wrong Prove model is for development phase only")

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

                if verification_status["status"]==200:
                    data = {
                        "message": verification_status['message'],
                        "name": "John Doe",
                        "sex": "Male",
                        "age": "25",
                        "arrest_date": "2021-09-01",
                        "crime": "Theft",
                        "address": "1234, Main Street, New York",
                    }
                    data_display(data)
                else:
                    access_denied_display()

            else:
                error_msg = proof["message"]
                access_denied_display()
                logger.error(f"ZK Proof Generation Failed | {error_msg}")

        except Exception as e:
            logger.error(f"ZK Proof Generation or Verification Failed | {str(e)}")
            logger.error("ERROR | SETUP FAILED | " + str(e))

    if st.button("Wrong Prove Model"):
        try:
            prover = Prover()
            proof = await prover.generate_proof()
            if 'status' not in proof.keys():

                with open(prover.proof_path, 'r') as f:
                    proof_data = json.load(f)

                data = json.dumps(proof_data)

                verification_status = requests.post("http://127.0.0.1:8000/wrong_verify", data=data).json()
                logger.info(verification_status['message'])
                access_denied_display()

            else:
                error_msg = proof["message"]
                access_denied_display()
                logger.error(f"ZK Proof Generation Failed | {error_msg}")

        except Exception as e:
            logger.error(f"ZK Proof Generation or Verification Failed | {str(e)}")
            logger.error("ERROR | SETUP FAILED | " + str(e))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
