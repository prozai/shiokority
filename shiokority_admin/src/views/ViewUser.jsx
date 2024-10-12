import React, { useState, useEffect } from 'react';
import AdministratorController from '../controller/administratorController';
import { useNavigate } from 'react-router-dom';

const UserList = () => {
  const [users, setUsers] = useState([]);
  const [statusMessage, setStatusMessage] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Fetch all users when component is loaded
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

  // Handle when the user clicks to edit a particular user
  const handleEdit = (user) => {
    navigate(`/EditUser/${user.cust_id}`);
  };

  return (
    <div>
      <h2>View Users</h2>
      {statusMessage && <p>{statusMessage}</p>}
      {error && <p>{error}</p>}
      {!error && (
        <div>
          <table>
            <thead>
              <tr>
                <th>User ID</th>
                <th>Email</th>
                <th>First Name</th>
                <th>Last Name</th>
                <th>Address</th>
                <th>Phone</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.cust_id}>
                  <td>{user.cust_id}</td>
                  <td>{user.cust_email}</td>
                  <td>{user.cust_fname}</td>
                  <td>{user.cust_lname}</td>
                  <td>{user.cust_address}</td>
                  <td>{user.cust_phone}</td>
                  <td>{user.cust_status ? 'Active' : 'Deactivated'}</td>
                  <td>
                    <button onClick={() => handleEdit(user)}>Edit</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default UserList;