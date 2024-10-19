import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link, useNavigate } from 'react-router-dom';
import { FiEdit, FiTrash2 } from 'react-icons/fi';
import AdministratorController from '../controller/administratorController';

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

  const totalPages = Math.ceil(data?.length / itemsPerPage);

  const paginateData = (data, pageNumber, itemsPerPage) => {
    const startIndex = (pageNumber - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    return data.slice(startIndex, endIndex);
  };

  const currentData = data ? paginateData(data, currentPage, itemsPerPage) : [];

  const handlePrevious = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleNext = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  if (isLoading) return <p>Loading...</p>;
  if (isError) return <p>Error: {isError.message}</p>;

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h3 className="text-2xl font-bold mb-4">Merchant Management</h3>

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
        <div className="overflow-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="text-gray-600">
                <th className="py-2 px-4">Merchant ID</th>
                <th className="py-2 px-4">Name</th>
                <th className="py-2 px-4">Phone</th>
                <th className="py-2 px-4">Email</th>
                <th className="py-2 px-4">Date Created</th>
                <th className="py-2 px-4">Date Updated</th>
                <th className="py-2 px-4">Account Status</th>
                <th className="py-2 px-4">Actions</th>
              </tr>
            </thead>
            <tbody>
              {currentData.map((merchant) => (
                <tr
                  key={merchant.merch_id}
                  className="border-b hover:bg-gray-100"
                >
                  <td className="py-2 px-4">{merchant.merch_id}</td>
                  <td className="py-2 px-4">{merchant.merch_name}</td>
                  <td className="py-2 px-4">{merchant.merch_phone}</td>
                  <td className="py-2 px-4">{merchant.merch_email}</td>
                  <td className="py-2 px-4">{merchant.date_created}</td>
                  <td className="py-2 px-4">{merchant.date_updated_on}</td>
                  <td className="py-2 px-4">
                    <span
                      className={`px-2 py-1 rounded-full text-xs ${
                        merchant.merch_status === 1
                          ? 'bg-green-200 text-green-800'
                          : 'bg-red-200 text-red-800'
                      }`}
                    >
                      {merchant.merch_status === 1 ? 'Active' : 'Suspended'}
                    </span>
                  </td>
                  <td className="py-2 px-4 flex space-x-2">
                    <Link
                      to={`/edit-merchant/${merchant.merch_id}`}
                      className="text-blue-600 hover:text-blue-800"
                    >
                      <FiEdit />
                    </Link>
                    <button
                      onClick={() =>
                        handleStatusChange(
                          merchant.merch_id,
                          merchant.merch_status === 1 ? 0 : 1
                        )
                      }
                      className="text-red-600 hover:text-red-800"
                    >
                      <FiTrash2 />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination Controls */}
        <div className="flex justify-between mt-4">
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
