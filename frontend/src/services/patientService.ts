import axios from 'axios';

const API_URL = '/api';

export interface Patient {
  id: number;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: 'M' | 'F' | 'O';
  address: string;
  phone_number: string;
  emergency_contact: string;
  blood_group: string;
  medical_history: string;
  created_at: string;
  updated_at: string;
}

export interface PatientFormData {
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: 'M' | 'F' | 'O';
  address: string;
  phone_number: string;
  emergency_contact: string;
  blood_group: string;
  medical_history?: string;
}

const patientService = {
  getAllPatients: async (): Promise<Patient[]> => {
    const response = await axios.get(`${API_URL}/patients/`);
    return response.data;
  },

  getPatient: async (id: number): Promise<Patient> => {
    const response = await axios.get(`${API_URL}/patients/${id}/`);
    return response.data;
  },

  createPatient: async (patientData: PatientFormData): Promise<Patient> => {
    const response = await axios.post(`${API_URL}/patients/`, patientData);
    return response.data;
  },

  updatePatient: async (id: number, patientData: Partial<PatientFormData>): Promise<Patient> => {
    const response = await axios.put(`${API_URL}/patients/${id}/`, patientData);
    return response.data;
  },

  deletePatient: async (id: number): Promise<void> => {
    await axios.delete(`${API_URL}/patients/${id}/`);
  },

  searchPatients: async (query: string): Promise<Patient[]> => {
    const response = await axios.get(`${API_URL}/patients/search/?q=${query}`);
    return response.data;
  },

  getPatientMedicalRecords: async (id: number): Promise<any[]> => {
    const response = await axios.get(`${API_URL}/patients/${id}/medical-records/`);
    return response.data;
  },

  getPatientAppointments: async (id: number): Promise<any[]> => {
    const response = await axios.get(`${API_URL}/patients/${id}/appointments/`);
    return response.data;
  },

  getPatientBilling: async (id: number): Promise<any[]> => {
    const response = await axios.get(`${API_URL}/patients/${id}/billing/`);
    return response.data;
  },
};

export default patientService; 