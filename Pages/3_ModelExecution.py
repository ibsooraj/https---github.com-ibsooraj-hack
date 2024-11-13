
import streamlit as st
import openai
import pandas as pd
import json

openai.api_key = ""
openai.base_url= "https://ai-ibsooraj8752ai916045283496.openai.azure.com/openai/deployments/gpt-4/chat/completions?"
#openai.base_url= "https://ai-ibsooraj8752ai916045283496.openai.azure.com/"
openai.api_version = "2024-02-15-preview" 
openai.api_type = "azure"

# CSS to set background color
page_bg_color = """
<style>
    body {
        background-color: #f0f8ff; /* Light blue background */
    }
</style>
"""

# Inject CSS into the app
st.markdown(page_bg_color, unsafe_allow_html=True)

def createSlidingControls():
    with st.expander("",expanded=True):
    # Example data for the table
        data = [
            {"name": "Delinquency", "value": 22, "slider_min": 0, "slider_max": 100},
            {"name": "Utilization", "value": 20, "slider_min": 0, "slider_max": 100},
            {"name": "FICO", "value": 20, "slider_min": 10, "slider_max": 100},
            {"name": "Credit_Inquiries", "value": 20, "slider_min": 0, "slider_max": 100},
            {"name": "Temperature", "value": 0.1, "slider_min": 0.0, "slider_max": 1.0},
            {"name": "Resultset", "value": 20, "slider_min": 0, "slider_max": 500},
        ]

        # Initialize a placeholder to store slider values
        slider_values = {}

        #st.title("Table with Slider Controls")

        # Create a header row
        header_cols = st.columns([2, 6])  # Adjust column widths as needed
        header_cols[0].write("Name")
        #header_cols[1].write("Current Value")
        header_cols[1].write("Adjust Value")

        # Populate table rows with sliders
        for i, row in enumerate(data):
            cols = st.columns([2, 6])  # Adjust column widths as needed
            cols[0].write(row["name"])  # Display the item name
            #cols[1].write(row["value"])  # Display the current value
            
            # Add a slider for each item
            slider_values[row["name"]] = cols[1].slider(
                "Adjust " + row["name"], 
                min_value=row["slider_min"], 
                max_value=row["slider_max"], 
                value=row["value"], 
                key=f"slider_{i}"
            )    

        # Display the updated slider values
        #st.subheader("Updated Values")
        #st.write(slider_values["Delinquency"])
        st.session_state["Delinquency"]=slider_values["Delinquency"]
        st.session_state["Utilization"]=slider_values["Utilization"]
        st.session_state["FICO"]=slider_values["FICO"]
        st.session_state["Credit_Inquiries"]=slider_values["Credit_Inquiries"] 
        st.session_state["Resultset"]=slider_values["Resultset"]
        st.session_state["Temperature"]=slider_values["Temperature"]
        
def get_openai_response(context, sysPrompt,prompt):
    try:        
        response = openai.chat.completions.create(
            model="gpt-4",  # Replace with your model name, 
            max_tokens=200,
            temperature=0.1,                      
            messages=[
               # {"role": "system", "content": "You are an expert data scientist who answers from given context"},
                {"role": "system", "content": sysPrompt},
                {"role": "user", "content": "Context: " +  context  + "\n\n Query: " + prompt}
            ]
        )
        x=response.choices[0].message.content
        content = x
        return  content 
    except Exception as e:
        return f"Error: {str(e)}"
      
st.write("Available Customer Data:")
custDataExists = False

if "sd" in st.session_state:   
    custDataExists = True 
    st.write(st.session_state["sd"]) 

st.write("Prompt Weight Adjustment:")
createSlidingControls()



prompt = f"""
"Assume you are a data scientist working for a major bank with access to customer month-end financial and risk performance metrics. Your goal is to categorize the customer’s financial risk, calculate their probability of default, and identify any significant deviations from expected financial behavior that could indicate the need for intervention.

### Risk Categorization:
Classify the customer based on a weighted composite of financial indicators. These are as follows:
- MoM Cumulative Profit
- Revolving Balance (Revolving_Bal)
- ECL (Expected Credit Loss)
- ECL MoM Change
- Delinquency
- Utilization
- FICO
- Credit_Inquiries
- Total_Debt
- Debt_to_Income_Ratio
- external_bank_credit_card_max_util_greater_than_90
- external_bank_credit_card_max_util_greater_than_50
- Revolving_Bal
- Credit_Limit
- Income Category
- Education_Level
- Marital Status
- Customer Age
- Month on Book

Use this scale for categorization:
- [<10%] Low Risk
- [10%-25%] Low-Medium Risk
- [25%-50%] Medium Risk
- [50%-80%] High Risk
- [80%-100%] Very High Risk

### Probability of Default:
Calculate the probability of default based on a weighted composite of the metrics above. Use the following weights:
- Delinquency (22%)
- Utilization (20%)
- FICO (20%)
- Credit_Inquiries (20%)
- Total_Debt (3%)
- Debt_to_Income_Ratio (3%)
- external_bank_credit_card_max_util_greater_than_90 (6%)
- external_bank_credit_card_max_util_greater_than_50 (6%)
- Revolving_Bal (5%)
- Credit_Limit (2%)
- Income Category (1%)
- Education_Level (1%)
- Marital Status (1%)
- Customer Age (1%)
- Month on Book (1%)

### Significant Deviation Indicators:
Identify significant month-on-month changes signaling a need for intervention:
- A decrease in Cumulative Profit of >1%.
- ECL increase of >10%.
- Increase in Utilization of >10%.
- Increase in Debt-to-Income Ratio >5%.

### Intervention Trigger:
Identify the earliest month in which:
1. MoM Cumulative Profit is negative and exceeds a 1% decrease.
2. Focus on the most recent and significant changes up to and including the specified benchmark date (**March 31, 2017**).

Output the result in an HTML table format with the following columns:
1. **probabilityofdefault**: The average probability of default.
2. **riskcategory**: The customer's risk category.
3. **earliest_month**: The earliest month requiring intervention based on corrected logic.
4. **comments**: Recommendations for intervention or monitoring.
5. **analysis**: A 20-word detailed analysis explaining the findings and rationale.
                    """
sysPrompt = f"""
You are a financial analyst AI working for a major bank. Your task is to categorize financial risk, calculate the probability of default, and identify significant deviations based on financial metrics provided by the user. Follow these rules when generating your response:

1. Focus on accuracy, logic, and consistency when analyzing financial data.
2. Use the weighted metrics and intervention logic exactly as specified.
3. Ensure your output is structured in a clear, concise, and tabular HTML format with the following columns:
   - probabilityofdefault: Average probability of default based on the provided weights.
   - riskcategory: Categorization of the customer's financial risk based on weighted metrics.
   - earliest_month: The earliest month requiring intervention based on the provided logic.
   - comments: Recommendations for intervention or monitoring.
   - analysis: A 20-word detailed explanation of the findings and rationale.
4. Adhere to the specified risk categorization scale and weights in your calculations.
5. Incorporate benchmark dates and corrected logic for identifying intervention points.

Ensure the output is well-structured, precise, and tailored to the specified requirements without including any additional text outside of the HTML table.
 """
# df = pd.read_csv("CustB.csv")
# context = df.to_json(orient="records") 
# #context=st.session_state["sd"].to_json(orient="records")  
# response = get_openai_response(context,prompt)
#     #df=pd.DataFrame(response["data"],columns=response["columns"])
#     #st.table(df)
# st.text_area("Response:", value=response, height=300)
# st.html(response)




debug = st.sidebar.checkbox("Debug", value=False)
if debug:
    with st.expander("Prompt:"):
        #prompt.replace({})
        st.markdown(prompt)

if  st.button("Run Model",key="rm", disabled= not custDataExists):
    context=st.session_state["sd"].to_json(orient="records")  
    #st.write(context)
    response = get_openai_response(context,sysPrompt,prompt)  
   
    st.write("Results:")
    st.markdown("<html>" + response.replace("```html","").replace("```","") + "</html>",unsafe_allow_html=True)



