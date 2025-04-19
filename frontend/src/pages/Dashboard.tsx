import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import {
  People as PeopleIcon,
  Hotel as BedIcon,
  LocalHospital as HospitalIcon,
  AttachMoney as MoneyIcon,
  Event as EventIcon,
  Warning as WarningIcon,
} from '@mui/icons-material';
import { useSelector } from 'react-redux';
import { RootState } from '../store';

const Dashboard: React.FC = () => {
  const { patients, appointments, beds, emergency } = useSelector((state: RootState) => ({
    patients: state.patients,
    appointments: state.appointments,
    beds: state.beds,
    emergency: state.emergency,
  }));

  const stats = [
    {
      title: 'Total Patients',
      value: patients.total,
      icon: <PeopleIcon sx={{ fontSize: 40 }} />,
      color: '#1976d2',
    },
    {
      title: 'Available Beds',
      value: beds.available,
      icon: <BedIcon sx={{ fontSize: 40 }} />,
      color: '#2e7d32',
    },
    {
      title: 'Staff On Duty',
      value: 25, // This should come from the staff slice
      icon: <HospitalIcon sx={{ fontSize: 40 }} />,
      color: '#ed6c02',
    },
    {
      title: 'Today\'s Revenue',
      value: '$12,500', // This should come from the billing slice
      icon: <MoneyIcon sx={{ fontSize: 40 }} />,
      color: '#9c27b0',
    },
    {
      title: 'Today\'s Appointments',
      value: appointments.today,
      icon: <EventIcon sx={{ fontSize: 40 }} />,
      color: '#0288d1',
    },
    {
      title: 'Emergency Alerts',
      value: emergency.active,
      icon: <WarningIcon sx={{ fontSize: 40 }} />,
      color: '#d32f2f',
    },
  ];

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Grid container spacing={3}>
        {stats.map((stat) => (
          <Grid item xs={12} sm={6} md={4} key={stat.title}>
            <Paper
              sx={{
                p: 2,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                height: 140,
                backgroundColor: stat.color,
                color: 'white',
              }}
            >
              <Box sx={{ mb: 1 }}>{stat.icon}</Box>
              <Typography variant="h6" component="div">
                {stat.title}
              </Typography>
              <Typography variant="h4" component="div">
                {stat.value}
              </Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Dashboard; 