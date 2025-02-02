import os
import json
import requests
import streamlit as st
from langchain_community.utilities import GoogleSerperAPIWrapper
from states.state import AgentGraphState

def format_results(organic_results):
    result_strings = []
    for result in organic_results:
        title = result.get('title', 'No Title')
        link = result.get('link', '#')
        snippet = result.get('snippet', 'No snippet available.')
        result_strings.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n---")
    
    return '\n'.join(result_strings)

def get_google_serper(state: AgentGraphState, plan):
    plan_data = plan().content
    plan_data = json.loads(plan_data)
    search = plan_data.get("search_term")

    search_url = "https://google.serper.dev/search"
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': st.secrets["SERPER_API_KEY"]  # Fetching the API key from Streamlit secrets
    }
    payload = json.dumps({"q": search})
    
    try:
        response = requests.post(search_url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4XX, 5XX)
        results = response.json()
        
        if 'organic' in results:
            formatted_results = format_results(results['organic'])
            state = {**state, "serper_response": formatted_results}
            return state
        else:
            return {**state, "serper_response": "No organic results found."}

    except requests.exceptions.HTTPError as http_err:
        return {**state, "serper_response": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        return {**state, "serper_response": f"Request error occurred: {req_err}"}
    except KeyError as key_err:
        return {**state, "serper_response": f"Key error occurred: {key_err}"}
