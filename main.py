import streamlit as st
from utils import run_async
import warnings

from zkml_middleware.prover import Prover
from zkml_middleware.verifier import Verifier

warnings.filterwarnings("ignore", message="RuntimeWarning: Enable tracemalloc to get the object allocation traceback")

st.set_page_config("Ziphr")
st.title("Ziphr")
st.markdown("")

if st.button("Prove Model"):
    try:
        print("INFO | ZKML Authentication Started")
        prover = Prover()
        proof = run_async(prover.generate_proof())
        print("INFO | ZK Proof Generated \n")
        print("INFO | ZK Verification started...")
        verifier = Verifier(
            prover.settings_path,
            prover.vk_path,
            prover.proof_path
        )
        verification = run_async(verifier.verify())
        if verification:
            st.write("The model is verified")
    except Exception as e:
        print("ERROR | SETUP FAILED | " + str(e))
