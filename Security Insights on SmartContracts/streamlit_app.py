import os
import streamlit as st
import tempfile
from dotenv import load_dotenv
from smart_contract_explainer import (
    analyze_contract_from_address,
    analyze_contract_from_source,
    is_valid_address
)

# Load environment variables
load_dotenv()

# page configuration
st.set_page_config(
    page_title="Smart Contract Explainer",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #bdbdbd;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #000000;
        border-left: 5px solid #17a2b8;
        padding: 1rem;
        border-radius: 0.25rem;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 0.25rem;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    .output-container {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 0.25rem;
        border: 1px solid #dee2e6;
        margin-top: 1rem;
    }
    .footer {
        margin-top: 2rem;
        text-align: center;
        color: #7f8c8d;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="main-header">Smart Contract Explainer</div>', unsafe_allow_html=True)
    
    # Info box
    st.markdown(
        '<div class="info-box">This tool provides plain-English explanations of Ethereum smart contracts. '
        'You can input a contract address (Sepolia testnet) or raw Solidity code.</div>',
        unsafe_allow_html=True
    )
    
    # Input tabs
    tab1, tab2, tab3 = st.tabs(["Contract Address", "Solidity Code", "Upload File"])
    
    with tab1:
        st.markdown('<div class="sub-header">Analyze by Contract Address</div>', unsafe_allow_html=True)
        address = st.text_input("Enter Sepolia testnet contract address (0x...)")
        address_submit = st.button("Analyze Contract", key="address_btn")
        
        if address_submit:
            if not address:
                st.error("Please enter a contract address")
            elif not is_valid_address(address):
                st.error("Invalid Ethereum address format")
            else:
                with st.spinner("Analyzing contract..."):
                    try:
                        explanation = analyze_contract_from_address(address)
                        display_output(explanation)
                    except Exception as e:
                        st.error(f"Error analyzing contract: {str(e)}")
    
    with tab2:
        st.markdown('<div class="sub-header">Analyze Solidity Code</div>', unsafe_allow_html=True)
        code = st.text_area("Paste Solidity code here", height=300)
        code_submit = st.button("Analyze Code", key="code_btn")
        
        if code_submit:
            if not code:
                st.error("Please enter Solidity code")
            else:
                with st.spinner("Analyzing code..."):
                    try:
                        explanation = analyze_contract_from_source(code)
                        display_output(explanation)
                    except Exception as e:
                        st.error(f"Error analyzing code: {str(e)}")
    
    with tab3:
        st.markdown('<div class="sub-header">Upload Solidity File</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose a Solidity file", type=["sol"])
        file_submit = st.button("Analyze File", key="file_btn")
        
        if file_submit:
            if not uploaded_file:
                st.error("Please upload a file")
            else:
                with st.spinner("Analyzing file..."):
                    try:
                        # Save the file temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".sol") as tmp:
                            tmp.write(uploaded_file.getvalue())
                            tmp_path = tmp.name
                        
                        # Read the file
                        with open(tmp_path, 'r') as f:
                            code = f.read()
                        
                        # Clean up
                        os.unlink(tmp_path)
                        
                        # Analyze the code
                        explanation = analyze_contract_from_source(code)
                        display_output(explanation)
                    except Exception as e:
                        st.error(f"Error analyzing file: {str(e)}")
    
    # Footer
    st.markdown(
        '<div class="footer">Smart Contract Explainer Tool - Created with Streamlit, Web3, and OpenAI</div>',
        unsafe_allow_html=True
    )

def display_output(explanation):
    st.markdown("## Contract Analysis:")


    st.markdown(
    f"""
    <div class="output-container">
        {explanation}
    </div>
    """,
    unsafe_allow_html=True
    )
    
    # Add export options
    st.download_button(
        label="Download Analysis",
        data=explanation,
        file_name="contract_analysis.md",
        mime="text/markdown"
    )

if __name__ == "__main__":
    main()
