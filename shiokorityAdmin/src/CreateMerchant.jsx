import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';

function CreateMerchant() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const createMerchantMutation = useMutation({
    mutationFn: async (merchantData) => {
      const response = await fetch('/create-merchant', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(merchantData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Merchant creation failed!');
      }

      return response.json();
    },
    onSuccess: () => {
      setSuccess(true);
      setError(null);
      setName(''); // Clear the form fields on success
      setEmail('');
      setPhone('');
    },
    onError: (error) => {
      setSuccess(false);
      setError(error.message || 'An error occurred while creating the merchant.');
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();

    const merchantData = {
      name,
      email,
      phone,
    };

    createMerchantMutation.mutate(merchantData);
  };

  return (
    <div>
      <h3>Create Merchant</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Merchant Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <br />
        <input
          type="email"
          placeholder="Merchant Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <br />
        <input
          type="text"
          placeholder="Merchant Phone"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
        />
        <br />
        <button type="submit">Create Merchant</button>

        {error && <p style={{ color: 'red' }}>{error}</p>}
        {success && <p style={{ color: 'green' }}>Merchant created successfully!</p>}
      </form>
    </div>
  );
}

export default CreateMerchant;
