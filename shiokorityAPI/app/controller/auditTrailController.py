from ..models.auditTrail import AuditTrail

class AuditTrailController:
    def __init__(self):
        self.audit_trail_model = AuditTrail()

    def log_action(self, method, module, description):
        """
        Logs an action in the audit trail.
        
        Parameters:
            method (str): The HTTP method or action type
            module (str): The module where the action occurred
            description (str): Description of the action
            
        Returns:
            bool: True if logging successful, False otherwise
        """
        return self.audit_trail_model.log_entry(method, module, description)

    def get_all_logs(self):
        """
        Retrieves all audit trail logs.
        
        Returns:
            list: List of all audit trail entries
        """
        return self.audit_trail_model.get_all_logs()

    def get_log_by_id(self, audit_id):
        """
        Retrieves a specific audit trail log by ID.
        
        Parameters:
            audit_id (int): The ID of the audit trail entry to retrieve
            
        Returns:
            dict: The audit trail entry if found, None otherwise
        """
        return self.audit_trail_model.get_log_by_id(audit_id)  # Fixed: using audit_id instead of module

    def get_logs_by_module(self, module):
        """
        Retrieves audit trail logs for a specific module.
        
        Parameters:
            module (str): The module name to filter logs by
            
        Returns:
            list: List of audit trail entries for the specified module
        """
        return self.audit_trail_model.get_logs_by_module(module)