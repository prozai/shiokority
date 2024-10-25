// src/views/EditMerchant.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import AdministratorController from '../controller/administratorController';

const MerchantEdit = () => {
    const { merchId } = useParams();
    const navigate = useNavigate(); 
    const [merchant, setMerchant] = useState({
        merch_name: '',
        merch_email: '',
        merch_phone: '',
        merch_address: '',
        merch_uen: ''
    });
    const [statusMessage, setStatusMessage] = useState('');
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchMerchant = async () => {
            setIsLoading(true);
            try {
                const merchantData = await AdministratorController.fetchMerchantById(merchId);
                setMerchant(merchantData);
                setStatusMessage('');
            } catch (error) {
                console.error("Error fetching merchant in view", error);
                setStatusMessage('Error fetching merchant data');
            } finally {
                setIsLoading(false);
            }
        };
        fetchMerchant();
    }, [merchId]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setMerchant({ ...merchant, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const isSuccess = await AdministratorController.updateMerchant(merchId, merchant);
            
            setStatusMessage(isSuccess.success ? 'Merchant updated successfully' : 'Failed to update merchant');
        } catch (error) {
            console.error("Error updating merchant in view", error);
            setStatusMessage('An error occurred while updating merchant');
        } finally {
            setIsLoading(false);
        }
    };

    const handleCancel = () => {
        navigate('/user-management');  // Navigate back to user-management
    };

    return (
        <div className="p-6 bg-gray-100 min-h-screen flex justify-center items-center">
            <form onSubmit={handleSubmit} className="w-full max-w-lg bg-white p-8 rounded-lg shadow-lg">
                <h3 className="text-2xl font-bold mb-6 text-[#153247]">Edit Merchant</h3>
                {['merch_name', 'merch_email', 'merch_phone', 'merch_address', 'merch_uen'].map((field) => (
                    <div className="mb-4" key={field}>
                        <label className="block text-gray-700 text-sm font-bold mb-2 capitalize">{field.replace('merch_', '').replace('_', ' ')}</label>
                        <input
                            type="text"
                            name={field}
                            value={merchant[field]}
                            onChange={handleChange}
                            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            required
                        />
                    </div>
                ))}
                <button type="submit" disabled={isLoading} className="bg-[#153247] text-white py-2 px-4 rounded w-full hover:bg-green-600 font-semibold">
                    {isLoading ? 'Updating...' : 'Update'}
                </button>
                <button type="button" onClick={handleCancel} className="bg-gray-400 text-white py-2 px-4 rounded w-full mt-2 hover:bg-gray-500 font-semibold">
                    Cancel
                </button>
                {statusMessage && <p className="mt-4 text-center text-gray-600">{statusMessage}</p>}
            </form>
        </div>
    );
};

export default MerchantEdit;
