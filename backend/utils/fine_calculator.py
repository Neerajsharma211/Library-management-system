from datetime import datetime
from config import Config

class FineCalculator:
    @staticmethod
    def calculate_fine(due_date_str, return_date_str=None):
        """Calculate fine amount"""
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date() if return_date_str else datetime.now().date()

            if return_date <= due_date:
                return 0, 0

            days_overdue = (return_date - due_date).days
            fine_amount = min(days_overdue * Config.FINE_PER_DAY, Config.MAX_FINE_AMOUNT)

            return fine_amount, days_overdue
        except:
            return 0, 0

    @staticmethod
    def get_fine_status(days_overdue):
        """Get fine status based on days overdue"""
        if days_overdue == 0:
            return "No fine"
        elif days_overdue <= 7:
            return "Minor overdue"
        elif days_overdue <= 30:
            return "Moderate overdue"
        else:
            return "Severe overdue"

    @staticmethod
    def calculate_total_fines(fines_list):
        """Calculate total fine amount from list of fines"""
        return sum(fine.get('amount', 0) for fine in fines_list if fine.get('status') == 'pending')
