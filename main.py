import sys
import os
from brain import Brain
import tools
def main():
    # Initialize your unified AI core
    try:
        jarvis = Brain()
        print("⚡ Jarvis Multi-Intent Core online.")
        print("Systems initialized cleanly. Standing by for directives, Boss...")
    except Exception as e:
        print(f"❌ Failed to initialize Jarvis Core: {e}")
        return

    while True:
        try:
            # 1. Capture user terminal input
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue

            # 2. Gatekeeper Stage: Route the intent using fast JSON classification
            intent = jarvis.route_user_intent(user_input)
            
            # ----------------------------------------------------
            # CASE 1: System Shut Down Directive
            # ----------------------------------------------------
            if intent.action == "EXIT":
                print("\n[🤖 Jarvis]: Spinning down systems...")
                # Have him say a clean, custom butler sign-off before closing
                jarvis.generate_jarvis_voice(intent.optimized_prompt)
                print("👋 Session terminated cleanly. Goodbye, Boss.")
                sys.exit(0)

            # ----------------------------------------------------
            # CASE 2: Image & Graphic Generation Asset Request
            # ----------------------------------------------------
            elif intent.action == "IMAGE_GEN":
                print(f"🎨 Intent Detected [IMAGE_GEN]: Rendering blueprint array...")
                print(f"   Prompt: '{intent.optimized_prompt}'")
                
                # Execute the Imagen generator method
                status_message = jarvis.generate_image_imagen(intent.optimized_prompt)
                print(f"  Status: {status_message}")
                
                # Audibly confirm the file save completely from RAM
                jarvis.generate_jarvis_voice("Asset array successfully compiled and stored locally, Boss.")

            # ----------------------------------------------------
            # CASE 3: Complex Software Engineering or Hacking Core Task
            # ----------------------------------------------------
            elif intent.action == "COMPLEX_TASK":
                print("🧠 Intent Detected [COMPLEX_TASK]: Deploying strategic planner...")
                
                # Call your Planner module to build the hyper-efficient engineering layout
                expanded_blueprint = jarvis.generate_content(intent.optimized_prompt)
                
                print("\n--- 📋 DYNAMIC META-PROMPT ENGINEERING BLUEPRINT ---")
                print(expanded_blueprint.strip())
                print("----------------------------------------------------\n")
                
                # Because the blueprint is a massive wall of text, don't make him read it all out loud.
                # Tell him to speak a quick, sharp verbal confirmation instead.
                jarvis.generate_jarvis_voice("Strategic engineering blueprint generated and displayed in the console, Boss.")

            # ----------------------------------------------------
            # CASE 4: Real-Time Live Web Search Footprint
            # ----------------------------------------------------
            elif intent.action == "WEB_SEARCH":
                print("🌐 Intent Detected [WEB_SEARCH]: Internet grounding required.")
                print(f"   Optimized Search Query: '{intent.optimized_prompt}'")
                
                # 🔥 THE REAL DEAL: Execute the live LangChain DuckDuckGo tool
                search_raw_results = tools.web_search_tool(intent.optimized_prompt)
                refine_search = jarvis.refine_search_results(intent.optimized_prompt, search_raw_results)
                print(f"\n[🌐 Live Raw Snippets Retrieved]:\n{search_raw_results}\n")
                
                # Feed the real-time internet data directly into Jarvis's voice module
                # The model will synthesize the data and read it using the British archetype!
                jarvis.generate_jarvis_voice(f"Web intelligence retrieved, Boss. Here are the findings: {refine_search}")
            # ----------------------------------------------------
            # CASE 5: General Conversational Small Talk / Greetings
            # ----------------------------------------------------
            elif intent.action == "NORMAL_CHAT":
                # Direct route straight to the in-memory voice loop
                jarvis.generate_jarvis_voice(intent.optimized_prompt)

        except KeyboardInterrupt:
            # Handle standard Ctrl+C terminal cancellations gracefully
            print("\n\n[System Interrupt Clean Catch]. Spreading system down...")
            jarvis.generate_jarvis_voice("Systems force interrupted. Standing down, Boss.")
            sys.exit(0)
            
        except Exception as e:
            print(f"❌ Core loop encountered an unexpected runtime exception: {e}")

if __name__ == "__main__":
    main()