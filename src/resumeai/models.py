"""Pydantic models for ResumeAI."""

# flake8: noqa: E501

from pydantic import BaseModel, Field, EmailStr, model_serializer

from typing import Any, Dict, List, Optional, Union
from abc import ABC, abstractmethod


class Base(BaseModel, ABC):
    jinja_template: Optional[str] = Field(
        None,
        description="The template used to generate the resume. DO NOT CHANGE THIS FIELD.",
    )

    @abstractmethod
    def get_items(self):
        pass

    @model_serializer
    def serialize_model(self):
        return {
            k: v.replace("&", "\\&") if isinstance(v, str) else v
            for k, v in self.__dict__.items()
        }


class _Degree(BaseModel):
    """
    A single degree held by a user.
    """

    title: str = Field(..., description="The title of the degree")
    university: str = Field(..., description="The university that awarded the degree")
    graduation: str = Field(
        ..., description="The date of graduation, in Month YYYY format"
    )


class _Job(BaseModel):
    """
    A single job or internship from a user's resume.
    """

    company: str = Field(..., description="The name of the company")
    position: str = Field(..., description="The position held at the company")
    start_date: str = Field(..., description="The start date of the position")
    end_date: str = Field(..., description="The end date of the position")
    location: str = Field(..., description="The location of the company")
    description: List[str] = Field(
        ..., description="A list of bullet points describing the position"
    )


class _Activity(BaseModel):
    """
    A single club or organization item from a resume.
    """

    organization: str = Field(..., description="The name of the organization")
    position: str = Field(..., description="The position held at the organization")
    startDate: str = Field(..., description="The start date of the position")
    endDate: str = Field(..., description="The end date of the position")


class _SkillList(BaseModel):
    """
    A list of skills of a specific type.
    """

    type: str = Field(
        ...,
        description="The type of skill",
        examples=["Programming Languages", "Frameworks", "Databases", "Tools", "Other"],
    )
    skills: List[str] = Field(..., description="A list of skills of the given type")

    @model_serializer
    def serialize_skill_list(self) -> Dict[str, Any]:
        return {"type": self.type, "skills": ", ".join(self.skills)}


class Bio(Base):
    """
    A user's personal information.
    """

    name: str = Field(..., description="The user's name")
    email: EmailStr = Field(..., description="The user's email")
    phone: Optional[str] = Field(None, description="The user's phone number")
    location: Optional[str] = Field(
        None, description="The user's location as a city, state pair"
    )
    linkedin_user: Optional[str] = Field(
        None,
        description="The user's LinkedIn profile URL. Only include the username, not the full URL.",
    )
    github_user: Optional[str] = Field(None, description="The user's GitHub username.")
    portfolio: Optional[str] = Field(
        None, description="The user's portfolio or personal website URL."
    )
    role: Optional[str] = Field("", description="The user's current role or position.")

    jinja_template: str = "resume"

    def get_items(self):
        return self.model_dump()


class Education(Base):
    """
    A list of degrees and associated information from a user's resume.
    """

    degrees: List[_Degree] = Field(
        ..., description="A list of degrees held by the user"
    )
    specializations: Optional[List[str]] = Field(
        None, description="A list of specializations or minors held by the user"
    )
    gpa: Optional[Union[int, float]] = Field(None, description="The user's GPA")

    jinja_template: str = "sections/education"

    def get_items(self):
        return {
            "degrees": self.degrees,
            "specializations": self.specializations,
            "gpa": str(self.gpa),
        }


class Experience(Base):
    """
    A list of all jobs and internships from the user's resume.
    """

    items: List[_Job]

    jinja_template: str = "sections/experience"

    def get_items(self):
        return self.model_dump()["items"]


class Activities(Base):
    """
    A list of clubs or organizations from user's resume. Ordered by start date.
    """

    items: List[_Activity]

    template: str = "sections/activities"

    def get_items(self):
        return self.model_dump()["items"]


class Skills(Base):
    """
    A list of all skills from a user's resume, organized by type.
    """

    items: List[_SkillList]

    template: str = "sections/skills"

    def get_items(self):
        return self.model_dump()["items"]


class Resume(Base):
    """
    A user's resume.
    """

    bio: Bio = Field(..., description="The user's personal information")
    education: Education = Field(..., description="The user's education")
    experience: Experience = Field(..., description="The user's work experience")
    activities: Activities = Field(
        ..., description="The user's extracurricular activities"
    )
    skills: Skills = Field(..., description="The user's skills")

    template: Optional[str] = None

    def get_items(self):
        return {
            "bio": self.bio.get_items(),
            "education": self.education.get_items(),
            "experiences": self.experience.get_items(),
            "activities": self.activities.get_items(),
            "skills": self.skills.get_items(),
        }

    def __iter__(self):
        for attr in [
            self.bio,
            self.education,
            self.experience,
            self.activities,
            self.skills,
        ]:
            yield attr
