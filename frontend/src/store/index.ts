import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import patientReducer from './slices/patientSlice';
import appointmentReducer from './slices/appointmentSlice';
import bedReducer from './slices/bedSlice';
import emergencyReducer from './slices/emergencySlice';
import labReducer from './slices/labSlice';
import pharmacyReducer from './slices/pharmacySlice';
import billingReducer from './slices/billingSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    patients: patientReducer,
    appointments: appointmentReducer,
    beds: bedReducer,
    emergency: emergencyReducer,
    lab: labReducer,
    pharmacy: pharmacyReducer,
    billing: billingReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch; 