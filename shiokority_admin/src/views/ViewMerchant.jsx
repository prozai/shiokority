import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import AdministratorController from '../controller/administratorController';


const ViewMerchants = () => {

  const queryClient = useQueryClient();
  
  const { data, isLoading, isError } = useQuery({
    queryKey: ['merchant'],
    queryFn: AdministratorController.getMerchantData,
  });

  const updateStatusMutation = useMutation({
    mutationFn: ({ merchantId, status }) => AdministratorController.updateMerchantStatus(merchantId, status),
    onSuccess: () => {
      queryClient.invalidateQueries('merchant');
    },
  });

  const handleStatusChange = (merchantId, newStatus) => {
    updateStatusMutation.mutate({ merchantId, status: newStatus });
  };
  
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
              <td>{merchant.status === 1 ? 'Active' : 'Suspend'}</td>
              <td>
                <Link to={`/edit-merchant/${merchant.merch_id}`}>
                  <button>Edit</button>
                </Link>
                <select
                  value={merchant.status}
                  onChange={(e) => handleStatusChange(merchant.merch_id, e.target.value)}
                >
                  <option value="1">Active</option>
                  <option value="0">Suspended</option>
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
  
};

export default ViewMerchants;
