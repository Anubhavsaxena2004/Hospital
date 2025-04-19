import React from 'react';
import { Box, Drawer, AppBar, Toolbar, List, Typography, Divider, IconButton, ListItem, ListItemIcon, ListItemText, useTheme, Theme } from '@mui/material';
// @ts-ignore
import { Menu as MenuIcon, Dashboard, People, CalendarToday, Hotel, Emergency, Science, LocalPharmacy, AttachMoney, Analytics, Settings } from '@mui/icons-material';
// @ts-ignore
import { useNavigate, useLocation } from 'react-router-dom';
// @ts-ignore
import { useSelector } from 'react-redux';
// @ts-ignore
import { RootState } from '../store';
// @ts-ignore
import { Theme } from '@mui/material/styles'; // Make sure this is imported

const drawerWidth = {
  xs: 200,
  sm: 240
};

const menuItems = [
  { text: 'Dashboard', icon: <Dashboard />, path: '/' },
  { text: 'Patients', icon: <People />, path: '/patients' },
  { text: 'Appointments', icon: <CalendarToday />, path: '/appointments' },
  { text: 'Staff', icon: <People />, path: '/staff' },
  { text: 'Beds', icon: <Hotel />, path: '/beds' },
  { text: 'Emergency', icon: <Emergency />, path: '/emergency' },
  { text: 'Lab', icon: <Science />, path: '/lab' },
  { text: 'Pharmacy', icon: <LocalPharmacy />, path: '/pharmacy' },
  { text: 'Billing', icon: <AttachMoney />, path: '/billing' },
  { text: 'Analytics', icon: <Analytics />, path: '/analytics' },
  { text: 'Settings', icon: <Settings />, path: '/settings' },
];

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const theme = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const user = useSelector((state: RootState) => state.auth.user);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawer = (
    <div>
      <Toolbar>
        <Typography variant="h6" noWrap component="div">
          Hospital Management
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem
            button
            key={item.text}
            onClick={() => navigate(item.path)}
            selected={location.pathname === item.path}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </div>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position="fixed"
        sx={{
          width: { xs: '100%', sm: `calc(100% - ${drawerWidth.sm}px)` },
          ml: { sm: `${drawerWidth.sm}px` },
         

          // In the sx prop:
          bgcolor: (theme: Theme) => theme.palette.mode === 'dark' ? '#1a1a1a' : '#ffffff',
          color: (theme: Theme) => theme.palette.mode === 'dark' ? '#ffffff' : 'rgba(0, 0, 0, 0.87)',
          borderBottom: (theme: Theme) => `1px solid ${theme.palette.divider}`,
          '&:hover': {
            backgroundColor: (theme: Theme) => theme.palette.mode === 'dark' ? '#2E2E2E' : '#1565c0'
          }

        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ 
              mr: 2, 
              display: { sm: 'none' },
              fontSize: '1.5rem',
              color: 'inherit',
              '&:hover': {
                backgroundColor: (theme: Theme) => theme.palette.mode === 'dark' ? '#2E2E2E' : '#1565c0'
              }
              
            }}
          >
            <MenuIcon fontSize="large" />
          </IconButton>
          <Typography 
            variant="h6" 
            noWrap 
            component="div" 
            sx={{ 
              flexGrow: 1,
              fontSize: { xs: '1.1rem', sm: '1.25rem' },
              fontWeight: 600
            }}
          >
            {menuItems.find(item => item.path === location.pathname)?.text || 'Dashboard'}
          </Typography>
          {user && (
            <Typography 
              variant="subtitle1" 
              sx={{
                fontSize: { xs: '0.9rem', sm: '1rem' },
                fontWeight: 500
              }}
            >
              {user.username} ({user.role})
            </Typography>
          )}
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
          sx={{ 
            width: { xs: drawerWidth.xs, sm: drawerWidth.sm }, 
            flexShrink: { sm: 0 } 
          }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { 
              boxSizing: 'border-box', 
              width: drawerWidth.xs,
              backgroundColor: theme.palette.background.paper
            },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { 
              boxSizing: 'border-box', 
              width: drawerWidth.sm,
              backgroundColor: theme.palette.background.paper
            },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: { xs: 1, sm: 3 },
          width: { xs: '100%', sm: `calc(100% - ${drawerWidth.sm}px)` },
          mt: '56px',
        }}
      >
        {children}
      </Box>
    </Box>
  );
};

export default Layout; 