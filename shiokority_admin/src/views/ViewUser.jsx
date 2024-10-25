import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FiEdit } from 'react-icons/fi';
import AdministratorController from '../controller/administratorController';

const UserList = () => {
  const [users, setUsers] = useState([]);
  const [statusMessage, setStatusMessage] = useState('');
  const [error, setError] = useState('');
  const [currentPage, setCurrentPage] = useState(1);  // Pagination state
  const [usersPerPage] = useState(5);  // Set number of users per page
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUsers = async () => {
      setStatusMessage('Loading users...');
      try {
        const userList = await AdministratorController.getAllUsers();
        setUsers(userList);
        setStatusMessage('');
      } catch (error) {
        if (error.response && error.response.status === 403) {
          setError('You are not authorized to view the user list.');
          navigate('/login');
        } else {
          setError('Failed to load the user list. Please try again later.');
        }
      }
    };

    fetchUsers();
  }, [navigate]);

  const handleAddUsers = () => {
    navigate('/create-user');
  };

  // Pagination logic
  const indexOfLastUser = currentPage * usersPerPage;
  const indexOfFirstUser = indexOfLastUser - usersPerPage;
  const currentUsers = users.slice(indexOfFirstUser, indexOfLastUser);

  const totalPages = Math.ceil(users.length / usersPerPage);

  const handlePreviousPage = () => {
    setCurrentPage((prevPage) => (prevPage === 1 ? 1 : prevPage - 1));
  };

  const handleNextPage = () => {
    setCurrentPage((prevPage) => (prevPage === totalPages ? totalPages : prevPage + 1));
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      {/* Logo at the top left */}
      <div className="flex items-center mb-4">
        <img
          src={ShiokorityAdminLogo}
          alt="Shiokority Admin"
          className="h-20 mr-4 cursor-pointer"
          onClick={handleLogoClick}
        />
        <h1 className="text-3xl font-bold">User Management</h1>
      </div>
      
      {/* Search and Add User Button */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex justify-between items-center mb-4">
          <input type="text" placeholder="Search ID" className="border rounded-lg p-2 w-1/4" />
          <button onClick={handleAddUsers} className="bg-[#153247] text-white py-2 px-4 rounded-lg hover:bg-green-600">
            + Add Users
          </button>
        </div>

        {/* Limit height and make the table scrollable */}
        <div className="max-h-80 overflow-y-scroll">
          <table className="w-full text-left">
            <thead>
              <tr className="text-gray-600">
                <th className="py-2 px-4 border-b">User ID</th>
                <th className="py-2 px-4 border-b">Email</th>
                <th className="py-2 px-4 border-b">First Name</th>
                <th className="py-2 px-4 border-b">Last Name</th>
                <th className="py-2 px-4 border-b">Address</th>
                <th className="py-2 px-4 border-b">Phone</th>
                <th className="py-2 px-4 border-b">Status</th>
                <th className="py-2 px-4 border-b">Actions</th>
              </tr>
            </thead>
            <tbody>
              {currentUsers.map(user => (
                <tr key={user.cust_id} className="hover:bg-gray-100">
                  <td className="py-2 px-4 border-b">{user.cust_id}</td>
                  <td className="py-2 px-4 border-b">{user.cust_email}</td>
                  <td className="py-2 px-4 border-b">{user.cust_fname}</td>
                  <td className="py-2 px-4 border-b">{user.cust_lname}</td>
                  <td className="py-2 px-4 border-b">{user.cust_address}</td>
                  <td className="py-2 px-4 border-b">{user.cust_phone}</td>
                  <td className="py-2 px-4 border-b">
                    <span className={`px-2 py-1 rounded-full text-xs ${user.cust_status ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'}`}>
                      {user.cust_status ? 'Active' : 'Deactivated'}
                    </span>
                  </td>
                  <td className="py-2 px-4 border-b">
                    <Link to={`/edit-user/${user.cust_id}`} className="text-blue-600 hover:text-blue-800">
                      <FiEdit />
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination controls */}
        <div className="flex justify-between items-center mt-4">
          <button
            onClick={handlePreviousPage}
            className="bg-gray-300 text-gray-800 py-1 px-3 rounded-lg hover:bg-gray-400"
            disabled={currentPage === 1}
          >
            Previous
          </button>
          <span>
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={handleNextPage}
            className="bg-gray-300 text-gray-800 py-1 px-3 rounded-lg hover:bg-gray-400"
            disabled={currentPage === totalPages}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default UserList;
