from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.security import require_trainer
from app.services.trainer_service import TrainerService
from app.schemas.trainer_schema import (
    TrainerLearnerResponse,
    TrainerEngagementResponse,
    TrainerSkillResponse,
    TrainerAssessmentResponse,
    TrainerCertificationResponse,
)


router = APIRouter()


@router.get(
    "/learners",
    response_model=list[TrainerLearnerResponse],
)
def get_learners(
    db: Session = Depends(get_db),
    current_user=Depends(require_trainer),
):

    return TrainerService.get_assigned_learners(db)


@router.get(
    "/learner/{learner_id}/engagement",
    response_model=TrainerEngagementResponse,
)
def get_learner_engagement(
    learner_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_trainer),
):

    return TrainerService.get_learner_engagement(
        db,
        learner_id,
    )


@router.get(
    "/learner/{learner_id}/skill-development",
    response_model=TrainerSkillResponse,
)
def get_learner_skill_development(
    learner_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_trainer),
):

    return TrainerService.get_learner_skill_development(
        db,
        learner_id,
    )


@router.get(
    "/learner/{learner_id}/assessment-analytics",
    response_model=TrainerAssessmentResponse,
)
def get_learner_assessment_analytics(
    learner_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_trainer),
):

    return TrainerService.get_learner_assessment_analytics(
        db,
        learner_id,
    )


@router.get(
    "/learner/{learner_id}/certification-status",
    response_model=TrainerCertificationResponse,
)
def get_learner_certification_status(
    learner_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_trainer),
):

    return TrainerService.get_learner_certification_status(
        db,
        learner_id,
    )