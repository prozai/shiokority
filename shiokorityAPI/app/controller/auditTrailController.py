from ..models.auditTrail import AuditTrail  # Import the AuditTrail model

class AuditTrailController:
    def __init__(self):
        self.audit_trail_model = AuditTrail()

    def log_action(self, method, module, description):
        return self.audit_trail_model.log_entry(method, module, description)

    def get_all_logs(self):
        return self.audit_trail_model.get_all_logs()

    def get_logs_by_module(self, module):
        return self.audit_trail_model.get_logs_by_module(module)
