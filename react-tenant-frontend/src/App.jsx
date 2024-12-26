import { useState } from 'react';
import UserList from './UserList';

function App() {
  const [tenant, setTenant] = useState('tenant_b');

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl mb-4">Tenant User Dashboard</h1>

      <div className="mb-6">
        {/* Custom Select Dropdown */}
        <div className="relative">
          <button
            className="w-[180px] p-2 bg-gray-200 text-gray-800 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            onClick={() => document.getElementById('tenant-dropdown').classList.toggle('hidden')}
          >
            {tenant === 'tenant_a' ? 'Tenant A' : tenant === 'tenant_b' ? 'Tenant B' : 'Select Tenant'}
          </button>

          <ul
            id="tenant-dropdown"
            className="absolute left-0 mt-2 w-[180px] bg-white border border-gray-300 rounded-md shadow-lg z-10 hidden"
          >
            <li
              onClick={() => setTenant('tenant_a')}
              className="px-4 py-2 cursor-pointer hover:bg-gray-100"
            >
              Tenant A
            </li>
            <li
              onClick={() => setTenant('tenant_b')}
              className="px-4 py-2 cursor-pointer hover:bg-gray-100"
            >
              Tenant B
            </li>
          </ul>
        </div>
      </div>

      <UserList tenant={tenant} />
    </div>
  );
}

export default App;
