import React, { useState, useEffect } from 'react';
import AdministratorController from '../controller/administratorController'; // Assuming you have a controller
import { useParams, useNavigate } from 'react-router-dom';

const EditUser = () => {
  const { cust_id } = useParams(); // Get the cust_id from the URL
  const [email, setEmail] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [address, setAddress] = useState('');
  const [phone, setPhone] = useState('');
  const [status, setStatus] = useState('');
  const [statusMessage, setStatusMessage] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Fetch user details based on cust_id when component loads
  useEffect(() => {
    const fetchUserDetails = async () => {
      setStatusMessage('Loading user details...');
      try {
        const user = await AdministratorController.getUserById(cust_id);
        if (user) {
          setEmail(user.cust_email);
          setFirstName(user.cust_fname);
          setLastName(user.cust_lname);
          setAddress(user.cust_address);
          setPhone(user.cust_phone);
          setStatus(user.cust_status);
        }
        setStatusMessage('');
      } catch (error) {
        setError('Failed to load user details. Please try again later.');
      }
    };

    fetchUserDetails();
  }, [cust_id]);

  // Handle when the user updates the user details and saves the changes
  const handleUpdateUser = async (event) => {
    event.preventDefault();
    setStatusMessage('Updating user...');

    try {
      const response = await AdministratorController.updateUser(cust_id, {
        email,
        first_name: firstName,
        last_name: lastName,
        address,
        phone,
        status
      });

      if (response.success) {
        setStatusMessage('User updated successfully.');
        navigate('/dashboard'); // Redirect back to the user list or another page
      } else {
        setError('Failed to update user: ' + response.message);
      }
    } catch (error) {
      setError('An error occurred while updating the user.');
    }
  };

  return (
    <div>
      {statusMessage && <p>{statusMessage}</p>}
      {error && <p>{error}</p>}
      <h2>Editing user with ID: {cust_id}</h2>
      {!error && (
        <div>
          <form onSubmit={handleUpdateUser}>
            <div>
              <label>Email: </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <label>First Name: </label>
              <input
                type="text"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
              />
            </div>
            <div>
              <label>Last Name: </label>
              <input
                type="text"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
              />
            </div>
            <div>
              <label>Address: </label>
              <input
                type="text"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
              />
            </div>
            <div>
              <label>Phone: </label>
              <input
                type="text"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
              />
            </div>
            <div>
              <label>Status: </label>
              <select
                value={status}
                onChange={(e) => setStatus(e.target.value)}
              >
                <option value="1">Active</option>
                <option value="0">Deactivate</option>
              </select>
            </div>
            <button type="submit">Update User</button>
            <button type="button" onClick={() => navigate('/dashboard')}>
              Cancel
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default EditUser;