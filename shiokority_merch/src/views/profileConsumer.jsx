import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import consumerController from '../controller/consumerController';
import CardValidation from './CardValidation';
import ShiokorityPayLogo from '../asset/image/ShiokorityPay.png';
import { 
  User, 
  Mail, 
  Phone, 
  MapPin, 
  CreditCard, 
  DollarSign,
  LogOut,
  Loader2,
  AlertCircle,
  CheckCircle2
} from 'lucide-react';

const ProfileConsumer = () => {
  const { pay_uen } = useParams();
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [paymentData, setPaymentData] = useState({ 
    cust_email: '', 
    amount: '',
    cardNumber: '',
    expiryDate: '',
    cvv: '',
    uen: pay_uen
  });
  const [cardValidation, setCardValidation] = useState({
    cardNumber: false,
    expiryDate: false,
    cvv: false
  });
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState(''); // 'success' or 'error'
  const navigate = useNavigate();

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      const data = await consumerController.getProfileConsumer();
      setProfileData(data);
      setPaymentData(prev => ({ ...prev, cust_email: data.cust_email }));
    } catch (error) {
      setMessage(error.message);
      setMessageType('error');
    } finally {
      setLoading(false);
    }
  };

  const handlePaymentChange = (e) => {
    if (e.target.name === 'amount') {
      const value = Math.max(0, Number(e.target.value));
      setPaymentData({ ...paymentData, amount: value ? value.toString() : '' });
    } else {
      setPaymentData({ ...paymentData, [e.target.name]: e.target.value });
    }
  };

  const handleCardValidationChange = (cardData, isValid) => {
    setPaymentData(prev => ({ ...prev, ...cardData }));
    setCardValidation(prev => ({ ...prev, [Object.keys(cardData)[0]]: isValid }));
  };

  const handleSendPayment = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (!Object.values(cardValidation).every(Boolean)) {
        setMessage('Please correct the card information');
        setMessageType('error');
        return;
      }
      const response = await consumerController.sendPayment(
        profileData.cust_email, 
        paymentData.amount,
        paymentData.cardNumber,
        paymentData.expiryDate,
        paymentData.cvv,
        paymentData.uen
      );
      setMessage(response.message);
      setMessageType('success');
      // Reset form after successful payment
      setPaymentData(prev => ({ ...prev, amount: '', cardNumber: '', expiryDate: '', cvv: '' }));
    } catch (error) {
      setMessage(error.message);
      setMessageType('error');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await consumerController.logoutConsumer();
      navigate('/login-consumer');
    } catch (error) {
      setMessage('Logout failed. Please try again.');
      setMessageType('error');
    }
  };

  if (loading && !profileData) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="flex items-center space-x-2 text-blue-600">
          <Loader2 className="h-6 w-6 animate-spin" />
          <span className="font-medium">Loading profile...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-xl mx-auto">
        {/* Logo and Header */}
        <div className="bg-white rounded-xl shadow-sm overflow-hidden mb-6">
          <div className="p-6 flex flex-col items-center">
            <img src={ShiokorityPayLogo} alt="Shiokority Pay" className="h-32 mb-6" />
            <h2 className="text-2xl font-bold text-[#153247]">Consumer Profile</h2>
          </div>
        </div>

        {/* Profile Information */}
        {profileData && (
          <div className="bg-white rounded-xl shadow-sm overflow-hidden mb-6">
            <div className="border-b px-6 py-4">
              <div className="flex items-center space-x-3">
                <div className="rounded-full bg-blue-100 p-2">
                  <User className="h-6 w-6 text-blue-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">Personal Information</h3>
              </div>
            </div>

            <div className="p-6 space-y-4">
              <div className="flex items-center space-x-3">
                <User className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-500">Name</p>
                  <p className="font-medium text-gray-900">{profileData.cust_fname} {profileData.cust_lname}</p>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <Mail className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-500">Email</p>
                  <p className="font-medium text-gray-900">{profileData.cust_email}</p>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <Phone className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-500">Phone</p>
                  <p className="font-medium text-gray-900">{profileData.cust_phone}</p>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <MapPin className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-500">Address</p>
                  <p className="font-medium text-gray-900">{profileData.cust_address}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Payment Form */}
        <div className="bg-white rounded-xl shadow-sm overflow-hidden mb-6">
          <div className="border-b px-6 py-4">
            <div className="flex items-center space-x-3">
              <div className="rounded-full bg-green-100 p-2">
                <CreditCard className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900">Send Payment</h3>
            </div>
          </div>

          <form onSubmit={handleSendPayment} className="p-6 space-y-6">
            <div className="relative">
              <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="number"
                name="amount"
                placeholder="Payment Amount"
                value={paymentData.amount}
                onChange={handlePaymentChange}
                min="0"
                step="0.01"
                onKeyDown={(e) => {
                  if (e.key === '-' || e.key === 'e') {
                    e.preventDefault();
                  }
                }}
                required
                className="pl-10 w-full border border-gray-300 rounded-lg py-3 px-4 text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
              />
            </div>

            <CardValidation onChange={handleCardValidationChange} />

            {message && (
              <div className={`flex items-center space-x-2 p-4 rounded-lg ${
                messageType === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
              }`}>
                {messageType === 'success' ? (
                  <CheckCircle2 className="h-5 w-5" />
                ) : (
                  <AlertCircle className="h-5 w-5" />
                )}
                <span>{message}</span>
              </div>
            )}

            <div className="space-y-4">
              <button
                type="submit"
                disabled={!Object.values(cardValidation).every(Boolean) || loading}
                className={`w-full flex items-center justify-center space-x-2 px-4 py-3 rounded-lg text-white font-medium transition-colors ${
                  Object.values(cardValidation).every(Boolean) && !loading
                    ? 'bg-[#153247] hover:bg-[#1a3d5c]'
                    : 'bg-gray-400 cursor-not-allowed'
                }`}
              >
                {loading ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin" />
                    <span>Processing...</span>
                  </>
                ) : (
                  <>
                    <CreditCard className="h-5 w-5" />
                    <span>Send Payment</span>
                  </>
                )}
              </button>

              <button
                type="button"
                onClick={handleLogout}
                className="w-full flex items-center justify-center space-x-2 px-4 py-3 rounded-lg text-white font-medium bg-red-500 hover:bg-red-600 transition-colors"
              >
                <LogOut className="h-5 w-5" />
                <span>Logout</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ProfileConsumer;