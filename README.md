# Ziphr
Securing confidential data in a database using a ZKML-based cryptographic approach with auto-encoder-based encoding

![ziphr](assets/ZKML-ENC.png)

## Local Setup
Clone the repository and install the required packages using poetry and follow the below steps:

1. Setup ZKML using ezkl:
```bash
python zkml/setup/ezkl_setup.py 
```

2. Run Clinet (Streamlit):
```bash
streamlit run main.py
```

3. Run Verifier Server (FastAPI):
```bash
# Run the verifier server on cloud
uvicorn verifier:app --reload

# Note: Run the below command for developer mode
fastapi dev zkml/verifier/verifier.py
```

