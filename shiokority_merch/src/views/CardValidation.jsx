import React, { useState } from 'react';

const CardValidation = ({ onChange }) => {
  const [errors, setErrors] = useState({});

  const validateCardNumber = (number) => {
    const regex = /^[0-9]{16}$/;
    return regex.test(number) ? "" : "Card number must be 16 digits";
  };

  const validateExpiryDate = (date) => {
    const regex = /^(0[1-9]|1[0-2])\/([0-9]{2})$/;
    if (!regex.test(date)) {
      return "Invalid format (MM/YY)";
    }
    const [month, year] = date.split('/');
    const expiryDate = new Date(2000 + parseInt(year), month - 1);
    const today = new Date();
    return expiryDate > today ? "" : "Card has expired";
  };

  const validateCVV = (cvv) => {
    const regex = /^[0-9]{3}$/;
    return regex.test(cvv) ? "" : "CVV must be 3 digits";
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    let error = '';
    let updatedValue = value;

    switch (name) {
      case 'cardNumber':
        updatedValue = value.slice(0, 16);
        error = validateCardNumber(updatedValue);
        break;
      case 'expiryDate':
        error = validateExpiryDate(value);
        break;
      case 'cvv':
        updatedValue = value.slice(0, 3);
        error = validateCVV(updatedValue);
        break;
      default:
        break;
    }

    setErrors(prev => ({ ...prev, [name]: error }));
    onChange({ [name]: updatedValue }, error === '');
  };

  return (
    <div className="space-y-4">
      <div>
        <input
          type="text"
          name="cardNumber"
          placeholder="Card Number (16 digits)"
          onChange={handleChange}
          maxLength={16}
          required
          className={`w-full px-3 py-2 placeholder-gray-300 border rounded-md focus:outline-none focus:ring focus:ring-indigo-100 focus:border-indigo-300 ${errors.cardNumber ? 'border-red-500' : 'border-gray-300'}`}
        />
        {errors.cardNumber && <p className="mt-1 text-xs text-red-500">{errors.cardNumber}</p>}
      </div>
      <div className="flex space-x-4">
        <div className="w-1/2">
          <input
            type="text"
            name="expiryDate"
            placeholder="MM/YY"
            onChange={handleChange}
            maxLength={5}
            required
            className={`w-full px-3 py-2 placeholder-gray-300 border rounded-md focus:outline-none focus:ring focus:ring-indigo-100 focus:border-indigo-300 ${errors.expiryDate ? 'border-red-500' : 'border-gray-300'}`}
          />
          {errors.expiryDate && <p className="mt-1 text-xs text-red-500">{errors.expiryDate}</p>}
        </div>
        <div className="w-1/2">
          <input
            type="text"
            name="cvv"
            placeholder="CVV"
            onChange={handleChange}
            maxLength={3}
            required
            className={`w-full px-3 py-2 placeholder-gray-300 border rounded-md focus:outline-none focus:ring focus:ring-indigo-100 focus:border-indigo-300 ${errors.cvv ? 'border-red-500' : 'border-gray-300'}`}
          />
          {errors.cvv && <p className="mt-1 text-xs text-red-500">{errors.cvv}</p>}
        </div>
      </div>
    </div>
  );
};

export default CardValidation;