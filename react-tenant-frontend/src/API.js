import axios from 'axios';

export const fetchUsers = async (tenant) => {
  try {
    const response = await axios.get('http://localhost:8080/users/', {
      headers: {
        'X-Tenant-ID': tenant,
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching users:', error);
    throw error;
  }
};