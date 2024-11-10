import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import AuditTrailController from '../controller/auditTrailController';
import AdministratorController from '../controller/administratorController';
import TopNavbar from '../components/TopNavBar';
import Sidebar from '../components/SideBar';
import { 
    FiChevronsLeft, 
    FiChevronLeft, 
    FiChevronRight, 
    FiChevronsRight,
    FiSearch,
    FiFilter,
    FiCalendar,
    FiX,
    FiDownload,
    FiRefreshCw
} from 'react-icons/fi';
import { 
    MdOutlineViewDay,
    MdOutlineViewStream
} from "react-icons/md";

const AuditTrail = () => {
    // State management
    const [auditLogs, setAuditLogs] = useState([]);
    const [filteredLogs, setFilteredLogs] = useState([]);
    const [searchType, setSearchType] = useState('id');
    const [searchTerm, setSearchTerm] = useState('');
    const [methodFilter, setMethodFilter] = useState('');
    const [sortOrder, setSortOrder] = useState('desc');
    const [currentPage, setCurrentPage] = useState(1);
    const [logsPerPage, setLogsPerPage] = useState(10);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [status, setStatus] = useState('');
    const [viewMode, setViewMode] = useState('paginated');
    const [refreshInterval, setRefreshInterval] = useState(null);
    const [lastRefresh, setLastRefresh] = useState(new Date());
    
    const scrollContainerRef = useRef(null);
    const navigate = useNavigate();

    // Get unique methods for filter dropdown
    const uniqueMethods = [...new Set(auditLogs.map(log => log.audit_trail_method))];

    // Fetch logs
    const fetchLogs = async (showLoading = true) => {
        if (showLoading) setLoading(true);
        setError(null);
        try {
            let data;
            if (searchTerm && searchType === 'id') {
                data = await AuditTrailController.getAuditTrailById(searchTerm);
            } else {
                data = await AuditTrailController.getAllAuditTrailLogs();
            }
            const sortedData = Array.isArray(data) ? data : [];
            setAuditLogs(sortedData);
            setLastRefresh(new Date());
        } catch (error) {
            console.error('Error fetching audit logs:', error);
            setError('Failed to fetch audit logs. Please try again later.');
            setAuditLogs([]);
        } finally {
            if (showLoading) setLoading(false);
        }
    };

    // Initial fetch and refresh interval
    useEffect(() => {
        fetchLogs();
        const interval = setInterval(() => {
            fetchLogs(false);
        }, 30000); // Refresh every 30 seconds
        setRefreshInterval(interval);

        return () => {
            if (interval) clearInterval(interval);
        };
    }, []);

    // Filter and sort logs
    useEffect(() => {
        let result = [...auditLogs];

        // Apply search filter
        if (searchTerm) {
            if (searchType === 'id') {
                result = result.filter(log => 
                    log.audit_trail_id.toString().includes(searchTerm)
                );
            } else if (searchType === 'description') {
                const searchLower = searchTerm.toLowerCase();
                result = result.filter(log => 
                    log.audit_trail_description.toLowerCase().includes(searchLower)
                );
            }
        }

        // Apply method filter
        if (methodFilter) {
            result = result.filter(log => log.audit_trail_method === methodFilter);
        }

        // Apply sorting
        result.sort((a, b) => {
            const dateA = new Date(a.timestamp);
            const dateB = new Date(b.timestamp);
            return sortOrder === 'asc' ? dateA - dateB : dateB - dateA;
        });

        setFilteredLogs(result);
        setCurrentPage(1);
    }, [auditLogs, methodFilter, sortOrder, searchTerm, searchType]);

    // Dynamic page size adjustment
    useEffect(() => {
        const adjustLogsPerPage = () => {
            const rowHeight = 48;
            const availableHeight = window.innerHeight - 350;
            const maxLogsPerPage = Math.floor(availableHeight / rowHeight);
            setLogsPerPage(Math.max(5, maxLogsPerPage)); // Minimum 5 rows
        };

        adjustLogsPerPage();
        window.addEventListener('resize', adjustLogsPerPage);
        return () => window.removeEventListener('resize', adjustLogsPerPage);
    }, []);

    // Pagination calculations
    const indexOfLastLog = currentPage * logsPerPage;
    const indexOfFirstLog = indexOfLastLog - logsPerPage;
    const currentLogs = viewMode === 'paginated' 
        ? filteredLogs.slice(indexOfFirstLog, indexOfLastLog)
        : filteredLogs;
    const totalPages = Math.ceil(filteredLogs.length / logsPerPage);

    // Handlers
    const handlePageChange = (pageNumber) => setCurrentPage(pageNumber);
    
    const handleSearch = (e) => {
        e.preventDefault();
        setCurrentPage(1);
        fetchLogs();
    };

    const handleMethodFilterChange = (e) => setMethodFilter(e.target.value);
    const toggleSortOrder = () => setSortOrder(prev => prev === 'asc' ? 'desc' : 'asc');
    const toggleViewMode = () => setViewMode(prev => prev === 'paginated' ? 'scroll' : 'paginated');

    const handleManualRefresh = async () => {
        await fetchLogs(true);
    };

    const clearFilters = () => {
        setSearchTerm('');
        setSearchType('id');
        setMethodFilter('');
        setCurrentPage(1);
    };const handleLogout = async () => {
        try {
            await AdministratorController.logout();
            setStatus('Logged out successfully');
            navigate('/login');
        } catch (error) {
            setStatus('Logout failed: ' + error.message);
        }
    };

    const handleSetup2FA = () => navigate('/setup2FA');
    const handleUserManagement = () => navigate('/user-management');
    const handleAuditTrail = () => navigate('/auditTrail');

    // CSV Export functionality
    const downloadCSV = () => {
        const headers = ['ID', 'Method', 'Module', 'Description', 'Timestamp'];
        const csvContent = [
            headers.join(','),
            ...filteredLogs.map(log => [
                log.audit_trail_id,
                log.audit_trail_method,
                log.audit_trail_module,
                `"${log.audit_trail_description.replace(/"/g, '""')}"`,
                log.timestamp
            ].join(','))
        ].join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        
        if (link.download !== undefined) {
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            link.setAttribute('download', `audit_trail_${timestamp}.csv`);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    };

    // Render Functions
    const renderSearchControls = () => (
        <form onSubmit={handleSearch} className="flex flex-wrap gap-4 items-center">
            <div className="flex flex-col sm:flex-row gap-2 sm:gap-4">
                <div className="relative flex-grow">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <FiSearch className="text-gray-400" />
                    </div>
                    <input
                        type="text"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        placeholder={searchType === 'id' ? "Search by ID..." : "Search in descriptions..."}
                        className="pl-10 pr-24 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 w-full sm:w-80"
                    />
                    <div className="absolute inset-y-0 right-0 flex items-center">
                        <select
                            value={searchType}
                            onChange={(e) => setSearchType(e.target.value)}
                            className="h-full py-0 pl-2 pr-7 border-l border-gray-200 bg-gray-50 text-gray-500 rounded-r-lg focus:ring-blue-500 focus:border-blue-500"
                        >
                            <option value="id">ID</option>
                            <option value="description">Description</option>
                        </select>
                    </div>
                </div>
                
                <button 
                    type="submit"
                    className="w-full sm:w-auto px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 flex items-center justify-center gap-2 transition-colors duration-200"
                >
                    <FiSearch size={18} />
                    <span>Search</span>
                </button>
            </div>

            {searchTerm && (
                <button
                    type="button"
                    onClick={() => {
                        setSearchTerm('');
                        setSearchType('id');
                    }}
                    className="px-2 py-1 text-gray-500 hover:text-gray-700 flex items-center gap-1 transition-colors duration-200"
                >
                    <FiX size={16} />
                    <span className="text-sm">Clear search</span>
                </button>
            )}
        </form>
    );

    const renderFilterControls = () => (
        <div className="flex flex-wrap gap-4 items-center">
            <div className="relative">
                <select
                    value={methodFilter}
                    onChange={handleMethodFilterChange}
                    className="pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none bg-white"
                >
                    <option value="">All Methods</option>
                    {uniqueMethods.map(method => (
                        <option key={method} value={method}>{method}</option>
                    ))}
                </select>
                <FiFilter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            </div>

            <button
                onClick={toggleSortOrder}
                className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 flex items-center gap-2 transition-colors duration-200"
                title={`Sort by Date (${sortOrder === 'asc' ? 'Ascending' : 'Descending'})`}
            >
                <FiCalendar size={18} />
                <span className="hidden sm:inline">Sort by Date</span>
                {sortOrder === 'asc' ? '↑' : '↓'}
            </button>

            <div className="flex gap-2">
                <button
                    onClick={handleManualRefresh}
                    className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 flex items-center gap-2 transition-colors duration-200"
                    title="Refresh Data"
                    disabled={loading}
                >
                    <FiRefreshCw size={18} className={loading ? 'animate-spin' : ''} />
                    <span className="hidden sm:inline">Refresh</span>
                </button>

                <button
                    onClick={downloadCSV}
                    className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 flex items-center gap-2 transition-colors duration-200"
                    title="Export to CSV"
                >
                    <FiDownload size={18} />
                    <span className="hidden sm:inline">Export</span>
                </button>

                <button
                    onClick={toggleViewMode}
                    className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 flex items-center gap-2 transition-colors duration-200"
                    title={viewMode === 'paginated' ? 'Switch to Scroll View' : 'Switch to Paginated View'}
                >
                    {viewMode === 'paginated' ? (
                        <>
                            <MdOutlineViewStream size={20} />
                            <span className="hidden sm:inline">Scroll View</span>
                        </>
                    ) : (
                        <>
                            <MdOutlineViewDay size={20} />
                            <span className="hidden sm:inline">Paginated View</span>
                        </>
                    )}
                </button>
            </div>

            {(methodFilter || searchTerm) && (
                <button
                    onClick={clearFilters}
                    className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 flex items-center gap-2 transition-colors duration-200"
                    title="Clear All Filters"
                >
                    <FiX size={18} />
                    <span className="hidden sm:inline">Clear All</span>
                </button>
            )}
        </div>
    );const renderPagination = () => (
        <div className="mt-4 flex justify-center flex-wrap gap-2">
            <button
                onClick={() => handlePageChange(1)}
                disabled={currentPage === 1}
                className="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50 
                         flex items-center gap-1 transition-colors duration-200"
                title="First Page"
            >
                <FiChevronsLeft size={18} />
                <span className="hidden sm:inline">First</span>
            </button>

            <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
                className="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50 
                         flex items-center gap-1 transition-colors duration-200"
                title="Previous Page"
            >
                <FiChevronLeft size={18} />
                <span className="hidden sm:inline">Previous</span>
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
                        className={`px-3 py-1 rounded transition-colors duration-200 ${
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
                className="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50 
                         flex items-center gap-1 transition-colors duration-200"
                title="Next Page"
            >
                <span className="hidden sm:inline">Next</span>
                <FiChevronRight size={18} />
            </button>

            <button
                onClick={() => handlePageChange(totalPages)}
                disabled={currentPage === totalPages}
                className="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50 
                         flex items-center gap-1 transition-colors duration-200"
                title="Last Page"
            >
                <span className="hidden sm:inline">Last</span>
                <FiChevronsRight size={18} />
            </button>
        </div>
    );

    const renderTable = () => (
        <div 
            ref={scrollContainerRef}
            className={`bg-white rounded-lg shadow overflow-hidden overflow-x-auto
                       ${viewMode === 'scroll' ? 'max-h-[calc(100vh-300px)] overflow-y-auto' : ''}`}
        >
            <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50 sticky top-0">
                    <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            ID
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Method
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Module
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Description
                        </th>
                        <th 
                            className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors duration-200"
                            onClick={toggleSortOrder}
                            title={`Sort by Date (${sortOrder === 'asc' ? 'Ascending' : 'Descending'})`}
                        >
                            Timestamp {sortOrder === 'asc' ? '↑' : '↓'}
                        </th>
                    </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                    {currentLogs.length > 0 ? (
                        currentLogs.map((log) => (
                            <tr key={log.audit_trail_id} className="hover:bg-gray-50 transition-colors duration-150">
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className="text-sm font-medium text-gray-900">
                                        {log.audit_trail_id}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full
                                        ${getMethodColor(log.audit_trail_method)}`}>
                                        {log.audit_trail_method}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className="text-sm text-gray-900">
                                        {log.audit_trail_module}
                                    </span>
                                </td>
                                <td className="px-6 py-4">
                                    <span className="text-sm text-gray-500 break-words max-w-lg block">
                                        {log.audit_trail_description}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {formatTimestamp(log.timestamp)}
                                </td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="5" className="px-6 py-4 text-center text-gray-500">
                                {loading ? 'Loading...' : 'No audit logs found'}
                            </td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );

    // Helper functions
    const getMethodColor = (method) => {
        const colors = {
            'GET': 'bg-blue-100 text-blue-800',
            'POST': 'bg-green-100 text-green-800',
            'PUT': 'bg-yellow-100 text-yellow-800',
            'DELETE': 'bg-red-100 text-red-800',
            'PATCH': 'bg-purple-100 text-purple-800',
            'INSERT': 'bg-indigo-100 text-indigo-800',
            'UPDATE': 'bg-orange-100 text-orange-800'
        };
        return colors[method] || 'bg-gray-100 text-gray-800';
    };

    const formatTimestamp = (timestamp) => {
        try {
            const date = new Date(timestamp);
            return new Intl.DateTimeFormat('en-GB', {
                day: '2-digit',
                month: 'short',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false
            }).format(date);
        } catch (error) {
            console.error('Error formatting timestamp:', error);
            return timestamp;
        }
    };return (
        <div className="flex h-screen bg-gray-200">
            <Sidebar 
                handleLogout={handleLogout} 
                handleSetup2FA={handleSetup2FA} 
                handleUserManagement={handleUserManagement}
                handleAuditTrail={handleAuditTrail}
            />
            <div className="flex flex-col min-h-screen bg-gray-100 w-full">
                <TopNavbar title="Audit Trail" />
                
                <div className="p-6 space-y-6">
                    {/* Controls Section */}
                    <div className="space-y-4">
                        {renderSearchControls()}
                        {renderFilterControls()}
                        
                        {/* Info Bar */}
                        <div className="flex flex-wrap justify-between items-center text-sm text-gray-600">
                            <div className="flex items-center gap-2">
                                <span>
                                    Showing {filteredLogs.length} results
                                    {methodFilter && ` for method: ${methodFilter}`}
                                    {searchTerm && ` matching "${searchTerm}"`}
                                </span>
                            </div>
                            <div className="flex items-center gap-2 text-gray-500">
                                <span>Last updated:</span>
                                <span>{formatTimestamp(lastRefresh)}</span>
                            </div>
                        </div>
                    </div>

                    {/* Loading State */}
                    {loading && (
                        <div className="flex justify-center items-center py-8">
                            <div className="flex flex-col items-center gap-2">
                                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                                <span className="text-gray-500">Loading audit logs...</span>
                            </div>
                        </div>
                    )}

                    {/* Error State */}
                    {error && (
                        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                                    </svg>
                                </div>
                                <div className="ml-3">
                                    <p className="text-sm text-red-700">
                                        {error}
                                    </p>
                                </div>
                                <div className="ml-auto pl-3">
                                    <div className="-mx-1.5 -my-1.5">
                                        <button
                                            onClick={() => setError(null)}
                                            className="inline-flex rounded-md p-1.5 text-red-500 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-600 focus:ring-offset-2"
                                        >
                                            <span className="sr-only">Dismiss</span>
                                            <FiX className="h-5 w-5" />
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Table Section */}
                    {!loading && !error && (
                        <div className="space-y-4">
                            {renderTable()}
                            
                            {/* Pagination */}
                            {viewMode === 'paginated' && totalPages > 1 && renderPagination()}
                            
                            {/* Mobile View Info */}
                            <div className="sm:hidden text-center text-sm text-gray-500">
                                Swipe horizontally to view more columns
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

// Method badge component for reuse
const MethodBadge = ({ method }) => {
    const getMethodColor = (method) => {
        const colors = {
            'GET': 'bg-blue-100 text-blue-800',
            'POST': 'bg-green-100 text-green-800',
            'PUT': 'bg-yellow-100 text-yellow-800',
            'DELETE': 'bg-red-100 text-red-800',
            'PATCH': 'bg-purple-100 text-purple-800',
            'INSERT': 'bg-indigo-100 text-indigo-800',
            'UPDATE': 'bg-orange-100 text-orange-800'
        };
        return colors[method] || 'bg-gray-100 text-gray-800';
    };

    return (
        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getMethodColor(method)}`}>
            {method}
        </span>
    );
};

export default AuditTrail;