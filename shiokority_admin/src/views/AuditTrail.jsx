import React, { useState, useEffect } from 'react';
import AuditTrailController from '../controller/auditTrailController';

const AuditTrail = () => {

  const [auditLogs, setAuditLogs] = useState([]);
  const [searchId, setSearchId] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [logsPerPage] = useState(10); // Define the number of logs per page

  // Fetch audit logs when the component mounts or searchId/currentPage changes
  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const data = searchId
          ? await AuditTrailController.getAuditTrailById(searchId)
          : await AuditTrailController.getAllAuditTrailLogs(currentPage, logsPerPage);
        setAuditLogs(data.logs);
      } catch (error) {
        console.error('Error fetching audit logs:', error);
      }
    };
    fetchLogs();
  }, [searchId, currentPage, logsPerPage]); // Add logsPerPage here
  

  // Pagination handling
  const handlePageChange = (pageNumber) => setCurrentPage(pageNumber);


  // Render pagination buttons
  const renderPagination = () => {
    const totalPages = Math.ceil(auditLogs.totalCount / logsPerPage);
    const pages = [];
    for (let i = 1; i <= totalPages; i++) {
      pages.push(
        <button
          key={i}
          onClick={() => handlePageChange(i)}
          className={i === currentPage ? 'active' : ''}
        >
          {i}
        </button>
      );
    }
    return pages;
  };

  return (
    <div>
      <h1>View Audit Trail</h1>
      <input
        type="text"
        placeholder="Search by Audit Trail ID"
        value={searchId}
        onChange={(e) => setSearchId(e.target.value)}
      />
      <button onClick={() => setCurrentPage(1)}>Search</button>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Method</th>
            <th>Module</th>
            <th>Description</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {auditLogs.logs && auditLogs.logs.length ? (
            auditLogs.logs.map((log) => (
              <tr key={log.audit_id}>
                <td>{log.audit_id}</td>
                <td>{log.method}</td>
                <td>{log.module}</td>
                <td>{log.description}</td>
                <td>{log.timestamp}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5">No audit logs found</td>
            </tr>
          )}
        </tbody>
      </table>

      <div className="pagination">{renderPagination()}</div>
    </div>
  );

  return (
    <div>
      <h1>View Audit Trail</h1>
      <input
        type="text"
        placeholder="Search by Audit Trail ID"
        value={searchId}
        onChange={(e) => setSearchId(e.target.value)}
      />
      <button onClick={() => setCurrentPage(1)}>Search</button>
      
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Method</th>
            <th>Module</th>
            <th>Description</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {auditLogs.length ? (
            auditLogs.map((log) => (
              <tr key={log.audit_id}>
                <td>{log.audit_id}</td>
                <td>{log.method}</td>
                <td>{log.module}</td>
                <td>{log.description}</td>
                <td>{log.timestamp}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5">No audit logs found</td>
            </tr>
          )}
        </tbody>
      </table>
      
      <div className="pagination">{renderPagination()}</div>
    </div>
  );
  
};

export default AuditTrail;
