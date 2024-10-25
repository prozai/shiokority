import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link, useNavigate } from 'react-router-dom';
import { FiEdit, FiTrash2 } from 'react-icons/fi';
import AdministratorController from '../controller/administratorController';
import ShiokorityAdminLogo from '../asset/image/ShiokorityAdmin.png';

const ViewMerchants = () => {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const itemsPerPage = 10; // Define items per page
  const [currentPage, setCurrentPage] = useState(1);

  const { data, isLoading, isError } = useQuery({
    queryKey: ['merchant'],
    queryFn: AdministratorController.getMerchantData,
  });

  const updateStatusMutation = useMutation({
    mutationFn: ({ merchantId, status }) =>
      AdministratorController.updateMerchantStatus(merchantId, status),
    onSuccess: () => {
      queryClient.invalidateQueries('merchant');
    },
  });

  const handleStatusChange = (merchantId, newStatus) => {
    updateStatusMutation.mutate({ merchantId, status: newStatus });
  };

  const handleAddMerchant = () => {
    navigate('/create-merchant');
  };

  const handleLogoClick = () => {
    navigate('/dashboard');
  };

  const handleBackClick = () => {
    navigate('/dashboard');
  };

  if (isLoading) return <p>Loading...</p>;
  if (isError) return <p>Error: {isError.message}</p>;

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      {/* Logo at the top left */}
      <div className="flex items-center mb-4">
        <img
          src={ShiokorityAdminLogo}
          alt="Shiokority Admin"
          className="h-20 mr-4 cursor-pointer"
          onClick={handleLogoClick}
        />
        <h1 className="text-3xl font-bold">Merchant Management</h1>
      </div>
      
      {/* Search and Add Merchant Button */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex justify-between items-center mb-4">
          <input
            type="text"
            placeholder="Search ID"
            className="border rounded-lg p-2 w-1/4"
          />
          <button
            onClick={handleAddMerchant}
            className="bg-[#153247] text-white py-2 px-4 rounded-lg hover:bg-green-600"
          >
            + Add Merchant
          </button>
        </div>

        {/* Merchant Table */}
        <table className="w-full text-left">
          <thead>
            <tr className="text-gray-600">
              <th className="py-2 px-4 border-b">Merchant ID</th>
              <th className="py-2 px-4 border-b">Name</th>
              <th className="py-2 px-4 border-b">Phone</th>
              <th className="py-2 px-4 border-b">Email</th>
              <th className="py-2 px-4 border-b">Date Created</th>
              <th className="py-2 px-4 border-b">Date Updated</th>
              <th className="py-2 px-4 border-b">Account Status</th>
              <th className="py-2 px-4 border-b">Actions</th>
            </tr>
          </thead>
          <tbody>
            {data.map(merchant => (
              <tr key={merchant.merch_id} className="hover:bg-gray-100">
                <td className="py-2 px-4 border-b">{merchant.merch_id}</td>
                <td className="py-2 px-4 border-b">{merchant.merch_name}</td>
                <td className="py-2 px-4 border-b">{merchant.merch_phone}</td>
                <td className="py-2 px-4 border-b">{merchant.merch_email}</td>
                <td className="py-2 px-4 border-b">{merchant.date_created}</td>
                <td className="py-2 px-4 border-b">{merchant.date_updated_on}</td>
                <td className="py-2 px-4 border-b">
                  <span className={`px-2 py-1 rounded-full text-xs ${merchant.merch_status === 1 ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'}`}>
                    {merchant.merch_status === 1 ? 'Active' : 'Suspended'}
                  </span>
                </td>
                <td className="py-2 px-4 border-b flex space-x-2">
                  <Link to={`/edit-merchant/${merchant.merch_id}`} className="text-blue-600 hover:text-blue-800">
                    <FiEdit />
                  </Link>
                  <button onClick={() => handleStatusChange(merchant.merch_id, merchant.merch_status === 1 ? 0 : 1)} className="text-red-600 hover:text-red-800">
                    <FiTrash2 />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
         {/* Back Button */}
         <div className="mt-6">
          <button
            onClick={handleBackClick}
            className="bg-gray-300 text-black py-2 px-4 rounded-lg hover:bg-gray-400"
          >
            Back
          </button>
      </div>
    </div>
    </div>
  );
};

export default ViewMerchants;
