import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const MerchantEdit = () => {
    const { merchId } = useParams();
    const [merchant, setMerchant] = useState({
        merch_name: '',
        merch_email: '',
        merch_phone: ''
    });

    useEffect(() => {
        // Fetch merchant data
        axios.get(`/admin/merchants/${merchId}`)
            .then(response => {
                setMerchant(response.data);
            })
            .catch(error => {
                console.error("There was an error fetching the merchant data!", error);
            });
    }, [merchId]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setMerchant({ ...merchant, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.put(`/admin/merchants/${merchId}`, merchant)
            .then(response => {
                alert('Merchant updated successfully');
            })
            .catch(error => {
                console.error("There was an error updating the merchant!", error);
            });
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
                <button type="submit">Update</button>
            </form>
        </div>
    );
};

export default MerchantEdit;
