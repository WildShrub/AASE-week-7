f"""
    Given the changes made, do the following, provide evidence to support your claims.
    
    Identify potential issues or improvements
    
    
    Categorize change (feature, bugfix, refactor, etc.)
    
    
    Assess risk (low / medium / high)


Changes: {DIFF}
"""


f"Use the available tools to analyze the changes made to the code base from SHA {BASE_SHA} to SHA {HEAD_SHA}.\n\n Then do the following:"
"1. Identify potential issues or improvements\n"
"2. Categorize change (feature, bugfix, refactor, etc.)\n"
"3. Assess risk of bugs or code failure (low / medium / high)\n"
"Support all claims with evidence from tools"