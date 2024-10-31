import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import consumerController from '../controller/consumerController';
import { 
  Store, 
  MapPin, 
  Building2, 
  Phone, 
  Mail,
  Search,
  Loader2,
  AlertCircle
} from 'lucide-react';

const PayMerchant = () => {
  const [merchants, setMerchants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMerchants = async () => {
      try {
        setLoading(true);
        const merchantData = await consumerController.getMerchantData();
        setMerchants(merchantData);
        setError('');
      } catch (error) {
        console.error('Failed to fetch merchants:', error);
        setError('Failed to load merchants. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchMerchants();
  }, []);

  const handleMerchantClick = (uen) => {
    navigate(`/profile-consumer/${uen}`);
  };

  const filteredMerchants = merchants.filter(merchant => 
    merchant.merch_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    merchant.merch_address.toLowerCase().includes(searchTerm.toLowerCase()) ||
    merchant.merch_uen.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="flex items-center space-x-2 text-blue-600">
          <Loader2 className="h-6 w-6 animate-spin" />
          <span className="font-medium">Loading merchants...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header Section */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="rounded-full bg-blue-100 p-3">
              <Store className="h-8 w-8 text-blue-600" />
            </div>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Available Merchants</h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Select a merchant to proceed with your payment
          </p>
        </div>

        {/* Search Bar */}
        <div className="max-w-xl mx-auto mb-8">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search merchants by name, address, or UEN..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
            />
          </div>
        </div>

        {error ? (
          <div className="flex items-center justify-center text-red-500 space-x-2">
            <AlertCircle className="h-5 w-5" />
            <span>{error}</span>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredMerchants.length > 0 ? (
              filteredMerchants.map((merchant) => (
                <div
                  key={merchant.merch_id}
                  onClick={() => handleMerchantClick(merchant.merch_uen)}
                  className="bg-white rounded-xl shadow-sm hover:shadow-md transition-all duration-200 cursor-pointer border border-gray-200 overflow-hidden"
                >
                  {/* Merchant Card Header */}
                  <div className="p-6 border-b border-gray-100">
                    <div className="flex items-center space-x-3">
                      <div className="rounded-full bg-blue-100 p-2">
                        <Store className="h-6 w-6 text-blue-600" />
                      </div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        {merchant.merch_name}
                      </h3>
                    </div>
                  </div>

                  {/* Merchant Details */}
                  <div className="p-6 space-y-4">
                    <div className="flex items-start space-x-3">
                      <MapPin className="h-5 w-5 text-gray-400 mt-0.5" />
                      <span className="text-gray-600">{merchant.merch_address}</span>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      <Building2 className="h-5 w-5 text-gray-400" />
                      <span className="text-gray-600">UEN: {merchant.merch_uen}</span>
                    </div>

                    {merchant.merch_phone && (
                      <div className="flex items-center space-x-3">
                        <Phone className="h-5 w-5 text-gray-400" />
                        <span className="text-gray-600">{merchant.merch_phone}</span>
                      </div>
                    )}

                    {merchant.merch_email && (
                      <div className="flex items-center space-x-3">
                        <Mail className="h-5 w-5 text-gray-400" />
                        <span className="text-gray-600">{merchant.merch_email}</span>
                      </div>
                    )}
                  </div>

                  {/* Call to Action */}
                  <div className="px-6 pb-6">
                    <button 
                      className="w-full bg-blue-50 text-blue-600 py-2 px-4 rounded-lg hover:bg-blue-100 transition-colors duration-200 font-medium"
                    >
                      Pay This Merchant
                    </button>
                  </div>
                </div>
              ))
            ) : (
              <div className="col-span-full text-center py-12">
                <Store className="h-12 w-12 mx-auto text-gray-400 mb-4" />
                <p className="text-gray-500 text-lg">No merchants found matching your search.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default PayMerchant;