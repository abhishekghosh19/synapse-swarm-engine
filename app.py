import streamlit as st
from google import genai
from concurrent.futures import ThreadPoolExecutor

st.set_page_config(page_title="Synapse Sovereign Swarm Engine", page_icon="🧠", layout="wide")

st.title("🧠 Synapse Sovereign Swarm Engine")
st.markdown("Multi-agent orchestrator powered by Google Gemini and Professor Synapse architecture.")

st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Gemini API Key", type="password")

PERSONAS = {
    "Professor Synapse": "You are Professor Synapse, master orchestrator and meta-intelligence architect. Your job is to analyze intent, coordinate strategy, and synthesize diverse agent viewpoints into an elite execution plan.",
    "Python Architect": "You are an elite Python Architect focused on clean code, scalability, modularity, and enterprise design patterns.",
    "Skeptical Critic": "You are a rigorous security and logic critic who hunts down edge cases, vulnerabilities, and architectural flaws.",
    "Product Manager": "You are a pragmatic Product Manager focused on user impact, user stories, MVPs, and rapid delivery timelines.",
    "Chaos Tester": "You are an adversarial stress-tester who simulates systemic failure modes, load spikes, and breaking conditions."
}

selected_personas = st.sidebar.multiselect(
    "Select Swarm Personas", 
    list(PERSONAS.keys()), 
    default=["Python Architect", "Skeptical Critic", "Product Manager"]
)

task_input = st.text_area("Enter your task or project description:", "Design a secure user authentication module.")

def run_agent(persona_name, persona_prompt, task):
    if not api_key:
        return persona_name, "Error: API key missing."
    try:
        client = genai.Client(api_key=api_key)
        full_prompt = f"{persona_prompt}\n\nTarget Task / Directive:\n{task}"
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=full_prompt,
        )
        return persona_name, response.text
    except Exception as e:
        return persona_name, f"Error: {str(e)}"

if st.button("Run Sovereign Swarm Execution", type="primary"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not task_input:
        st.warning("Please enter a task.")
    elif not selected_personas:
        st.warning("Please select at least one persona.")
    else:
        with st.spinner("Executing multi-agent swarm pipeline..."):
            results = {}
            
            # Filter out Professor Synapse from parallel worker execution if present
            worker_personas = [p for p in selected_personas if p != "Professor Synapse"]
            
            # Step 1: Run Worker Agents Concurrently
            if worker_personas:
                with ThreadPoolExecutor(max_workers=len(worker_personas)) as executor:
                    futures = {
                        executor.submit(run_agent, name, PERSONAS[name], task_input): name 
                        for name in worker_personas
                    }
                    for future in futures:
                        name, res = future.result()
                        results[name] = res

            # Step 2: Professor Synapse Orchestration & Synthesis (If Selected)
            if "Professor Synapse" in selected_personas:
                synthesis_input = f"Original Directive: {task_input}\n\nSub-Agent Outputs:\n"
                for name, res in results.items():
                    synthesis_input += f"\n--- [{name}] ---\n{res}\n"
                
                synapse_prompt = (
                    f"{PERSON_PROMPT := PERSONAS['Professor Synapse']}\n\n"
                    f"Review the sub-agent analyses above. Synthesize their insights, reconcile conflicts, "
                    f"call out missing critical gaps, and output a final Sovereign Master Strategy."
                )
                _, synth_res = run_agent("Professor Synapse", synapse_prompt, synthesis_input)
                results["Professor Synapse"] = synth_res

        st.success("Sovereign swarm execution complete!")
        
        # Display Professor Synapse first if available
        if "Professor Synapse" in results:
            with st.expander("🧠 Master Orchestrator: Professor Synapse (Synthesis)", expanded=True):
                st.markdown(results["Professor Synapse"])
                
        # Display other agents
        for name, res in results.items():
            if name != "Professor Synapse":
                with st.expander(f"🤖 Persona: {name}", expanded=False):
                    st.markdown(res)
