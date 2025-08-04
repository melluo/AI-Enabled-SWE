from pydantic import BaseModel
from typing import List, Dict, Optional

class Goal(BaseModel):
    goal: str
    kpi: str
    target: str

class Persona(BaseModel):
    name: str
    scenario: str

class UserStory(BaseModel):
    story_id: str
    description: str
    acceptance_criteria: List[str]

class FunctionalRequirement(BaseModel):
    epic: str
    user_stories: List[UserStory]

class NonFunctionalRequirement(BaseModel):
    performance: str
    security: str
    accessibility: str
    scalability: str

class ReleasePlan(BaseModel):
    version: str
    target_date: str
    features: List[str]

class OutOfScope(BaseModel):
    out_of_scope: List[str]
    future_work: List[str]

class Appendix(BaseModel):
    open_questions: List[str]
    dependencies: List[str]

class ProductRequirementsDocument(BaseModel):
    status: str
    author: str
    version: str
    last_updated: str
    executive_summary_vision: str
    problem_statement: str
    user_personas_scenarios: List[Persona]
    goals_success_metrics: List[Goal]
    functional_requirements_user_stories: List[FunctionalRequirement]
    non_functional_requirements: NonFunctionalRequirement
    release_plan_milestones: List[ReleasePlan]
    out_of_scope_future_considerations: OutOfScope
    appendix_open_questions: Appendix