import axios from 'axios';

import { ADMIN_PREFIX } from '../model/administrator';

class AuditTrail {

  constructor(audit_id, method, module, description, timestamp) {
    this.audit_id = audit_id;
    this.method = method;
    this.module = module;
    this.description = description;
    this.timestamp = timestamp;
  }
  
static async getAllAuditTrailLogs() {
    try {
      const response = await axios.get(`${ADMIN_PREFIX}/getAllAuditTrailLogs`);
      const auditTrailLog = await response.json();

      return auditTrailLog.map(
        (auditTrail) =>
          new AuditTrail(
            auditTrail.audit_id,
            auditTrail.method,
            auditTrail.module,
            auditTrail.description,
            auditTrail.timestamp,
          )
      );
    } catch (error) {
      console.error('Error fetching all audit trail logs:', error);
      throw error;
    }
  }

  static async getAuditTrailById(auditId) {
    try {
      const response = await axios.get(`${ADMIN_PREFIX}/getAuditTrailById/${auditId}`);
      const auditTrailLog = await response.json();

      return auditTrailLog.map(
        (auditTrail) =>
          new AuditTrail(
            auditTrail.audit_id,
            auditTrail.method,
            auditTrail.module,
            auditTrail.description,
            auditTrail.timestamp,
          )
      );
    } catch (error) {
      console.error('Error fetching audit trail log by ID:', error);
      throw error;
    }
  }

}

export default AuditTrail;