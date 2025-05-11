import streamlit as st
import openai
import os
import time
from dotenv import load_dotenv



load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


# page configuration
st.set_page_config(
    page_title="Solidity Smart Contract Generator",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper function for OpenAI API 
def generate_contract_with_openai(prompt, api_key):
    try:
        code_prompt = f"""You are an expert Solidity developer tasked with creating secure, minimal smart contracts.
        
Generate Solidity code based on this requirement: "{prompt}"

Follow these guidelines:
1. Use Solidity ^0.8.0 or higher and prioritize gas efficiency  
2. Avoid unsafe patterns like `tx.origin`, `call.value`, `delegatecall`, and `selfdestruct`  
3. Leverage OpenZeppelin contracts (e.g., Ownable, ReentrancyGuard, ERC20) where applicable  
4. Implement strong access control and input validation  
5. Emit events for key state changes and guard against reentrancy in Ether transfers  
6. Return only the complete, minimal, well-commented contract — no extra text or markdown


Return ONLY the complete Solidity code without explanations.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are an expert Solidity developer. You write secure, gas-efficient, and production-ready smart contracts "
                        "that follow best practices, including input validation, access control, events for key state changes, and "
                        "clear, maintainable structure. Your code adheres to the latest Solidity version, uses OpenZeppelin contracts where appropriate, "
                        "and includes inline comments for clarity."
                        "You only write safe, production-ready contracts and avoid any insecure or deprecated practices."
                        
                        )},
                {"role": "user", "content": code_prompt}

                # {"role": "system", "content": "You are an expert Solidity developer who writes secure, efficient and production-ready smart contracts."},
                # {"role": "user", "content": code_prompt}
            ],
            temperature=0.2,
            max_tokens=2000
        )
        
        solidity_code = response.choices[0].message.content.strip()
        
        # Then, generate security considerations
        security_prompt = f"""You are a blockchain security auditor. Examine this Solidity code and provide EXACTLY 5 key security considerations that were addressed in the implementation.

{solidity_code}

Format your response as a numbered list of 5 brief bullet points (1-2 sentences each), focusing ONLY on security aspects that were properly handled in the code (not suggestions for improvement).
"""

        security_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert blockchain security auditor."},
                {"role": "user", "content": security_prompt}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        
        security_considerations = security_response.choices[0].message.content.strip()
        
        return solidity_code, security_considerations
        
    except Exception as e:
        st.error(f"Error generating code: {str(e)}")
        return None, None

# Example prompts
example_prompts = [
    "Create an ERC-20 token with minting restricted to addresses in an allowlist",
    "Build a simple NFT marketplace where creators receive royalties on secondary sales",
    "Create a multi-signature wallet that requires approval from two out of three owners",
    "Develop a staking contract where users earn rewards based on time staked",
    "Make a decentralized voting system where users can delegate their votes"
]

# Main application
def main():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2196F3;
        margin-top: 2rem;
    }
    .info-box {
        background-color: #000000;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #2196F3;
    }
    .success-box {
        background-color: #000000;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #4CAF50;
    }
    .code-header {
        font-size: 1.2rem;
        color: #333;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header">Natural Language to Solidity Converter</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    This tool translates natural language requirements into secure, production-ready Solidity smart contract code.
    Simply describe what you need, and get back a complete smart contract with security explanations.
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Features:")
        st.markdown("""
        - Generate Solidity code from plain English
        - Security analysis included
        - Best practices enforced
        - OpenZeppelin integration
        """)
        
        st.header("Example Prompts")
        for example in example_prompts:
            if st.button(f"📝 {example}"):
                st.session_state.user_input = example
                
        
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="sub-header">What would you like to build?</div>', unsafe_allow_html=True)
        
        # Initialize session state for user input
        if 'user_input' not in st.session_state:
            st.session_state.user_input = ""
        
        user_input = st.text_area(
            "Describe your smart contract requirements:",
            height=150,
            key="user_input_widget",
            value=st.session_state.user_input,
            help="Be as specific as possible about functionality, permissions, and security requirements."
        )
    
    with col2:
        st.markdown('<div class="sub-header">Tips for better results:</div>', unsafe_allow_html=True)
        st.markdown("""
        - Specify the token standard (ERC-20, ERC-721, etc.)
        - Mention access control requirements
        - Include special features (e.g., pausable, burnable)
        - Describe interactions with other contracts
        - Mention any specific security concerns
        """)
    

    # Generate button  
    generate_pressed = st.button("🔮 Generate Smart Contract", type="primary", use_container_width=True)
    
    # Display loading spinner during generation
    if generate_pressed and user_input:
        # Store the input in session state
        st.session_state.user_input = user_input
        
        if not api_key:
            st.error("OpenAI API key is required. Please enter your API key in the field above.")
        else:
            with st.spinner("Generating secure smart contract..."):
                # Call OpenAI API with the provided API key
                solidity_code, security_considerations = generate_contract_with_openai(user_input, api_key)
                
                if solidity_code and security_considerations:
                    st.session_state.solidity_code = solidity_code
                    st.session_state.security_considerations = security_considerations
                else:
                    st.error("Failed to generate code. Please check your API key and try again with a different prompt.")
    
    # Display results if available in session state
    if 'solidity_code' in st.session_state and 'security_considerations' in st.session_state:
        st.markdown('<div class="sub-header">Generated Smart Contract</div>', unsafe_allow_html=True)
        
        # Create tabs for code and security considerations
        code_tab, security_tab = st.tabs(["Solidity Code", "Security Considerations"])
        
        with code_tab:
            st.code(st.session_state.solidity_code, language="solidity")
            
            # Download button for the code
            st.download_button(
                label="⬇️ Download Solidity Code",
                data=st.session_state.solidity_code,
                file_name="SmartContract.sol",
                mime="text/plain",
                use_container_width=True
            )
        
        with security_tab:
            st.markdown("""
            <div class="success-box">
            <strong>Security Analysis:</strong> The following security considerations have been addressed in the generated code.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(st.session_state.security_considerations)
            
        # Next steps guidance
        st.markdown('<div class="sub-header">Next Steps</div>', unsafe_allow_html=True)
        st.markdown("""
        1. **Review** the generated code thoroughly
        2. **Test** using a local blockchain environment (Hardhat, Truffle, Foundry)
        3. **Deploy** to a testnet before moving to production
        4. Consider a professional **security audit** for high-value contracts
        """)

if __name__ == "__main__":
    main()
