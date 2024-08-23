import React from 'react';
import { useQuery } from '@tanstack/react-query';

const ViewMerchants = () => {
  // Using React Query to fetch merchants

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
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
  
};

export default ViewMerchants;
