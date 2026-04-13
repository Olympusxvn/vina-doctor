from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, Query

from ai_engine.api.v1.schemas.consultation_schemas import (
    ErrorResponse,
    ProcessAudioResponse,
)
from ai_engine.application.use_cases.process_audio_use_case import (
    ProcessAudioError,
    ProcessAudioUseCase,
)

router = APIRouter(prefix="/v1/consultations", tags=["consultations"])


def _get_use_case() -> ProcessAudioUseCase:
    """Dependency injector — resolved by the app factory in main.py."""
    from ai_engine.main import get_process_audio_use_case  # noqa: PLC0415
    return get_process_audio_use_case()


@router.post(
    "/process",
    response_model=ProcessAudioResponse,
    responses={
        422: {"model": ErrorResponse, "description": "VAD rejection or bad format"},
        500: {"model": ErrorResponse, "description": "Pipeline or API error"},
    },
    summary="Process a medical consultation audio file",
    description=(
        "Accepts an audio upload, runs VAD, calls Qwen2-Audio with the master "
        "medical scribe prompt, and returns a structured multilingual SOAP report."
    ),
)
async def process_consultation(
    file: UploadFile,
    model: str = Query(
        default="qwen-audio-turbo",
        description="Qwen model to use. Use 'qwen-audio-max' for long/complex recordings.",
    ),
    use_case: ProcessAudioUseCase = Depends(_get_use_case),
) -> ProcessAudioResponse:
    """Upload an audio file and receive a structured medical report."""

    audio_bytes = await file.read()

    with tempfile.TemporaryDirectory() as tmp:
        work_dir = Path(tmp)
        audio_path = work_dir / (file.filename or "audio.mp3")
        audio_path.write_bytes(audio_bytes)

        try:
            report = use_case.execute(
                audio_path,
                work_dir=work_dir,
                model=model,
            )
        except ProcessAudioError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc),
            ) from exc

    return ProcessAudioResponse(
        metadata=report.metadata,
        transcript=report.transcript,
        clinical_report=report.clinical_report,
        multilingual_summary=report.multilingual_summary,
    )
