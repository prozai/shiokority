// src/views/ViewUser.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FiEdit } from 'react-icons/fi';
import AdministratorController from '../controller/administratorController';


const UserList = () => {
  const [users, setUsers] = useState([]);
  const [statusMessage, setStatusMessage] = useState('');
  const [error, setError] = useState('');
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

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h3 className="text-2xl font-bold mb-4">User Management</h3>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex justify-between items-center mb-4">
          <input type="text" placeholder="Search ID" className="border rounded-lg p-2 w-1/4" />
          <button onClick={handleAddUsers} className="bg-[#153247] text-white py-2 px-4 rounded-lg hover:bg-green-600">
            + Add Users
          </button>
        </div>

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
            {users.map(user => (
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
    </div>
  );
};

export default UserList;
