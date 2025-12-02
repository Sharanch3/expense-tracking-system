from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date
from logger_helper import setup_logger
from database import (
    fetch_expense_for_date,
    fetch_expense_summary,
    insert_expenses,
    delete_expense_for_date,
    fetch_monthly_expense_summary
)

# logging config
logger = setup_logger(name='server', log_file='../logs/server.log')


# schema
class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date


app = FastAPI()



@app.get("/expenses/{expense_date}", response_model=List[Expense])
def fetch_expenses(expense_date: date):
    try:
        logger.info(f"Fetching expenses for date: {expense_date}")
        expenses = fetch_expense_for_date(expense_date)
        
        if not expenses:
            logger.warning(f"No expenses found for date: {expense_date}")
            raise HTTPException(status_code=404, detail="No data found for the given date.")
        
        logger.info(f"Successfully fetched {len(expenses)} expense(s) for date: {expense_date}")
        return expenses
        
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Database error while fetching expenses for {expense_date}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/expenses/{expense_date}")
def add_expenses(expense_date: date, expenses: List[Expense]):
    """Add new expenses without deleting existing ones."""
    
    if not expenses:
        logger.error(f"No expenses provided for date: {expense_date}")
        raise HTTPException(status_code=400, detail="No expenses provided")
    
    try:
        logger.info(f"Adding {len(expenses)} expense(s) for date: {expense_date}")

        delete_expense_for_date(expense_date)
        
        for expense in expenses:
            if expense.amount <= 0:
                logger.error(f"Invalid expense amount: {expense.amount} for date: {expense_date}")
                raise HTTPException(status_code=400, detail="Expense amount must be positive.")
            
            insert_expenses(expense_date, expense.amount, expense.category, expense.notes)
        
        logger.info(f"Successfully added {len(expenses)} expense(s) for date: {expense_date}")
        return {'message': f'Successfully added {len(expenses)} expense(s)!'}

    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Failed to add expenses for {expense_date}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to add expenses: {str(e)}")



@app.post("/analytics/")
def get_analytics(date_range: DateRange):
    """Get expense analytics for a date range."""
    
    if not date_range:
        logger.error("No date range provided for analytics")
        raise HTTPException(status_code=400, detail="Date range is required")
    
    try:
        logger.info(f"Fetching analytics from {date_range.start_date} to {date_range.end_date}")
        
        data = fetch_expense_summary(date_range.start_date, date_range.end_date)
        
        if not data:
            logger.warning(f"No expense data found for range: {date_range.start_date} to {date_range.end_date}")
            raise HTTPException(
                status_code=404, 
                detail="No expenses found for the given date range"
            )
        
        logger.info(f"Successfully fetched analytics for date range: {date_range.start_date} to {date_range.end_date}")
        return data
        
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Failed to fetch analytics for {date_range.start_date} to {date_range.end_date}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to fetch analytics: {str(e)}")

   
    

@app.get("/monthly_analytics/")
def get_monthly_analytics():
    monthly_summary = fetch_monthly_expense_summary()
    if monthly_summary is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve monthly expense summary from the database.")
    
    return monthly_summary
