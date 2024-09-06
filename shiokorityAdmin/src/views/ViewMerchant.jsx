import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import UpdateMerchantStatus from './SuspendMerchant';


const ViewMerchants = () => {
  

  const { data, isLoading, isError } 
  = useQuery({ 
    queryKey: ['merchant'], 
    queryFn: async () => {
        const response = await fetch('/admin/view-merchant')
        return (await response.json())

    } });
  
    

  if (isLoading) return <p>Loading...</p>;
  if (isError) return <p>Error: {isError.message}</p>;

  return (
    <div>
      <h3>View Merchants</h3>
      <table>
        <thead>
          <tr>
            <th>Merchant ID</th>
            <th>Name</th>
            <th>Phone</th>
            <th>Email</th>
            <th>Date Created</th>
            <th>Date Updated</th>
            <th>Account Status</th>
          </tr>
        </thead>
        <tbody>
          {data.map(merchant => (
            <tr key={merchant.merch_id}>
              <td>{merchant.merch_id}</td>
              <td>{merchant.merch_name}</td>
              <td>{merchant.merch_phone}</td>
              <td>{merchant.merch_email}</td>
              <td>{merchant.date_created}</td>
              <td>{merchant.date_updated_on}</td>
              <td>{merchant.merch_status === 1 ? 'Active' : 'Suspend'}</td>
              <td>
                <Link to={`/edit-merchant/${merchant.merch_id}`}>
                  <button>Edit</button>
                </Link>
                <button onClick={() => UpdateMerchantStatus(merchant.merch_id)}>Suspend</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
  
};

export default ViewMerchants;
