import React, { useState } from 'react';
import AdministratorController from '../controller/administratorController';

const MerchantForm = () => {
  const [ formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '' 
  });
  const [status, setStatus] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('Submitting...');
    try {
      await AdministratorController.createMerchant(formData);
      setStatus('Merchant created successfully!');
      setFormData({ name: '', email: '', phone: '', address: '' }); 
    } catch (error) {
      setStatus(`Error: ${error.message}`);
    }
  };

  return (
    <form onSubmit={handleSubmit}>

      <br />
      <div>
        <input
          type="text"
          id="name"
          name="name"
          placeholder='Merchant Name'
          value={formData.name}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <input
          type="email"
          id="email"
          name="email"
          placeholder='Merchant Email'
          value={formData.email}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <input
          type="tel"
          id="phone"
          name="phone"
          placeholder='Merchant Phone Number'
          value={formData.phone}
          onChange={handleChange}
          required
        />
      </div>
      
      <div>
        <input 
        type="text"
        id="address"
        name="address"
        placeholder='merchant address'
        value={formData.address}
        onChange={handleChange}
        required 
        
        />
      </div>
      
      <button type="submit">Create Merchant</button>
      {status && <p>{status}</p>}
    </form>
  );
};

export default MerchantForm;


