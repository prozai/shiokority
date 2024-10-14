import React, { useState } from 'react';
import { CreditCard, Calendar, Lock } from 'lucide-react';

const CardValidation = () => {
  const [cardData, setCardData] = useState({
    cardNumber: '',
    expirationDate: '',
    cvv: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCardData({ ...cardData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you would typically send the card data to a server for validation
    console.log('Card data submitted:', cardData);
    // You can add your validation logic here
  };

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-light-blue-500 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <div className="max-w-md mx-auto">
            <div>
              <h1 className="text-2xl font-semibold">Card Details</h1>
            </div>
            <div className="divide-y divide-gray-200">
              <form onSubmit={handleSubmit} className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                <div className="relative">
                  <input
                    id="cardNumber"
                    name="cardNumber"
                    type="text"
                    className="peer placeholder-transparent h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
                    placeholder="Card Number"
                    value={cardData.cardNumber}
                    onChange={handleChange}
                  />
                  <label htmlFor="cardNumber" className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm">Card Number</label>
                  <CreditCard className="absolute right-0 top-2 h-6 w-6 text-gray-400" />
                </div>
                <div className="relative">
                  <input
                    id="expirationDate"
                    name="expirationDate"
                    type="text"
                    className="peer placeholder-transparent h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
                    placeholder="MM/YY"
                    value={cardData.expirationDate}
                    onChange={handleChange}
                  />
                  <label htmlFor="expirationDate" className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm">Expiration Date (MM/YY)</label>
                  <Calendar className="absolute right-0 top-2 h-6 w-6 text-gray-400" />
                </div>
                <div className="relative">
                  <input
                    id="cvv"
                    name="cvv"
                    type="text"
                    className="peer placeholder-transparent h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
                    placeholder="CVV"
                    value={cardData.cvv}
                    onChange={handleChange}
                  />
                  <label htmlFor="cvv" className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm">CVV</label>
                  <Lock className="absolute right-0 top-2 h-6 w-6 text-gray-400" />
                </div>
                <div className="relative">
                  <button className="bg-blue-500 text-white rounded-md px-4 py-2 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-50">Validate Card</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CardValidation;