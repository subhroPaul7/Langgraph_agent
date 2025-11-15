import streamlit as st
from langgraph.graph import END
from agent_graph.graph_module import create_graph, compile_workflow
import json

server = 'groq'
models = ['llama-3.3-70b-versatile', 'openai/gpt-oss-120b', 'qwen/qwen3-32b']
# model = 'llama-3.3-70b-versatile'
endpoint= None


st.set_page_config(
    page_title="Agentic Workflow",
    page_icon="🧠"
)

display_dict ={
    "planner_response": "Planner 👩🏿‍💻",
    "selector_response": "Selector 🖱️",
    "reporter_response": "Reporter 💻",
    "reviewer_response": "Reviewer 👩🏽‍⚖️",
    "router_response": "Router🔌"
}

# Initialize Streamlit UI
st.title("Agent Workflow Executor🧠")

# User input for the research question
research_question = st.text_input("Enter your research question:")
model = st.selectbox('Choose a model:', models)

if st.button("Run Workflow"):
    if research_question:
        # Create and compile the graph
        graph = create_graph(server=server, model=model, model_endpoint=endpoint)
        workflow = compile_workflow(graph)
        
        # Initialize the state
        initial_state = {"research_question": research_question}
        
        # Run the workflow
        with st.spinner("Loading content... Please wait"):
            try:
                result = workflow.invoke(initial_state)
            
                st.subheader("Workflow Output:")
                with st.expander("JSON output:"):
                    st.json(result)
                for i in range(len(result['serper_response'])):
                    with st.expander("Google search results"):
                        # Splitting the string by the separator `---`
                        entries = result['serper_response'][i].content.split('---')

                        # Creating an empty list to store the rows
                        table_rows = []

                        # Loop through each entry and extract the title and link
                        for entry in entries:
                            lines = entry.strip().split('\n')
                            
                            # Extract title and link
                            title = link = ''
                            for line in lines:
                                if line.startswith('Title:'):
                                    title = line.replace('Title: ', '').strip()
                                if line.startswith('Link:'):
                                    link = line.replace('Link: ', '').strip()
                            
                            # Append the extracted title and link to the list
                            if title and link:
                                table_rows.append((title, link))

                        # Prepare markdown for the table
                        markdown_table = "| Title | Link |\n|-------|------|\n"
                        for row in table_rows:
                            markdown_table += f"| {row[0]} | {row[1]} |\n"

                        # Display the markdown table in Streamlit
                        st.markdown(markdown_table)
                    # Display the output
                    with st.expander("Scrape results"):
                        # st.write(result['scraper_response'][0].content)
                        scraps = result['scraper_response'][i].content.split(",")
                        page = scraps[0].replace('source',"")
                        page = page.replace("'","")
                        page = page.replace(":","")
                        page = page.replace("{","")
                        con = scraps[1].replace('content',"")
                        con = con.replace("'","")
                        con = con.replace(":","")
                        con = con.replace("{","")
                        markdown_table1 = f"| **Source** | {page} |\n|-----|-------|\n"
                        markdown_table1 += f"| **Content** | {con} |\n"

                        # Display the table in Streamlit
                        st.markdown(markdown_table1)
                for key, value in result.items():
                    if key in display_dict and key!="reporter_response":
                        st.write(f"## {display_dict[key]}:\n\n")
                        # Parse the JSON string into a Python dictionary
                        json_data = json.loads(value[0].content)

                        # Prepare the markdown table
                        markdown_table = "| Step | Value |\n|-----|-------|\n"
                        for key, value in json_data.items():
                            markdown_table += f"| {key} | {value} |\n"

                        # Display the table in Streamlit
                        st.markdown(markdown_table)
                    elif key=='reporter_response':
                        st.write(f"## {display_dict[key]}: \n-----\n\n{result[key][0].content}")
                st.write(f"## Final response: \n-----\n\n{result['final_reports'][0].content}")
            except:
                st.error("LLM rate limit reached. Please try after sometime.")
    else:
        st.warning("Please enter a research question before running the workflow.")
