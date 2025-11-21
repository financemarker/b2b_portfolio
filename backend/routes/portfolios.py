from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.dependencies import get_db, get_current_client
from backend.models.client import Client
from backend.models.user import User
from backend.models.portfolio import Portfolio
from backend.schemas.response_wrapper import ApiResponse
from backend.schemas.portfolio import PortfolioCreate, PortfolioRead, ImportPayload, ImportResponse
from backend.services.integration import service
from backend.core import utils

router = APIRouter()

# === PORTFOLIOS ===


@router.post("/", response_model=ApiResponse[PortfolioRead])
async def create_connection(
    payload: PortfolioCreate,
    db: Session = Depends(get_db),
    client: Client = Depends(get_current_client),
):
    """Создать новый портфель для пользователя"""
    try:
        user = db.query(User).filter(User.client_id == client.id,
                                     User.external_id == payload.external_user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        utils.check_portfolios_limit(client, user)

        portfolio = utils.create_and_link_portfolio(user, db)
        return ApiResponse.ok_list(portfolio)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{portfolio_id}/", response_model=ApiResponse[PortfolioRead])
async def create_connection(
    portfolio_id: int,
    db: Session = Depends(get_db),
    client: Client = Depends(get_current_client),
):
    """Создать новый портфель для пользователя"""
    try:
        portfolio = db.query(Portfolio).filter(
            Portfolio.id == portfolio_id, Portfolio.user.client_id == client.id)
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        return ApiResponse.ok_item(portfolio)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{portfolio_id}/operations/import/", response_model=ApiResponse[ImportResponse])
async def import_operations(
    portfolio_id: int,
    payload: ImportPayload,
    db: Session = Depends(get_db),
    client: Client = Depends(get_current_client),
):
    """Разовый импорт сделок — по connection_id или файлу"""
    try:
        user = db.query(User).filter(User.client_id == client.id,
                                     User.external_id == payload.external_user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not payload.connection_id and not payload.operations:
            raise HTTPException(
                status_code=404, detail="Payload invalid: specify data for import")

        portfolio = db.query(Portfolio).filter(
            Portfolio.id == portfolio_id, Portfolio.user_id == user.id)
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        result = await service.import_operations(db, user, portfolio, payload)
        return ApiResponse.ok_item(result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
