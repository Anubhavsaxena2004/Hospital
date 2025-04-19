// @ts-ignore
import { createTheme, responsiveFontSizes } from '@mui/material/styles';

let theme = createTheme({
  breakpoints: {
    values: {
      xs: 0,
      sm: 600,
      md: 900,
      lg: 1200,
      xl: 1536,
    },
  },
  palette: {
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#9c27b0',
      light: '#ba68c8',
      dark: '#7b1fa2',
    },
    error: {
      main: '#d32f2f',
      light: '#ef5350',
      dark: '#c62828',
    },
    warning: {
      main: '#ed6c02',
      light: '#ff9800',
      dark: '#e65100',
    },
    info: {
      main: '#0288d1',
      light: '#03a9f4',
      dark: '#01579b',
    },
    success: {
      main: '#2e7d32',
      light: '#4caf50',
      dark: '#1b5e20',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2rem',
      fontWeight: 500,
      [createTheme().breakpoints.down('sm')]: {
        fontSize: '1.75rem',
      },
    },
    h2: {
      fontSize: '1.75rem',
      fontWeight: 500,
      [createTheme().breakpoints.down('sm')]: {
        fontSize: '1.5rem',
      },
    },
    h3: {
      fontSize: '1.5rem',
      fontWeight: 500,
      [createTheme().breakpoints.down('sm')]: {
        fontSize: '1.25rem',
      },
    },
    h4: {
      fontSize: '1.25rem',
      fontWeight: 500,
      [createTheme().breakpoints.down('sm')]: {
        fontSize: '1.1rem',
      },
    },
    h5: {
      fontSize: '1.1rem',
      fontWeight: 500,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 500,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          minWidth: 'auto',
          padding: '8px 16px',
          [createTheme().breakpoints.down('sm')]: {
            padding: '6px 12px',
            fontSize: '0.875rem',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          [createTheme().breakpoints.down('sm')]: {
            margin: '8px',
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          [createTheme().breakpoints.down('sm')]: {
            marginBottom: '8px',
          },
        },
      },
    },
  },
});

theme = responsiveFontSizes(theme);

export default theme;
