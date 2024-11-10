// src/model/auditTrail.jsx
import api from '../services/api';

class AuditTrail {
    constructor(audit_trail_id, audit_trail_method, audit_trail_module, audit_trail_description, audit_trail_timestamp) {
        this.audit_trail_id = audit_trail_id;
        this.audit_trail_method = audit_trail_method;
        this.audit_trail_module = audit_trail_module;
        this.audit_trail_description = audit_trail_description;
        this.audit_trail_timestamp = audit_trail_timestamp;
    }
    
    static async getAllAuditTrailLogs() {
        try {
            const response = await api.get('/admin/getAllAuditTrailLogs');
            return response.data || [];
        } catch (error) {
            console.error('Error fetching all audit trail logs:', error);
            return [];
        }
    }

    static async getAuditTrailById(auditId) {
        try {
            if (!auditId) return [];
            const response = await api.get(`/admin/getAuditTrailById/${auditId}`);
            return response.data ? [response.data] : [];
        } catch (error) {
            console.error('Error fetching audit trail log by ID:', error);
            return [];
        }
    }
}

export default AuditTrail;