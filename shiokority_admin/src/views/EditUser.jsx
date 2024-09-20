import React, { useState, useEffect } from 'react';
import AdministratorController from '../controller/administratorController'; // Assuming you have a controller
import { useNavigate } from 'react-router-dom';

const EditUser = () => {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [email, setEmail] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [status, setStatus] = useState('');
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
    setSelectedUser(user.user_id);
    setEmail(user.user_email);
    setFirstName(user.first_name);
    setLastName(user.last_name);
    setStatus(user.status);
  };

  // Handle when the user updates a particular user and saves the changes
  const handleUpdateUser = async (event) => {
    event.preventDefault();
    setStatusMessage('Updating user...');

    try {
      const response = await AdministratorController.updateUser(selectedUser, {
        email,
        first_name: firstName,
        last_name: lastName,
        status
      });

      if (response.success) {
        setUsers(users.map(user =>
          user.user_id === selectedUser
            ? { ...user, user_email: email, first_name: firstName, last_name: lastName, status }
            : user
        ));
        setSelectedUser(null);
        setStatusMessage('User updated successfully.');
      } else {
        setError('Failed to update user: ' + response.message);
      }
    } catch (error) {
      setError('An error occurred while updating the user.');
    }
  };

  return (
    <div>
      <h2>View Users</h2>
      {statusMessage && <p>{statusMessage}</p>}
      {error && <p>{error}</p>}
      {!error && (
        <>
          <div>
            <table>
              <thead>
                <tr>
                  <th>User ID</th>
                  <th>Email</th>
                  <th>First Name</th>
                  <th>Last Name</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.user_id}>
                    <td>{user.user_id}</td>
                    <td>{user.user_email}</td>
                    <td>{user.first_name}</td>
                    <td>{user.last_name}</td>
                    <td>{user.status ? 'Active' : 'Deactivated'}</td>
                    <td>
                      <button onClick={() => handleEdit(user)}>Edit</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {selectedUser && (
            <div>
              <h3>Edit User</h3>
              <form onSubmit={handleUpdateUser}>
                <div>
                  <label>Email</label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>
                <div>
                  <label>First Name</label>
                  <input
                    type="text"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                  />
                </div>
                <div>
                  <label>Last Name</label>
                  <input
                    type="text"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                  />
                </div>
                <div>
                  <label>Status</label>
                  <select
                    value={status}
                    onChange={(e) => setStatus(e.target.value)}
                  >
                    <option value="1">Active</option>
                    <option value="0">Deactivate</option>
                  </select>
                </div>
                <button type="submit">Update User</button>
                <button type="button" onClick={() => setSelectedUser(null)}>Cancel</button>
              </form>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default EditUser;