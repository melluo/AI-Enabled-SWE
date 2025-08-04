from datetime import date
from typing import List, Optional, Dict, Tuple
from pydantic import BaseModel

class UserStory(BaseModel):
    story: str
    acceptance_criteria: List[str]

class PersonaScenario(BaseModel):
    persona: str
    scenario: str

class Goal(BaseModel):
    goal: str
    kpi: str
    target: str

class NonFunctionalRequirement(BaseModel):
    category: str
    description: str

class Milestone(BaseModel):
    version: str
    target_date: Optional[date]
    features: List[str]

class OutOfScope(BaseModel):
    description: str

class FutureWork(BaseModel):
    description: str

class AppendixItem(BaseModel):
    type: str
    description: str

class ProductRequirementsDocument(BaseModel):
    title: str
    status: str
    author: str
    version: str
    last_updated: Optional[date]
    executive_summary: str
    vision: str
    problem_statement: str
    user_personas_scenarios: List[PersonaScenario]
    goals_and_metrics: List[Goal]
    user_stories: List[UserStory]
    non_functional_requirements: List[NonFunctionalRequirement]
    release_plan: List[Milestone]
    out_of_scope: List[OutOfScope]
    future_considerations: List[FutureWork]
    appendix: List[AppendixItem]

# Example usage:
prd = ProductRequirementsDocument(
    title="Product Requirements Document: Example Product",
    status="Draft",
    author="Team Example",
    version="1.0",
    last_updated=date(2023, 10, 5),
    executive_summary="This product aims to streamline onboarding for new hires by providing a centralized, user-friendly platform.",
    vision="To enhance productivity and engagement for new hires by reducing onboarding friction.",
    problem_statement="New hires currently face a fragmented and overwhelming onboarding experience...",
    user_personas_scenarios=[
        PersonaScenario(persona="The New Hire", scenario="Faces confusion with multiple onboarding platforms."),
        PersonaScenario(persona="The Hiring Manager", scenario="Spends excessive time answering repetitive questions."),
        PersonaScenario(persona="The HR Coordinator", scenario="Handles high volume of support tickets.")
    ],
    goals_and_metrics=[
        Goal(goal="Improve New Hire Efficiency", kpi="Reduce time-to-first-contribution", target="Decrease by 20% in Q1"),
        Goal(goal="Reduce Support Load", kpi="Decrease repetitive questions to HR", target="30% reduction in support tickets"),
        Goal(goal="Increase Engagement", kpi="Onboarding completion rate", target="Achieve 95% completion rate")
    ],
    user_stories=[
        UserStory(
            story="As a New Hire, I want to log in with my company credentials, so that I can access the onboarding platform securely.",
            acceptance_criteria=[
                "Given I am on the login page, when I enter my valid SSO credentials, then I am redirected to my personal dashboard.",
                "Given I am on the login page, when I enter invalid credentials, then I see a clear error message."
            ]
        )
    ],
    non_functional_requirements=[
        NonFunctionalRequirement(category="Performance", description="The application must load in under 3 seconds on a standard corporate network connection."),
        NonFunctionalRequirement(category="Security", description="All data must be encrypted in transit and at rest. The system must comply with company SSO policies."),
        NonFunctionalRequirement(category="Accessibility", description="The user interface must be compliant with WCAG 2.1 AA standards."),
        NonFunctionalRequirement(category="Scalability", description="The system must support up to 500 concurrent users during peak onboarding seasons.")
    ],
    release_plan=[
        Milestone(version="1.0 (MVP)", target_date=date(2023, 12, 1), features=["Core features including user login", "task checklist", "document repository"]),
        Milestone(version="1.1", target_date=date(2024, 3, 1), features=["Mentorship connection", "team introduction features"]),
        Milestone(version="2.0", target_date=date(2024, 6, 1), features=["Full social engagement", "gamification elements"])
    ],
    out_of_scope=[
        OutOfScope(description="Direct integration with third-party HR payroll systems."),
        OutOfScope(description="A native mobile application (the web app will be mobile-responsive)."),
        OutOfScope(description="Advanced analytics dashboard for managers.")
    ],
    future_considerations=[
        FutureWork(description="Integration with the corporate Learning Management System (LMS)."),
        FutureWork(description="AI-powered personalized learning paths for new hires.")
    ],
    appendix=[
        AppendixItem(type="Open Question", description="Which team will be responsible for maintaining the content in the document repository?"),
        AppendixItem(type="Dependency", description="The final UI design mockups are required from the Design team by [Date].")
    ]
)