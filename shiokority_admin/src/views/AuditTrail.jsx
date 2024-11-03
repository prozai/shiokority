import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AuditTrailController from '../controller/auditTrailController';
import AdministratorController from '../controller/administratorController';
import TopNavbar from '../components/TopNavBar';
import Sidebar from '../components/SideBar'; // Import Sidebar component
import TopNotificationBar from '../components/TopNotificationBar'; // Import TopNotificationBar component

const AuditTrail = () => {
    const [auditLogs, setAuditLogs] = useState([]);
    const [searchId, setSearchId] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const [logsPerPage, setLogsPerPage] = useState(10);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [status, setStatus] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchLogs = async () => {
            setLoading(true);
            setError(null);
            try {
                let data;
                if (searchId) {
                    data = await AuditTrailController.getAuditTrailById(searchId);
                } else {
                    data = await AuditTrailController.getAllAuditTrailLogs();
                }
                setAuditLogs(Array.isArray(data) ? data : []);
            } catch (error) {
                console.error('Error fetching audit logs:', error);
                setError('Failed to fetch audit logs. Please try again later.');
                setAuditLogs([]);
            } finally {
                setLoading(false);
            }
        };
        fetchLogs();
    }, [searchId]);
    
    // Adjust logsPerPage dynamically based on screen height
    useEffect(() => {
        const adjustLogsPerPage = () => {
            const rowHeight = 48; // row height in pixels
            const availableHeight = window.innerHeight - 350; // Deducting space for navbar, search bar, etc.
            const maxLogsPerPage = Math.floor(availableHeight / rowHeight);
            setLogsPerPage(maxLogsPerPage);
        };

        adjustLogsPerPage();
        window.addEventListener('resize', adjustLogsPerPage);

        return () => {
            window.removeEventListener('resize', adjustLogsPerPage);
        };
    }, []);

    // Calculate pagination
    const indexOfLastLog = currentPage * logsPerPage;
    const indexOfFirstLog = indexOfLastLog - logsPerPage;
    const currentLogs = auditLogs.slice(indexOfFirstLog, indexOfLastLog);
    const totalPages = Math.ceil(auditLogs.length / logsPerPage);

    const handlePageChange = (pageNumber) => {
        setCurrentPage(pageNumber);
    };

    const handleSearch = () => {
        setCurrentPage(1);
    };

    const handleLogout = async () => {
      try {
        await AdministratorController.logout();
        setStatus('Logged out successfully');
        navigate('/login');
      } catch (error) {
        setStatus('Logout failed: ' + error.message);
      }
    };
  
    const handleSetup2FA = () => {
      navigate('/setup2FA');
    };
  
    const handleUserManagement = () => {
      navigate('/user-management');
    };
  
    const handleAuditTrail = () => {
      navigate('/auditTrail');
    };
    const initialAlerts = [
      { color: 'bg-red-500', message: 'Red Alert' },
      // { color: 'bg-gray-500', message: 'Gray Alert' },
      // { color: 'bg-green-500', message: 'Green Alert' },
      // { color: 'bg-orange-500', message: 'Orange Alert' },
      // { color: 'bg-blue-500', message: 'Blue Alert' },
      // { color: 'bg-black', message: 'Black Alert' },
    ];
    
    return (
    <div className="flex h-screen bg-gray-200">
      {/* Use Sidebar Component */}
      <Sidebar 
        handleLogout={handleLogout} 
        handleSetup2FA={handleSetup2FA} 
        handleUserManagement={handleUserManagement}
        handleAuditTrail={handleAuditTrail}
      />
        <div className="flex flex-col min-h-screen bg-gray-100 w-full">
            <TopNavbar title="Audit Trail" />
            
            <div className="p-6">
                <div className="mb-6 flex gap-4">
                    <input
                        type="text"
                        placeholder="Search by Audit Trail ID"
                        value={searchId}
                        onChange={(e) => setSearchId(e.target.value)}
                        className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button 
                        onClick={handleSearch}
                        className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                    >
                        Search
                    </button>
                </div>

                {loading && (
                    <div className="text-center py-4">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
                    </div>
                )}

                {error && (
                    <div className="text-red-500 text-center py-4 bg-red-50 border border-red-200 rounded-lg">
                        {error}
                    </div>
                )}
                
                <div className="bg-white rounded-lg shadow overflow-hidden overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Method</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Module</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Timestamp</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {currentLogs.length > 0 ? (
                                currentLogs.map((log) => (
                                    <tr key={log.audit_trail_id} className="hover:bg-gray-50">
                                        <td className="px-6 py-4 whitespace-nowrap">{log.audit_trail_id}</td>
                                        <td className="px-6 py-4 whitespace-nowrap">{log.audit_trail_method}</td>
                                        <td className="px-6 py-4 whitespace-nowrap">{log.audit_trail_module}</td>
                                        <td className="px-6 py-4 break-words max-w-lg">{log.audit_trail_description}</td>
                                        <td className="px-6 py-4 whitespace-nowrap">{log.timestamp}</td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="5" className="px-6 py-4 text-center text-gray-500">
                                        No audit logs found
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>

                {!loading && !error && totalPages > 1 && (
                    <div className="mt-4 flex justify-center flex-wrap gap-2">
                        <button
                            onClick={() => handlePageChange(1)}
                            disabled={currentPage === 1}
                            className="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
                        >
                            First
                        </button>
                        <button
                            onClick={() => handlePageChange(currentPage - 1)}
                            disabled={currentPage === 1}
                            className="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
                        >
                            Previous
                        </button>
                        {[...Array(Math.min(5, totalPages))].map((_, index) => {
                            let pageNum;
                            if (totalPages <= 5) {
                                pageNum = index + 1;
                            } else if (currentPage <= 3) {
                                pageNum = index + 1;
                            } else if (currentPage >= totalPages - 2) {
                                pageNum = totalPages - 4 + index;
                            } else {
                                pageNum = currentPage - 2 + index;
                            }
                            return (
                                <button
                                    key={pageNum}
                                    onClick={() => handlePageChange(pageNum)}
                                    className={`px-3 py-1 rounded ${
                                        currentPage === pageNum
                                            ? 'bg-blue-500 text-white'
                                            : 'bg-gray-200 hover:bg-gray-300'
                                    }`}
                                >
                                    {pageNum}
                                </button>
                            );
                        })}
                        <button
                            onClick={() => handlePageChange(currentPage + 1)}
                            disabled={currentPage === totalPages}
                            className="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
                        >
                            Next
                        </button>
                        <button
                            onClick={() => handlePageChange(totalPages)}
                            disabled={currentPage === totalPages}
                            className="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
                        >
                            Last
                        </button>
                    </div>
                )}
            </div>
        </div>
      </div>
    );
};

export default AuditTrail;