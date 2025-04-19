import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { Provider } from 'react-redux';
import { store } from './store';
import theme from './theme';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Patients from './pages/Patients';
import Appointments from './pages/Appointments';
import Staff from './pages/Staff';
import Beds from './pages/Beds';
import Emergency from './pages/Emergency';
import Lab from './pages/Lab';
import Pharmacy from './pages/Pharmacy';
import Billing from './pages/Billing';
import Analytics from './pages/Analytics';
import Settings from './pages/Settings';

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/patients" element={<Patients />} />
              <Route path="/appointments" element={<Appointments />} />
              <Route path="/staff" element={<Staff />} />
              <Route path="/beds" element={<Beds />} />
              <Route path="/emergency" element={<Emergency />} />
              <Route path="/lab" element={<Lab />} />
              <Route path="/pharmacy" element={<Pharmacy />} />
              <Route path="/billing" element={<Billing />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </Layout>
        </Router>
      </ThemeProvider>
    </Provider>
  );
};

export default App; 