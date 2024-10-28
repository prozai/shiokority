import React, { useState } from 'react';
import axios from 'axios';
import { Loader2 } from 'lucide-react';

function TransactionDashboard() {
  const [activeTab, setActiveTab] = useState('record');
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  React.useEffect(() => {
    fetchData(activeTab);
  }, [activeTab]);

  const fetchData = async (type) => {
    try {
      setLoading(true);
      setError(null);
      
      let endpoint;
      switch(type) {
        case 'transactions':
          endpoint = 'bank/view_transaction';
          break;
        case 'history':
          endpoint = 'bank/view_transactionHistory';
          break;
        case 'record':
          endpoint = 'bank/view_transactionRecord';
          break;
        default:
          endpoint = 'bank/view_transaction';
      }
        
      const response = await axios.get(endpoint);
      setData(response.data);
    } catch (error) {
      setError('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const handleTabClick = (tab) => {
    setActiveTab(tab);
    fetchData(tab);
  };

  const DataRow = ({ label, value }) => (
    <div className="flex items-center py-3 border-b border-gray-800/50">
      <div className="w-1/2 text-[#a7b8c1] text-sm">
        {label}
      </div>
      <div className="w-1/2 text-[#e5eaed] text-sm">
        {value}
      </div>
    </div>
  );

  const TransactionCard = ({ item }) => {
    if (!item) return null;

    return (
      <div className="bg-[#1a1f24] rounded mb-2 p-4">
        {Object.entries(item).map(([key, value]) => (
          <DataRow
            key={key}
            label={key}
            value={
              key.includes('status') ? (
                <span className={`px-2 py-1 rounded text-xs ${
                  value === 'completed' 
                    ? 'bg-green-500/10 text-green-400'
                    : value === 'pending'
                    ? 'bg-yellow-500/10 text-yellow-400'
                    : value === 'failed'
                    ? 'bg-red-500/10 text-red-400'
                    : 'bg-gray-500/10 text-gray-400'
                }`}>
                  {value}
                </span>
              ) : key.includes('amount') ? (
                <span className="text-[#e5eaed] font-medium">
                  {value}
                </span>
              ) : value
            }
          />
        ))}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-[#111518]">
      <div className="max-w-4xl mx-auto">
        {/* Navigation Tabs */}
        <div className="flex bg-[#1a1f24]">
          {[
            { id: 'transactions', label: 'Transactions' },
            { id: 'history', label: 'History' },
            { id: 'record', label: 'Record' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => handleTabClick(tab.id)}
              className={`
                flex-1 px-6 py-3 text-sm transition-colors
                ${activeTab === tab.id
                  ? 'bg-[#111518] text-white'
                  : 'text-[#a7b8c1] hover:text-[#e5eaed] hover:bg-[#111518]/50'
                }
              `}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <div className="p-6">
          {loading ? (
            <div className="flex justify-center items-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-[#a7b8c1]" />
            </div>
          ) : error ? (
            <div className="bg-red-900/20 text-red-400 p-4 rounded">
              {error}
            </div>
          ) : (
            <div>
              {Array.isArray(data) && data.length > 0 ? (
                data.map((item, index) => (
                  <TransactionCard key={item.id || index} item={item} />
                ))
              ) : (
                <div className="text-center py-12 text-[#a7b8c1] bg-[#1a1f24] rounded">
                  No data available
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default TransactionDashboard;