// src/views/MerchantEdit.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import AdministratorController from '../controller/administratorController';

const MerchantEdit = () => {
    const { merchId } = useParams();
    const [merchant, setMerchant] = useState({
        merch_name: '',
        merch_email: '',
        merch_phone: '',
        merch_address: ''
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
            
            if (isSuccess.success) {
                setStatusMessage('Merchant updated successfully');
            } else {
                setStatusMessage('Failed to update merchant');
            }
        } catch (error) {
            console.error("Error updating merchant in view", error);
            setStatusMessage('An error occurred while updating merchant');
        } finally {
            setIsLoading(false);
        }
    };


    return (
        <div>
            <h2>Edit Merchant</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Name:</label>
                    <input 
                        type="text"         
                        name="merch_name" 
                        value={merchant.merch_name} 
                        onChange={handleChange} 
                    />
                </div>
                <div>
                    <label>Email:</label>
                    <input 
                        type="email" 
                        name="merch_email" 
                        value={merchant.merch_email} 
                        onChange={handleChange} 
                    />
                </div>
                <div>
                    <label>Phone:</label>
                    <input 
                        type="text" 
                        name="merch_phone" 
                        value={merchant.merch_phone} 
                        onChange={handleChange} 
                    />
                </div>
                <div>
                    <label>Address:</label>
                    <input 
                    type="text"
                    name="merch_address"
                    value={merchant.merch_address}
                    onChange={handleChange}
                    />
                </div>            

                <br />
                <button type="submit" disabled={isLoading}>
                    {isLoading ? 'Updating...' : 'Update'}
                </button>
                
            </form>
            <br />
            {statusMessage && <div className="status-message">{statusMessage}</div>}
        </div>
    );
};

export default MerchantEdit;