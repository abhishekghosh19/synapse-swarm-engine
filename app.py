import streamlit as st
from google import genai
from concurrent.futures import ThreadPoolExecutor

st.set_page_config(page_title="Synapse Swarm Engine", page_icon="🧠", layout="wide")

st.title("🧠 Synapse Swarm Engine")
st.markdown("Dynamic multi-agent AI swarm powered by Google Gemini and Streamlit.")

st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Gemini API Key", type="password")

PERSONAS = {
    "Python Architect": "You are an elite Python Architect focused on clean code, scalability, and design patterns.",
    "Skeptical Critic": "You are a rigorous, skeptical critic who finds edge cases, security vulnerabilities, and logic gaps.",
    "Product Manager": "You are a pragmatic Product Manager focused on user impact, timelines, and MVP delivery."
}

selected_personas = st.sidebar.multiselect("Select Swarm Personas", list(PERSONAS.keys()), default=list(PERSONAS.keys()))

task_input = st.text_area("Enter your task or project description:", "Design a secure user authentication module.")

def run_agent(persona_name, persona_prompt, task):
    if not api_key:
        return persona_name, "Error: API key missing."
    try:
        client = genai.Client(api_key=api_key)
        full_prompt = f"{persona_prompt}\n\nTask: {task}"
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
        )
        return persona_name, response.text
    except Exception as e:
        return persona_name, f"Error: {str(e)}"

if st.button("Run Swarm Execution", type="primary"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not task_input:
        st.warning("Please enter a task.")
    elif not selected_personas:
        st.warning("Please select at least one persona.")
    else:
        with st.spinner("Swarm executing concurrently..."):
            results = {}
            with ThreadPoolExecutor(max_workers=len(selected_personas)) as executor:
                futures = {
                    executor.submit(run_agent, name, PERSONAS[name], task_input): name 
                    for name in selected_personas
                }
                for future in futures:
                    name, res = future.result()
                    results[name] = res

        st.success("Swarm execution complete!")
        for name, res in results.items():
            with st.expander(f"🤖 Persona: {name}", expanded=True):
                st.markdown(res)
