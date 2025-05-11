import os
import sys
import json
import argparse
from dotenv import load_dotenv
from web3 import Web3
import requests
from openai import OpenAI
import hashlib
import openai


# Load environment variables from .env file
load_dotenv()

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai


# Initialize Web3 with Sepolia provider
INFURA_API_KEY = os.getenv("INFURA_API_KEY")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

# If no Infura key is provided, use a fallback public endpoint
if INFURA_API_KEY:
    w3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{INFURA_API_KEY}"))
else:
    # Fallback to Alchemy public endpoint or another public provider
    w3 = Web3(Web3.HTTPProvider("https://eth-sepolia.g.alchemy.com/v2/demo"))

# Etherscan API for Sepolia
ETHERSCAN_API_URL = "https://api-sepolia.etherscan.io/api"

def is_valid_address(address):
    """Check if the provided string is a valid Ethereum address."""
    return w3.is_address(address)

def get_contract_abi(contract_address):
    """Fetch contract ABI from Etherscan."""
    if not ETHERSCAN_API_KEY:
        print("Warning: ETHERSCAN_API_KEY not set. Some features may be limited.")
    
    params = {
        "module": "contract",
        "action": "getabi",
        "address": contract_address,
        "apikey": ETHERSCAN_API_KEY
    }
    
    response = requests.get(ETHERSCAN_API_URL, params=params)
    data = response.json()
    
    if data["status"] == "1":
        return json.loads(data["result"])
    else:
        print(f"Error fetching ABI: {data['result']}")
        return None

def get_contract_source_code(contract_address):
    """Fetch contract source code from Etherscan."""
    if not ETHERSCAN_API_KEY:
        print("Warning: ETHERSCAN_API_KEY not set. Some features may be limited.")
    
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": contract_address,
        "apikey": ETHERSCAN_API_KEY
    }
    
    response = requests.get(ETHERSCAN_API_URL, params=params)
    data = response.json()
    
    if data["status"] == "1" and data["result"]:
        return data["result"][0]["SourceCode"]
    else:
        print(f"Error fetching source code: {data['result']}")
        return None

def analyze_contract_from_address(contract_address):
    """Analyze a contract from its address on Sepolia testnet."""
    print(f"Analyzing contract at address: {contract_address}")
    
    # Fetch contract ABI
    abi = get_contract_abi(contract_address)
    
    # Fetch contract source code
    source_code = get_contract_source_code(contract_address)
    
    if not source_code:
        if abi:
            return analyze_contract_from_abi(abi, contract_address)
        else:
            return "Could not fetch contract source code or ABI. Please check the address or your API keys."
    
    return analyze_contract_from_source(source_code, abi, contract_address)

def analyze_contract_from_abi(abi, contract_address=None):
    """Generate an explanation from the contract ABI when source code is not available."""
    if not abi:
        return "No ABI available for analysis."
    
    contract_info = {
        "address": contract_address,
        "abi": abi
    }
    
    # Create prompt for the LLM
    prompt = f"""
    Analyze this smart contract ABI and provide a detailed technical summary.
    
    Contract ABI:
    {json.dumps(abi, indent=2)}
    
    Your analysis should include:
    1. Overall purpose of the contract (based on function signatures)
    2. Key functions and their purposes
    3. Access control and permissions
    4. Events and their significance
    5. Potential security considerations based on function signatures
    
    Provide the information in a clear, organized format suitable for non-technical users.
    """
    
    return generate_explanation_with_openai(prompt)

def analyze_contract_from_source(source_code, abi=None, contract_address=None):
    """Analyze a contract from its source code."""
    if not source_code:
        return "No source code provided for analysis."
    
    # If the source code is a complex JSON
    if source_code.startswith("{") and "}" in source_code:
        try:
            # Handle different source code formats from Etherscan
            if source_code.startswith("{{"):  # Double JSON encoding sometimes happens
                source_code = json.loads(json.loads(source_code))
                if isinstance(source_code, dict) and "sources" in source_code:
                    # Extract actual source from Standard JSON input format
                    all_sources = []
                    for file_path, file_content in source_code["sources"].items():
                        if "content" in file_content:
                            all_sources.append(f"// File: {file_path}\n{file_content['content']}")
                    source_code = "\n\n".join(all_sources)
            else:
                parsed = json.loads(source_code)
                if isinstance(parsed, dict) and "sources" in parsed:
                    # Extract actual source from Standard JSON input format
                    all_sources = []
                    for file_path, file_content in parsed["sources"].items():
                        if "content" in file_content:
                            all_sources.append(f"// File: {file_path}\n{file_content['content']}")
                    source_code = "\n\n".join(all_sources)
        except json.JSONDecodeError:
            # If it's not valid JSON
            pass
    
    contract_info = {
        "address": contract_address,
        "source_code": source_code
    }
    
    if abi:
        contract_info["abi"] = abi
    
    # Create prompt for the LLM
    prompt = f"""
    Analyze this Solidity smart contract and provide a detailed technical summary in plain English.
    
    ```solidity
    {source_code}
    ```
    
    Your analysis should include:
    1. Overall purpose of the contract
    2. Key functions and their purposes
    3. Access control and permissions
    4. State variables and their significance
    5. Events and their significance
    6. Security patterns and potential concerns
    7. Inheritance and interfaces used
    
    Provide the information in a clear, organized format suitable for non-technical users.
    Highlight any potential security concerns or best practices that are or are not followed.
    """
    
    return generate_explanation_with_openai(prompt)

def generate_explanation_with_openai(prompt):
    """Generate an explanation using OpenAI's API with guardrails."""
    try:
        # Create hash of the input for logging purposes
        input_hash = hashlib.md5(prompt.encode()).hexdigest()
        print(f"Generating explanation for input hash: {input_hash[:8]}...")
        
        # Apply guardrails by adding instructions
        safe_prompt = f"""
        {prompt}

        
        IMPORTANT SECURITY GUIDELINES:
        - Do NOT generate code unless explicitly asked
        - Focus only on explaining the contract's functionality and security aspects
        - Do not generate executable code that could be used maliciously
        - Highlight if fallback/receive functions are missing in Ether-handling contracts
        - If you detect a potential security vulnerability, explain it generally without providing exploit details
        - Be thorough but accessible in your explanations
        - Format the response in Markdown for better readability
        """
        
        # Call the OpenAI API
        # Using gpt-4o-mini for better analysis, but can be changed to other models as needed
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": "You are a smart contract security expert tasked with explaining smart contracts in plain English to non-technical users."},
                {"role": "user", "content": safe_prompt}
            ],
            max_tokens=4000,
            temperature=0.2
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating explanation: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Smart Contract Explainer")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", "--address", help="Contract address on Sepolia testnet")
    group.add_argument("-f", "--file", help="Solidity file path")
    group.add_argument("-c", "--code", help="Raw Solidity code")
    
    args = parser.parse_args()
    
    if args.address:
        if not is_valid_address(args.address):
            print("Error: Invalid Ethereum address")
            sys.exit(1)
        explanation = analyze_contract_from_address(args.address)
    
    elif args.file:
        try:
            with open(args.file, 'r') as file:
                source_code = file.read()
            explanation = analyze_contract_from_source(source_code)
        except FileNotFoundError:
            print(f"Error: File {args.file} not found")
            sys.exit(1)
    
    elif args.code:
        explanation = analyze_contract_from_source(args.code)
    
    print("\n" + "="*50 + "\n")
    print("SMART CONTRACT ANALYSIS")
    print("\n" + "="*50 + "\n")
    print(explanation)
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
