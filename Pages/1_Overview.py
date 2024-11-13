import streamlit as st


# Define custom CSS
custom_css = """
<style>
    .container {
        
        margin: 0 auto;
        padding: 20px;        
    }
    h1 {
        color: #0056b3;
        text-align: left;
    }
    h2 {
        color: #0056b3;
        margin-top: 20px;
    }
    ul {
        margin-top: 10px;
        padding-left: 20px;
    }
    li {
        margin-bottom: 10px;
    }
    .output {
        background-color: #f1f1f1;
        padding: 15px;
        border-left: 4px solid #0056b3;
        font-family: monospace;
        margin-top: 10px;
    }
</style>
"""

# Display CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Main content
st.markdown("""
<div class="container">
    <h1>Product Overview</h1>
    <p>The product will include two main parts:</p>    
    <h2>Part 1 – Machine Learning</h2>
    <p><strong>Step 1:</strong> Use Machine Learning models to produce <em>“segmentation”</em> and project <em>“behavior patterns”</em> for a given customer with profile metrics.</p>    
    <ul>
        <li> Output example for customer X:</li>
    </ul>   
    
          
""", unsafe_allow_html=True)
st.image("Images/image001.png", caption="")
            
st.markdown("""
    <ul>  
        <li>This first step will generate different timelines of how Net Profit changes for different accounts overtime, based on segmentation on different customer types and behaviors.</li>  
    </ul>   
     <p><strong>Step 2:</strong> Based on the output in 1, the model will know the “sweet timing point” for starting risk management intervention for maintaining “equal marginal returns” after customer risk increases. </p?
    <ul>
        <li> Output example for customer X:</li>
    </ul> 
            """, unsafe_allow_html=True)
st.image("Images/image002.png", caption="")
st.markdown("""
    <div class="container">
    <h2>Part 2 – GenAI tool for user interaction and use cases</h2>
      
    </div>

           
""", unsafe_allow_html=True)

