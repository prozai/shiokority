import AuditTrail from '../model/auditTrail';  // Import the auditTrail model
class AuditTrailController {

static async getAllAuditTrailLogs() {
    try {
      const auditTrailLogs = await AuditTrail.getAllAuditTrailLogs();  // Fetch audit trail log from the model
      return auditTrailLogs
    } catch (error) {
      console.error('Error in getAllAuditTrailLogs:', error);
      throw error;
    }
  }

  static async getAuditTrailById(auditId) {
    try {
      const auditTrailLog = await AuditTrail.getAuditTrailById(auditId);  // Fetch audit trail by ID from the model
      return auditTrailLog
    } catch (error) {
      console.error('Error in getAuditTrailById:', error);
      throw error;
    }
  }
};

export default AuditTrailController;