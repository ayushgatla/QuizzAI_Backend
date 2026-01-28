from crewai import Agent, Crew, Task
from typing import Dict, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
import json
import os


class AgentManager:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.context_storage: Dict[str, Dict[str, str]] = {}  
    
    def create_agent(self, session_id: str) -> Agent:
        if session_id in self.agents:
            print(f"Using existing agent for session: {session_id}")
            return self.agents[session_id]
        
        self.context_storage[session_id] = {}
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",  
            google_api_key=os.getenv("GEMINI_API_KEY"),  
            temperature=0.7, 
            convert_system_message_to_human=True  
        )
        
        agent = Agent(
            role="Educational AI Assistant",
            goal="""Generate high-quality educational questions (MCQs, short answer, long answer, or just normal answer for a question asked) 
                   from PDF content and help students learn through intelligent conversation. also the format should be correct everytime like the outermost part must be labelled as "mcqs" then further inner "question" ,"options","correct" and the answer should be respective A,B,C,D represented in such manner this for mcq but for shorts/long questions do accordling as asked from prompt""",
            backstory="""You are an expert educational assistant with deep knowledge across multiple subjects.
                        You excel at creating challenging yet fair questions that test understanding.
                        You have access to PDF content and can reference it to create questions.
                        
                        When generating questions, ensure they are:
                        - Clear and unambiguous
                        - Based on the actual PDF content
                        - At an appropriate difficulty level
                        - Well-structured with correct answers
                        
                        IMPORTANT: When asked to generate questions, you MUST respond ONLY with valid JSON.
                        Do not include any explanatory text, markdown formatting, or code blocks.
                        Just pure JSON that can be parsed directly.""",
            verbose=True,
            llm=llm,
            tools=[],
            allow_delegation=False,
        )
        
        self.agents[session_id] = agent
        print(f"Created new agent for session: {session_id}")
        return agent

    def add_to_context(self, session_id: str, content: str, content_type: str = "pdf_content"):
        """Add content to the session context."""
        if session_id not in self.context_storage:
            self.context_storage[session_id] = {}
        
        context_key = f"{content_type}_{len(self.context_storage[session_id])}"
        self.context_storage[session_id][context_key] = content
        
        print(f"Added {len(content)} characters to context for session: {session_id}")
        print(f"Total context items: {len(self.context_storage[session_id])}")

    def get_context(self, session_id: str) -> str:
        if session_id not in self.context_storage:
            return ""
        
        context_parts = []
        for key, value in self.context_storage[session_id].items():
            context_parts.append(f"[{key}]\n{value}\n")
        
        return "\n".join(context_parts)

    def run_agent(self, prompt: str, session_id: str, include_context: bool = True) -> str:
        if session_id not in self.agents:
            raise ValueError(
                f"No agent found for session: {session_id}\n"
                f"Available sessions: {list(self.agents.keys())}\n"
                f"Did you forget to create the agent first?"
            )
        
        try:
            agent = self.agents[session_id]
            
            full_prompt = prompt
            if include_context:
                context = self.get_context(session_id)
                if context:
                    full_prompt = f"""Context Information:
{context}

{prompt}"""
            
            print(f"Running agent for session: {session_id}")
            print(f"Prompt preview: {full_prompt[:200]}...")
            
            task = Task(
                description=full_prompt,
                agent=agent,
                expected_output="JSON formatted response with the requested questions or answer"
            )
            
            crew = Crew(
                agents=[agent],
                tasks=[task],
                verbose=True
            )
            
            result = crew.kickoff()
            response = str(result)
            
            print(f"Agent response length: {len(response)} characters")
            return response
        
        except Exception as ex:
            print(f"Error running agent: {str(ex)}")
            raise

    def get_agent_info(self, session_id: str) -> Optional[dict]:
        if session_id in self.agents:
            return {
                "session_id": session_id,
                "has_agent": True,
                "has_context": session_id in self.context_storage,
                "context_items": len(self.context_storage.get(session_id, {})),
                "agent_role": self.agents[session_id].role,
                "agent_goal": self.agents[session_id].goal
            }
        return {"error": f"No agent found for session: {session_id}"}

    def clean_session(self, session_id: str) -> bool:
        found = False
        
        if session_id in self.agents:
            print(f"Deleting agent for session: {session_id}")
            del self.agents[session_id]
            found = True
        
        if session_id in self.context_storage:
            print(f"Deleting context for session: {session_id}")
            del self.context_storage[session_id]
            found = True
        
        if not found:
            print(f"No data found for session: {session_id}")
        
        return found

    def get_active_sessions(self) -> list:
        return list(self.agents.keys())

    def get_stats(self) -> dict:
        return {
            "total_agents": len(self.agents),
            "total_contexts": len(self.context_storage),
            "active_sessions": self.get_active_sessions()
        }



agent_maneger = AgentManager()