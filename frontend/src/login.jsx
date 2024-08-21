import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [status, setStatus] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await axios.post('/login/admin', {
                username,
                password,
            });

            if (response.data.success) {
                console.log('Login successful:', response.data);
                // Handle successful login, maybe redirect or show a success message
                navigate('/dashboard');
            }
            else {
                setStatus('Login failed: Incorrect username or password.');
            }
        } catch (error) {
            if (error.response) {
                console.log('Login failed:', error.response.data);
                setStatus('Login failed')
            } else {
                console.error('Error:', error);
                setStatus('An error occurred during login. Please try again.');
            }
        }
    };

    return (
        <div>
            <h2>Login</h2>
            {status && <p>{status}</p>} 
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username </label>
                    <input 
                        type="text" 
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <div>
                    <label>Password </label>
                    <input 
                        type="password" 
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button type="submit">Login</button>
                
            </form>
        </div>
    );
}

export default Login;
