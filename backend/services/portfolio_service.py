from typing import List, Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from models.portfolio import Portfolio, Position
from models.order import Order, OrderStatus, OrderType, OrderSide
from schemas.order import OrderCreate

async def get_portfolio_by_user(db: AsyncSession, user_id: str) -> Portfolio:
    result = await db.execute(
        select(Portfolio).options(selectinload(Portfolio.positions)).where(Portfolio.user_id == user_id)
    )
    portfolio = result.scalars().first()
    
    # Auto-create if it doesn't exist for the user yet
    if not portfolio:
        portfolio = Portfolio(user_id=user_id, cash_balance=Decimal("100000.0000"))
        db.add(portfolio)
        await db.commit()
        await db.refresh(portfolio)
        
    return portfolio

async def get_orders_by_portfolio(db: AsyncSession, portfolio_id: str) -> List[Order]:
    result = await db.execute(
        select(Order).where(Order.portfolio_id == portfolio_id).order_by(Order.created_at.desc())
    )
    return list(result.scalars().all())

async def submit_order(db: AsyncSession, portfolio_id: str, order_in: OrderCreate) -> Order:
    portfolio = await db.get(Portfolio, portfolio_id)
    if not portfolio:
        raise ValueError("Portfolio not found")
        
    # Create the order
    order = Order(
        portfolio_id=portfolio_id,
        symbol=order_in.symbol,
        order_type=order_in.order_type,
        side=order_in.side,
        quantity=order_in.quantity,
        price=order_in.price,
        status=OrderStatus.PENDING
    )
    db.add(order)
    
    # Mock execution engine: Execute immediately if it's a MARKET order
    # In a real app, this goes to an order matching engine or broker API
    if order.order_type == OrderType.MARKET:
        # Mock price since it's a market order (in a real app, we fetch from a pricing service)
        execution_price = Decimal("150.00") # Hardcoded for demo purposes
        order.price = execution_price
        
        cost_basis = order.quantity * execution_price
        
        if order.side == OrderSide.BUY:
            if portfolio.cash_balance < cost_basis:
                order.status = OrderStatus.REJECTED
            else:
                portfolio.cash_balance -= cost_basis
                order.status = OrderStatus.EXECUTED
                
                # Update position
                result = await db.execute(select(Position).where(Position.portfolio_id == portfolio_id, Position.symbol == order.symbol))
                position = result.scalars().first()
                if position:
                    # Very simple avg price calculation
                    total_value = (position.quantity * position.average_price) + cost_basis
                    position.quantity += order.quantity
                    position.average_price = total_value / position.quantity
                else:
                    position = Position(
                        portfolio_id=portfolio_id,
                        symbol=order.symbol,
                        quantity=order.quantity,
                        average_price=execution_price
                    )
                    db.add(position)
                    
        elif order.side == OrderSide.SELL:
            result = await db.execute(select(Position).where(Position.portfolio_id == portfolio_id, Position.symbol == order.symbol))
            position = result.scalars().first()
            
            if not position or position.quantity < order.quantity:
                order.status = OrderStatus.REJECTED
            else:
                portfolio.cash_balance += cost_basis
                order.status = OrderStatus.EXECUTED
                position.quantity -= order.quantity
                
                if position.quantity == 0:
                    await db.delete(position)
                    
    await db.commit()
    await db.refresh(order)
    return order
