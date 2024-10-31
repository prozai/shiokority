import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import merchantController from '../controller/merchantController';
import Sidebar from '../components/sidebar';
import { 
  User, 
  Mail, 
  Phone, 
  MapPin, 
  Building2, 
  Clock,
  Receipt,
  CreditCard,
  ChevronRight,
  AlertCircle
} from 'lucide-react';

const Profile = () => {
  const [profileData, setProfileData] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await merchantController.getProfile();
        setProfileData(data);
        if (data.merchant?.merch_id) {
          fetchTransactionHistory();
        }
      } catch (error) {
        setMessage('Failed to load data. Please try again later.');
      }
    };

    const fetchTransactionHistory = async () => {
      try {
        const data = await merchantController.getTransactionHistory();
        setTransactions(data.slice(0, 5)); // Show only last 5 transactions
      } catch (error) {
        console.error("Error fetching transactions:", error);
      }
    };

    fetchProfile();
  }, []);

  const handleViewTransactionHistory = () => {
    navigate('/transactions');
  };

  if (!profileData && !message) {
    return (
      <div className="flex h-screen bg-gray-100">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="animate-pulse text-gray-500">Loading profile...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />

      <div className="flex-1 p-6 overflow-auto">
        <div className="max-w-4xl mx-auto space-y-6">
          {/* Profile Header */}
          <div className="bg-white rounded-xl shadow-sm overflow-hidden">
            <div className="border-b px-6 py-4">
              <div className="flex items-center space-x-3">
                <div className="rounded-full bg-blue-100 p-2">
                  <User className="h-6 w-6 text-blue-600" />
                </div>
                <h2 className="text-2xl font-bold text-[#153247]">Merchant Profile</h2>
              </div>
            </div>

            {message ? (
              <div className="p-6 flex items-center justify-center text-red-500 space-x-2">
                <AlertCircle className="h-5 w-5" />
                <span>{message}</span>
              </div>
            ) : (
              <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="flex items-center space-x-3">
                  <User className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="text-sm text-gray-500">Name</p>
                    <p className="font-medium text-gray-900">{profileData.merch_name}</p>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <Mail className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="text-sm text-gray-500">Email</p>
                    <p className="font-medium text-gray-900">{profileData.merch_email}</p>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <Phone className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="text-sm text-gray-500">Phone</p>
                    <p className="font-medium text-gray-900">{profileData.merch_phone}</p>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <MapPin className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="text-sm text-gray-500">Address</p>
                    <p className="font-medium text-gray-900">{profileData.merch_address}</p>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <Building2 className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="text-sm text-gray-500">UEN</p>
                    <p className="font-medium text-gray-900">{profileData.merch_uen}</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Recent Transactions */}
          <div className="bg-white rounded-xl shadow-sm overflow-hidden">
            <div className="border-b px-6 py-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="rounded-full bg-green-100 p-2">
                    <Receipt className="h-6 w-6 text-green-600" />
                  </div>
                  <h3 className="text-xl font-bold text-[#153247]">Recent Transactions</h3>
                </div>
                <button
                  onClick={handleViewTransactionHistory}
                  className="flex items-center text-blue-600 hover:text-blue-700 font-medium"
                >
                  View All
                  <ChevronRight className="h-5 w-5 ml-1" />
                </button>
              </div>
            </div>

            <div className="divide-y">
              {transactions.length > 0 ? (
                transactions.map((transaction) => (
                  <div
                    key={transaction.payment_id}
                    className="p-4 hover:bg-gray-50 transition-colors duration-150"
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex items-center space-x-3">
                        <div className="rounded-full bg-blue-50 p-2">
                          <CreditCard className="h-5 w-5 text-blue-500" />
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">
                            ${parseFloat(transaction.payment_record_amount).toFixed(2)}
                          </p>
                          <p className="text-sm text-gray-500">
                            ID: {transaction.payment_record_id}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2 text-gray-500">
                        <Clock className="h-4 w-4" />
                        <span className="text-sm">
                          {new Date(transaction.payment_record_date_created).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="p-6 text-center text-gray-500">
                  <Receipt className="h-12 w-12 mx-auto mb-2 text-gray-400" />
                  <p>No recent transactions available.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;