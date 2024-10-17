from ..auth.databaseConnection import getDBConnection
from flask import current_app
from .bank import Bank
from .merchant import Merchant

class ApiProcess():
    
    def paymentProcessProcedure(self, data):

        #data include cust_email, merch_email, amount, cardNumber, expiryDate, cvv

        # get the merchant id by the merchant email
        merchId = Merchant().getMerchantIdByEmail(data['merch_email'])['merch_id']

        
        #after validate card need to store the card info into the shiokority_api.Staging_card
        isInserted = self.insertCardIntoStaging(data['cardNumber'], data['cvv'], data['expiryDate'])

        if not isInserted:
            return False, "Error inserting card into staging"
        
        #after insert card into staging, need to insert the payment record into the shiokority_api.Payment_record
        isInserted, paymentRecordId = self.insertPaymentRecord(data['amount'], data['cardNumber'], merchId)

        if not isInserted:
            # if isInserted is False, paymentRecordId will be the error message
            return False, paymentRecordId
        
        #after insert payment record, need to process the payment
        isProcessed, paymentId = self.insertPayment(data['amount'], data['cardNumber'], merchId, paymentRecordId)

        if not isProcessed:
            # if isProcessed is False, paymentId will be the error message
            return False, paymentId

        # if all the above steps are successful, now we need to call the bank to process the payment
        bankProcessPayment, message = Bank().bankProcessPayment(data['cardNumber'], data['amount'])

        # Need insert the payment_success_history table or payment_fail_history table
        # this lulin need to help I also need to help lulin

        if not bankProcessPayment:

            # bankProcessPayment is False, need to update the payment status (fail) in the shiokority_api.Payment table
            isUpdated, message = self.updatePaymentStatus(paymentRecordId)

            if not isUpdated:
                return False, message

            # bank process payment failed, need to insert the shiokority_api.Payment_result table after update the payment status
            isInserted, message = self.insertPaymentResult(paymentId)
            
            if not isInserted:
                return False, message

            return False, message
        
        # after verify completed with the bank, need to update the payment status in the shiokority_api.Payment table
        isUpdated, message = self.updatePaymentStatus(paymentRecordId)

        if not isUpdated:
            return False, message
        
        # if the Payment status is updated successfully, insert the record payment_result table
        isInserted, message = self.insertPaymentResult(paymentId)

        if not isInserted:
            return False, message
        
        return True, "Payment processed successfully"

    def insertPaymentResult(self, payment_id):
        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])
        try:
            with connection.cursor() as cursor:
                sql_query = '''
                    INSERT INTO Payment_result (payment_id, payment_result_status, payment_result_date_created, payment_result_date_updated_on)
                    VALUES (%s, 'completed', NOW(), NOW())
                '''
                result = cursor.execute(sql_query, (payment_id))
                connection.commit()

                if result == 0:
                    return False, "Error inserting payment result"
                
                return True, "Payment result inserted successfully"
        except Exception as e:
            print(f"Error inserting payment result function: {str(e)}")
            return False, "Error inserting payment result"


    def updatePaymentStatus(self, payment_record_id):
        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])
        try:
            with connection.cursor() as cursor:
                sql_query = '''
                    UPDATE Payment
                    SET payment_status = 'completed', payment_updated_on = NOW()
                    WHERE payment_record_id = %s
                '''
                result = cursor.execute(sql_query, (payment_record_id))
                connection.commit()

                if result == 0:
                    return False, "Error updating payment status"
                
                return True, "Payment status updated successfully"
        except Exception as e:
            print(f"Error updating payment status function: {str(e)}")
            return False, "Error updating payment status"
    
    def insertPayment(self, amount, cardNumber, merch_id, payment_record_id):
        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])
        try:
            with connection.cursor() as cursor:
                sql_query = '''
                    INSERT INTO Payment (payment_amount, payment_type, payment_status, payment_date_created, 
                    payment_updated_on, tokenised_pan, merch_id, payment_record_id)
                    VALUES (%s, 'payment', 'pending', NOW(), NOW(), %s, %s, %s)
                '''
                result = cursor.execute(sql_query, (amount, cardNumber, merch_id, payment_record_id))
                paymentId = cursor.lastrowid
                connection.commit()

                if result == 0:
                    return False, "Error inserting payment "
                
                return True, paymentId
        except Exception as e:
            print(f"Error inserting payment function: {str(e)}")
            return False, "Error inserting payment record"

    def insertPaymentRecord(self, amount, cardNumber, merch_id):
        connection = getDBConnection('shiokority_api')

        try:
            with connection.cursor() as cursor:
                sql_query = '''
                    INSERT INTO Payment_record (payment_record_amount, payment_record_type, payment_record_status,
                    payment_record_date_created, payment_record_updated_on, tokenised_pan, merch_id)
                    VALUES (%s, 'payment', 'pending', NOW(), NOW(), %s, %s);
                '''
                result = cursor.execute(sql_query, (amount, cardNumber, merch_id))
                # Get the primary key of the newly inserted record
                payment_record_pk = cursor.lastrowid
                connection.commit()
                
                if result == 0:
                    return False, "Error inserting payment record"


                return True, payment_record_pk
        except Exception as e:
            print(f"Error inserting payment record function: {str(e)}")
            return False, "Error inserting payment record"
        
        finally:
            connection.close()

    def insertCardIntoStaging(self, card_number, cvv, expiry_date):
        
        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            with connection.cursor() as cursor:

                sql_query = '''
                    INSERT INTO Staging_card (tokenised_pan, cvv, date_expired)
                    VALUES (%s, %s, %s)
                '''
                cursor.execute(sql_query, (card_number, cvv, expiry_date))
                connection.commit()
                return True
            
        except Exception as e:
            print(f"Error inserting card into staging function: {str(e)}")
            return False
        
