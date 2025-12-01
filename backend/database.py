from db_connection import DatabaseConnection
from logger_helper import setup_logger



logger = setup_logger(name = "database", log_file = "../logs/database.log")



def insert_expenses(expense_date, amount, category, notes):
    try:
        with DatabaseConnection() as cursor:
            cursor.execute("INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)", (expense_date, amount, category, notes))

    except Exception as e:
        logger.error(str(e))
        raise
    
    else:
        logger.info("Successfully inserted the new data")




def fetch_all_records():
    try:
        with DatabaseConnection() as cursor:
            logger.info("Fetching all expenses")
            cursor.execute("SELECT * FROM expenses")
            expenses = cursor.fetchall()
    
    except Exception as e:
        logger.error(str(e))
        raise
    
    else:
        logger.info("Successful fetched all data.")
        return expenses



def fetch_expense_for_date(expense_date):
     try:
        with DatabaseConnection() as cursor:
            logger.info(f"Fetching expense for date {expense_date}")
            cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
            expenses = cursor.fetchall()

     except Exception as e:
         logger.error(str(e))
         raise
     
     else:
         logger.info(f"Successfully fetched expense for date {expense_date}")
         return expenses
         



def delete_expense_for_date(expense_date):
    try:
        with DatabaseConnection() as cursor:
            cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))
            
    except Exception as e:
        logger.error(str(e))
        raise
    
    else:
        logger.info("Successfully deleted!")



def fetch_expense_summary(start_date, end_date):
    try:
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT category, SUM(amount) AS Total, ROUND(SUM(amount) / (SELECT SUM(amount) FROM expenses), 2) AS Percentage FROM expenses WHERE expense_date BETWEEN %s AND %s GROUP BY Category ORDER BY Total DESC", (start_date, end_date))
            expense_summary = cursor.fetchall()

    except Exception as e:
        logger.error(str(e))
        raise

    else:
        logger.info("Successfully fetched summary")
        return expense_summary
    



if __name__ == "__main__":

    # delete_expense_for_date("2025-01-01")

    expenses = fetch_expense_for_date("2025-01-01")
    for expense in expenses:
        print(expense)

    # expenses = fetch_expense_summary("2024-08-01", "2024-08-15")
    # for expense in expenses:
    #     print(expense)